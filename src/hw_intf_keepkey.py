#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Bertrand256
# Created on: 2017-03
import json
import binascii
import logging
import unicodedata
from typing import Optional, Tuple, List, Dict
from keepkeylib.client import TextUIMixin as keepkey_TextUIMixin
from keepkeylib.client import ProtocolMixin as keepkey_ProtocolMixin
from keepkeylib.client import BaseClient as keepkey_BaseClient, CallException
from keepkeylib import messages_pb2 as keepkey_proto
from keepkeylib.tx_api import TxApiInsight
from mnemonic import Mnemonic
import polis_utils
from hw_common import HardwareWalletCancelException, ask_for_pin_callback, ask_for_pass_callback, ask_for_word_callback, \
    HwSessionInfo, select_hw_device
import keepkeylib.types_pb2 as proto_types
from wnd_utils import WndUtils
from hw_common import clean_bip32_path


class MyKeepkeyTextUIMixin(keepkey_TextUIMixin):

    def __init__(self, transport, ask_for_pin_fun, ask_for_pass_fun, passphrase_encoding):
        keepkey_TextUIMixin.__init__(self, transport)
        self.ask_for_pin_fun = ask_for_pin_fun
        self.ask_for_pass_fun = ask_for_pass_fun
        self.passphrase_encoding = passphrase_encoding
        self.__mnemonic = Mnemonic('english')

    def callback_PassphraseRequest(self, msg):
        passphrase = self.ask_for_pass_fun(msg)
        if passphrase is None:
            raise HardwareWalletCancelException('Cancelled')
        else:
            if self.passphrase_encoding in ('NFKD', 'NFC'):
                passphrase = unicodedata.normalize(self.passphrase_encoding, passphrase)
            else:
                raise Exception('Invalid passphrase encoding value: ' + self.passphrase_encoding)
        return keepkey_proto.PassphraseAck(passphrase=passphrase)

    def callback_PinMatrixRequest(self, msg):
        if msg.type == 1:
            desc = 'Enter current PIN'
        elif msg.type == 2:
            desc = 'Enter new PIN'
        elif msg.type == 3:
            desc = 'Enter new PIN again'
        else:
            desc = 'Enter PIN'
        pin = self.ask_for_pin_fun(desc)
        if not pin:
            raise HardwareWalletCancelException('Cancelled')
        return keepkey_proto.PinMatrixAck(pin=pin)

    def callback_WordRequest(self, msg):
        msg = "Enter one word of mnemonic: "
        word = ask_for_word_callback(msg, self.__mnemonic.wordlist)
        if not word:
            raise HardwareWalletCancelException('Cancelled')
        return keepkey_proto.WordAck(word=word)


class MyKeepkeyClient(keepkey_ProtocolMixin, MyKeepkeyTextUIMixin, keepkey_BaseClient):
    def __init__(self, transport, ask_for_pin_fun, ask_for_pass_fun, passphrase_encoding):
        keepkey_ProtocolMixin.__init__(self, transport, ask_for_pin_fun, ask_for_pass_fun, passphrase_encoding)
        MyKeepkeyTextUIMixin.__init__(self, transport, ask_for_pin_fun, ask_for_pass_fun, passphrase_encoding)
        keepkey_BaseClient.__init__(self, transport)


def get_device_list(return_clients: bool = True, passphrase_encoding: Optional[str] = 'NFC',
                    allow_bootloader_mode: bool = False) \
        -> Tuple[List[Dict], List[Exception]]:
    """
    :return: Tuple[List[Dict <{'client': MyTrezorClient, 'device_id': str, 'desc',: str, 'model': str}>],
                   List[Exception]]
    """
    from keepkeylib.transport_hid import HidTransport

    ret_list = []
    exceptions: List[Exception] = []
    device_ids = []
    was_bootloader_mode = False

    for d in HidTransport.enumerate():
        try:
            transport = HidTransport(d)
            client = MyKeepkeyClient(transport, ask_for_pin_callback, ask_for_pass_callback, passphrase_encoding)

            if client.features.bootloader_mode:
                if was_bootloader_mode:
                    # in bootloader mode the device_id attribute isn't available, so for a given client object
                    # we are unable to distinguish between being the same device reached with the different
                    # transport and being another device
                    # for that reason, to avoid returning duplicate clients for the same device, we don't return
                    # more than one instance of a device in bootloader mod
                    client.close()
                    continue
                was_bootloader_mode = True

            if (not client.features.bootloader_mode or allow_bootloader_mode) and \
                (client.features.device_id not in device_ids or client.features.bootloader_mode):

                version = f'{client.features.major_version}.{client.features.minor_version}.' \
                          f'{client.features.patch_version}'
                if client.features.label:
                    desc = client.features.label
                else:
                    desc = '[UNNAMED]'
                desc = f'{desc} (ver: {version}, id: {client.features.device_id})'

                c = {
                    'client': client,
                    'device_id': client.features.device_id,
                    'desc': desc,
                    'model': client.features.model,
                    'bootloader_mode': client.features.bootloader_mode
                }

                ret_list.append(c)
                device_ids.append(client.features.device_id)  # beware: it's empty in bootloader mode
            else:
                # the same device is already connected using different connection medium
                client.close()
        except Exception as e:
            logging.warning(
                f'Cannot create Keepkey client ({d.__class__.__name__}) due to the following error: ' + str(e))
            exceptions.append(e)

    if not return_clients:
        for cli in ret_list:
            cli['client'].close()
            cli['client'] = None

    return ret_list, exceptions


def connect_keepkey(passphrase_encoding: Optional[str] = 'NFC',
                    device_id: Optional[str] = None) -> Optional[MyKeepkeyClient]:
    """
    Connect to a Keepkey device.
    :passphrase_encoding: Allowed values: 'NFC' or 'NFKD'. Note: Keekpey uses NFC encoding for passphrases, which is
        incompatible with BIP-39 standard (NFKD). This argument gives the possibility to enforce comforming the
        standard encoding.
    :return: ref to a keepkey client if connection successfull or None if we are sure that no Keepkey device connected.
    """

    logging.info('Started function')
    def get_client() -> Optional[MyKeepkeyClient]:
        hw_clients, exceptions = get_device_list(passphrase_encoding=passphrase_encoding)
        if not hw_clients:
            if exceptions:
                raise exceptions[0]
        else:
            selected_client = None
            if device_id:
                # we have to select a device with the particular id number
                for cli in hw_clients:
                    if cli['device_id'] == device_id:
                        selected_client = cli['client']
                        break
                    else:
                        cli['client'].close()
                        cli['client'] = None
            else:
                # we are not forced to automatically select the particular device
                if len(hw_clients) > 1:
                    hw_names = [a['desc'] for a in hw_clients]

                    selected_index = select_hw_device(None, 'Select Keepkey device', hw_names)
                    if selected_index is not None and (0 <= selected_index < len(hw_clients)):
                        selected_client = hw_clients[selected_index]
                else:
                    selected_client = hw_clients[0]['client']

            # close all the clients but the selected one
            for cli in hw_clients:
                if cli['client'] != selected_client:
                    cli['client'].close()
                    cli['client'] = None

            return selected_client
        return None

    # HidTransport.enumerate() has to be called in the main thread - second call from bg thread
    # causes SIGSEGV
    client = WndUtils.call_in_main_thread(get_client)
    if client:
        logging.info('Keepkey connected. Firmware version: %s.%s.%s, vendor: %s, initialized: %s, '
                     'pp_protection: %s, pp_cached: %s, bootloader_mode: %s ' %
                     (str(client.features.major_version),
                      str(client.features.minor_version),
                      str(client.features.patch_version), str(client.features.vendor),
                      str(client.features.initialized),
                      str(client.features.passphrase_protection), str(client.features.passphrase_cached),
                      str(client.features.bootloader_mode)))
        return client
    else:
        if device_id:
            msg = 'Cannot connect to the Keepkey device with this id: .' % device_id
        else:
            msg = 'Cannot find any Keepkey device.'
        raise Exception(msg)


class MyTxApiInsight(TxApiInsight):

    def __init__(self, network, url, polisd_inf, cache_dir, zcash=None):
        TxApiInsight.__init__(self, network, url, zcash)
        self.polisd_inf = polisd_inf
        self.cache_dir = cache_dir

    def fetch_json(self, url, resource, resourceid):
        cache_file = ''
        if self.cache_dir:
            cache_file = '%s/%s_%s_%s.json' % (self.cache_dir, self.network, resource, resourceid)
            try: # looking into cache first
                j = json.load(open(cache_file))
                return j
            except:
                pass
        try:
            j = self.polisd_inf.getrawtransaction(resourceid, 1)
        except Exception as e:
            raise
        if cache_file:
            try: # saving into cache
                json.dump(j, open(cache_file, 'w'))
            except Exception as e:
                pass
        return j


def prepare_transfer_tx(hw_session: HwSessionInfo, utxos_to_spend: List[dict], dest_addresses: List[Tuple[str, int, str]], tx_fee):
    """
    Creates a signed transaction.
    :param hw_session:
    :param utxos_to_spend: list of utxos to send
    :param dest_address: destination (Polis) address
    :param tx_fee: transaction fee
    :return: tuple (serialized tx, total transaction amount in satoshis)
    """

    insight_network = 'insight_polis'
    if hw_session.app_config.is_testnet():
        insight_network += '_testnet'
    polis_network = hw_session.app_config.polis_network

    tx_api = MyTxApiInsight(insight_network, '', hw_session.polisd_intf, hw_session.app_config.cache_dir)
    client = hw_session.hw_client
    client.set_tx_api(tx_api)
    inputs = []
    outputs = []
    inputs_amount = 0
    for utxo_index, utxo in enumerate(utxos_to_spend):
        if not utxo.get('bip32_path', None):
            raise Exception('No BIP32 path for UTXO ' + utxo['txid'])
        address_n = client.expand_path(clean_bip32_path(utxo['bip32_path']))
        it = proto_types.TxInputType(address_n=address_n, prev_hash=binascii.unhexlify(utxo['txid']),
                                     prev_index=utxo['outputIndex'])
        inputs.append(it)
        inputs_amount += utxo['satoshis']

    outputs_amount = 0
    for addr, amount, bip32_path in dest_addresses:
        outputs_amount += amount
        if addr[0] in polis_utils.get_chain_params(polis_network).B58_PREFIXES_SCRIPT_ADDRESS:
            stype = proto_types.PAYTOSCRIPTHASH
            logging.debug('Transaction type: PAYTOSCRIPTHASH' + str(stype))
        elif addr[0] in polis_utils.get_chain_params(polis_network).B58_PREFIXES_PUBKEY_ADDRESS:
            stype = proto_types.PAYTOADDRESS
            logging.debug('Transaction type: PAYTOADDRESS ' + str(stype))
        else:
            raise Exception('Invalid prefix of the destination address.')
        if bip32_path:
            address_n = client.expand_path(bip32_path)
        else:
            address_n = None

        ot = proto_types.TxOutputType(
            address=addr if address_n is None else None,
            address_n=address_n,
            amount=amount,
            script_type=stype
        )
        outputs.append(ot)

    if outputs_amount + tx_fee != inputs_amount:
        raise Exception('Transaction validation failure: inputs + fee != outputs')

    signed = client.sign_tx(hw_session.app_config.hw_coin_name, inputs, outputs)
    logging.info('Signed transaction')
    return signed[1], inputs_amount


def sign_message(hw_session: HwSessionInfo, bip32path, message):
    client = hw_session.hw_client
    address_n = client.expand_path(clean_bip32_path(bip32path))
    return client.sign_message(hw_session.app_config.hw_coin_name, address_n, message)


def change_pin(hw_session: HwSessionInfo, remove=False):
    if hw_session.hw_client:
        hw_session.hw_client.change_pin(remove)
    else:
        raise Exception('HW client not set.')


def apply_settings(hw_session: HwSessionInfo, label=None, language=None, use_passphrase=None, homescreen=None):
    if hw_session.hw_client:
        hw_session.hw_client.apply_settings()
    else:
        raise Exception('HW client not set.')


def wipe_device(hw_device_id) -> Tuple[str, bool]:
    """
    :param hw_device_id:
    :return: Tuple
        [0]: Device id. If a device is wiped before initializing with mnemonics, a new device id is generated. It's
            returned to the caller.
        [1]: True, if the user cancelled the operation. In this case we deliberately don't raise the 'cancelled'
            exception, because in the case of changing of the device id (when wiping) we want to pass the new device
            id back to the caller.
    """
    client = None
    try:
        client = connect_keepkey(device_id=hw_device_id)

        if client:
            client.wipe_device()
            hw_device_id = client.features.device_id
            client.close()
            return hw_device_id, False
        else:
            raise Exception('Couldn\'t connect to Keepkey device.')

    except CallException as e:
        if client:
            client.close()
        if not (len(e.args) >= 0 and str(e.args[1]) == 'Action cancelled by user'):
            raise
        else:
            return hw_device_id, True  # cancelled by user

    except HardwareWalletCancelException:
        if client:
            client.close()
        return hw_device_id, True  # cancelled by user


def load_device_by_mnemonic(hw_device_id: str, mnemonic: str, pin: str, passphrase_enbled: bool, hw_label: str,
                            language: Optional[str]=None) -> Tuple[str, bool]:
    """
    :param hw_device_id:
    :param mnemonic:
    :param pin:
    :param passphrase_enbled:
    :param hw_label:
    :param language:
    :return: Tuple
        [0]: Device id. If a device is wiped before initializing with mnemonics, a new device id is generated. It's
            returned to the caller.
        [1]: True, if the user cancelled the operation. In this case we deliberately don't raise the 'cancelled'
            exception, because in the case of changing of the device id (when wiping) we want to pass the new device
            id back to the caller.
    """
    client = None
    try:
        client = connect_keepkey(device_id=hw_device_id)

        if client:
            if client.features.initialized:
                client.wipe_device()
                hw_device_id = client.features.device_id
            client.load_device_by_mnemonic(mnemonic, pin, passphrase_enbled, hw_label, language=language)
            client.close()
            return hw_device_id, False
        else:
            raise Exception('Couldn\'t connect to Keepkey device.')

    except CallException as e:
        if client:
            client.close()
        if not (len(e.args) >= 0 and str(e.args[1]) == 'Action cancelled by user'):
            raise
        else:
            return hw_device_id, True  # cancelled by user

    except HardwareWalletCancelException:
        if client:
            client.close()
        return hw_device_id, True  # cancelled by user


def recovery_device(hw_device_id: str, word_count: int, passphrase_enabled: bool, pin_enabled: bool, hw_label: str) \
        -> Tuple[str, bool]:
    """
    :param hw_device_id:
    :param passphrase_enbled:
    :param pin_enbled:
    :param hw_label:
    :return: Tuple
        [0]: Device id. If a device is wiped before initializing with mnemonics, a new device id is generated. It's
            returned to the caller.
        [1]: True, if the user cancelled the operation. In this case we deliberately don't raise the 'cancelled'
            exception, because in the case of changing of the device id (when wiping) we want to pass the new device
            id back to the caller.
    """
    client = None
    try:
        client = connect_keepkey(device_id=hw_device_id)

        if client:
            if client.features.initialized:
                client.wipe_device()
                hw_device_id = client.features.device_id

            client.recovery_device(use_trezor_method=True, word_count=word_count,
                                   passphrase_protection=passphrase_enabled, pin_protection=pin_enabled,
                                   label=hw_label, language='english')
            client.close()
            return hw_device_id, False
        else:
            raise Exception('Couldn\'t connect to Keepkey device.')

    except CallException as e:
        if client:
            client.close()
        if not (len(e.args) >= 0 and str(e.args[1]) == 'Action cancelled by user'):
            raise
        else:
            return hw_device_id, True  # cancelled by user

    except HardwareWalletCancelException:
        if client:
            client.close()
        return hw_device_id, True  # cancelled by user


def reset_device(hw_device_id: str, strength: int, passphrase_enabled: bool, pin_enabled: bool,
                 hw_label: str) -> Tuple[str, bool]:
    """
    Initialize device with a newly generated words.
    :param hw_type: app_config.HWType
    :param hw_device_id: id of the device selected by the user
    :param strength: number of bits of entropy (will have impact on number of words)
    :param passphrase_enbled: if True, hw will have passphrase enabled
    :param pin_enabled: if True, hw will have pin enabled
    :param hw_label: label for device (Trezor/Keepkey)
    :return: Tuple
        Ret[0]: Device id. If a device is wiped before initializing with mnemonics, a new device id is generated. It's
            returned to the caller.
        Ret[1]: True, if the user cancelled the operation. In this situation we deliberately don't raise the
            'cancelled' exception, because in the case of changing of the device id (when wiping) we want to pass
            it back to the caller function.
    """
    client = None
    try:
        client = connect_keepkey(device_id=hw_device_id)

        if client:
            if client.features.initialized:
                client.wipe_device()
                hw_device_id = client.features.device_id

            client.reset_device(display_random=True, strength=strength, passphrase_protection=passphrase_enabled,
                                pin_protection=pin_enabled, label=hw_label, language='english')
            client.close()
            return hw_device_id, False
        else:
            raise Exception('Couldn\'t connect to Keepkey device.')

    except CallException as e:
        if client:
            client.close()
        if not (len(e.args) >= 0 and str(e.args[1]) == 'Action cancelled by user'):
            raise
        else:
            return hw_device_id, True  # cancelled by user

    except HardwareWalletCancelException:
        if client:
            client.close()
        return hw_device_id, True  # cancelled by user
