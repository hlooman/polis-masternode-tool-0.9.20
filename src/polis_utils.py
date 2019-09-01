#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Bertrand256
# Created on: 2017-03

import binascii
import base64
import typing
import bitcoin
import base58


# Bitcoin opcodes used in the application
OP_DUP = b'\x76'
OP_HASH160 = b'\xA9'
OP_EQUALVERIFY = b'\x88'
OP_CHECKSIG = b'\xAC'
OP_EQUAL = b'\x87'


class ChainParams(object):
    B58_PREFIXES_PUBKEY_ADDRESS = None
    B58_PREFIXES_SCRIPT_ADDRESS = None
    B58_PREFIXES_SECRET_KEY = None
    PREFIX_PUBKEY_ADDRESS = None
    PREFIX_SCRIPT_ADDRESS = None
    PREFIX_SECRET_KEY = None
    BIP44_COIN_TYPE = None


class ChainParamsMainNet(ChainParams):
    B58_PREFIXES_PUBKEY_ADDRESS = ['P']
    B58_PREFIXES_SCRIPT_ADDRESS = ['P']
    B58_PREFIXES_SECRET_KEY = ['3', '3']
    PREFIX_PUBKEY_ADDRESS = 55
    PREFIX_SCRIPT_ADDRESS = 56
    PREFIX_SECRET_KEY = 60
    BIP44_COIN_TYPE = 1997


class ChainParamsTestNet(ChainParams):
    B58_PREFIXES_PUBKEY_ADDRESS = ['y']
    B58_PREFIXES_SCRIPT_ADDRESS = ['8', '9']
    B58_PREFIXES_SECRET_KEY = ['9', 'c']
    PREFIX_PUBKEY_ADDRESS = 140
    PREFIX_SCRIPT_ADDRESS = 19
    PREFIX_SECRET_KEY = 239
    BIP44_COIN_TYPE = 1


def get_chain_params(polis_network: str) -> typing.ClassVar[ChainParams]:
    if polis_network == 'MAINNET':
        return ChainParamsMainNet
    elif polis_network == 'TESTNET':
        return ChainParamsTestNet
    else:
        raise Exception('Invalid \'network\' value.')


def get_default_bip32_path(polis_network: str):
    return bip32_path_n_to_string([44 + 0x80000000, get_chain_params(polis_network).BIP44_COIN_TYPE + 0x80000000, 0x80000000, 0, 0])


def get_default_bip32_base_path(polis_network: str):
    return bip32_path_n_to_string([44 + 0x80000000, get_chain_params(polis_network).BIP44_COIN_TYPE + 0x80000000])


def get_default_bip32_base_path_n(polis_network: str):
    return [44 + 0x80000000, get_chain_params(polis_network).BIP44_COIN_TYPE + 0x80000000]


def validate_bip32_path(path: str) -> bool:
    try:
        path_n = bip32_path_string_to_n(path)
        for e in path_n:
            if e < 0 or e > 0xFFFFFFFF:
                return False
        return True
    except Exception:
        return False


def pubkey_to_address(pub_key, polis_network: str):
    """Convert public key to Polis address."""
    pubkey_bin = bytes.fromhex(pub_key)
    pub_hash = bitcoin.bin_hash160(pubkey_bin)
    data = bytes([get_chain_params(polis_network).PREFIX_PUBKEY_ADDRESS]) + pub_hash
    checksum = bitcoin.bin_dbl_sha256(data)[0:4]
    return base58.b58encode(data + checksum)


def validate_address(address: str, polis_network: typing.Optional[str]) -> bool:
    """Validates if the 'address' is a valid Polis address.
    :address: address to be validated
    :polis_network: the polis network type against which the address will be validated; if the value is None, then
      the network type prefix validation will be skipped
    """
    data = base58.b58decode(address)
    if len(data) > 5:
        prefix = data[0]
        if polis_network:
            prefix_valid = (prefix == get_chain_params(polis_network).PREFIX_PUBKEY_ADDRESS)
        else:
            prefix_valid = (prefix == ChainParamsMainNet.PREFIX_PUBKEY_ADDRESS or
                            prefix == ChainParamsTestNet.PREFIX_PUBKEY_ADDRESS)
        if prefix_valid:
            pubkey_hash = data[:-4]
            checksum = data[-4:]
            if bitcoin.bin_dbl_sha256(pubkey_hash)[0:4] == checksum:
                return True
    return False


def generate_privkey(polis_network: str, compressed: bool = False):
    """
    Based on Andreas Antonopolous work from 'Mastering Bitcoin'.
    """
    valid = False
    privkey = 0
    while not valid:
        privkey = bitcoin.random_key()
        decoded_private_key = bitcoin.decode_privkey(privkey, 'hex')
        valid = 0 < decoded_private_key < bitcoin.N
    if compressed:
        privkey += '01'
    data = bytes([get_chain_params(polis_network).PREFIX_SECRET_KEY]) + bytes.fromhex(privkey)
    checksum = bitcoin.bin_dbl_sha256(data)[0:4]
    return base58.b58encode(data + checksum)


def privkey_to_pubkey(privkey):
    pub = bitcoin.privkey_to_pubkey(privkey)
    return pub


def num_to_varint(a):
    """
    Based on project: https://github.com/chaeplin/dashmnb
    """
    x = int(a)
    if x < 253:
        return x.to_bytes(1, byteorder='big')
    elif x < 65536:
        return int(253).to_bytes(1, byteorder='big') + x.to_bytes(2, byteorder='little')
    elif x < 4294967296:
        return int(254).to_bytes(1, byteorder='big') + x.to_bytes(4, byteorder='little')
    else:
        return int(255).to_bytes(1, byteorder='big') + x.to_bytes(8, byteorder='little')


def read_varint_from_buf(buffer, offset) -> typing.Tuple[int, int]:
    if (buffer[offset] < 0xfd):
        value_size = 1
        value = buffer[offset]
    elif (buffer[offset] == 0xfd):
        value_size = 3
        value = int.from_bytes(buffer[offset + 1: offset + 3], byteorder='little')
    elif (buffer[offset] == 0xfe):
        value_size = 5
        value = int.from_bytes(buffer[offset + 1: offset + 5], byteorder='little')
    elif (buffer[offset] == 0xff):
        value_size = 9
        value = int.from_bytes(buffer[offset + 1: offset + 9], byteorder='little')
    else:
        raise Exception("Invalid varint size")
    return value, value_size + offset


def read_varint_from_file(fptr: typing.BinaryIO) -> int:
    buffer = fptr.read(1)
    if (buffer[0] < 0xfd):
        value_size = 1
        value = buffer[0]
    elif (buffer[0] == 0xfd):
        value_size = 2
        buffer = fptr.read(value_size)
        value = int.from_bytes(buffer[0: 2], byteorder='little')
    elif (buffer[0] == 0xfe):
        value_size = 4
        buffer = fptr.read(value_size)
        value = int.from_bytes(buffer[0: 4], byteorder='little')
    elif (buffer[0] == 0xff):
        value_size = 8
        buffer = fptr.read(value_size)
        value = int.from_bytes(buffer[0: 8], byteorder='little')
    else:
        raise Exception("Invalid varint size")
    if value_size != len(buffer):
        raise ValueError('File end before read completed.')
    return value


def wif_to_privkey(wif_key: str, polis_network: str):
    """
    Based on project: https://github.com/chaeplin/dashmnb with some changes related to usage of bitcoin library.
    """
    privkey_encoded = base58.b58decode(wif_key).hex()
    wif_version = privkey_encoded[:2]
    wif_prefix = get_chain_params(polis_network).PREFIX_SECRET_KEY
    checksum = privkey_encoded[-8:]

    vs = bytes.fromhex(privkey_encoded[:-8])
    check = binascii.unhexlify(bitcoin.dbl_sha256(vs))[0:4]

    if wif_version == wif_prefix.to_bytes(1, byteorder='big').hex() and checksum == check.hex():
        privkey = privkey_encoded[2:-8]
        return privkey
    else:
        return None


def wif_privkey_to_uncompressed(wif_key: str):
    privkey_encoded = base58.b58decode(wif_key)
    if len(privkey_encoded) == 38 and privkey_encoded[33] == 0x01:
        # [1-byte prefix][32-byte privkey][optional 1-byte compression suffix][4-byte checksum]
        data = privkey_encoded[:33]
        checksum = bitcoin.bin_dbl_sha256(data)[0:4]
        return base58.b58encode(data + checksum)
    else:
        return wif_key


def privkey_valid(privkey):
    try:
        pk = bitcoin.decode_privkey(privkey, 'wif')
        pkbin = bytes.fromhex(bitcoin.encode_privkey(pk, 'hex'))
        if len(pkbin) == 32 or (len(pkbin) == 33 and pkbin[-1] == 1):
            return True
        else:
            return False
    except Exception as e:
        return False


def from_string_to_bytes(a):
    """
    Based on project: https://github.com/chaeplin/dashmnb.
    """
    return a if isinstance(a, bytes) else bytes(a, 'utf-8')


def electrum_sig_hash(message):
    """
    Based on project: https://github.com/chaeplin/dashmnb.
    """
    padded = b"\x19Polis Signed Message:\n" + \
        num_to_varint(len(message)) + from_string_to_bytes(message)
    return bitcoin.dbl_sha256(padded)


def ecdsa_sign(msg: str, wif_priv_key: str, polis_network: str):
    """Signs a message with the Elliptic Curve algorithm.
    Note: Polis core uses uncompressed public keys, so if the private key passed as an argument
    is of compressed format, convert it to an uncompressed
    """
    # wif_priv_key = wif_privkey_to_uncompressed(wif_priv_key)

    v, r, s = bitcoin.ecdsa_raw_sign(electrum_sig_hash(msg), wif_priv_key)
    sig = bitcoin.encode_sig(v, r, s)
    pubkey = bitcoin.privkey_to_pubkey(wif_to_privkey(wif_priv_key, polis_network))

    ok = bitcoin.ecdsa_raw_verify(electrum_sig_hash(msg), bitcoin.decode_sig(sig), pubkey)
    if not ok:
        raise Exception('Bad signature!')
    return sig


def serialize_input_str(tx, prevout_n, sequence, script_sig):
    """Based on project: https://github.com/chaeplin/dashmnb."""
    s = ['CTxIn(']
    s.append('COutPoint(%s, %s)' % (tx, prevout_n))
    s.append(', ')
    if tx == '00' * 32 and prevout_n == 0xffffffff:
        s.append('coinbase %s' % script_sig)
    else:
        script_sig2 = script_sig
        if len(script_sig2) > 24:
            script_sig2 = script_sig2[0:24]
        s.append('scriptSig=%s' % script_sig2)

    if sequence != 0xffffffff:
        s.append(', nSequence=%d' % sequence)
    s.append(')')
    return ''.join(s)


def bip32_path_n_to_string(path_n):
    ret = ''
    for elem in path_n:
        if elem >= 0x80000000:
            ret += ('/' if ret else '') + str(elem - 0x80000000) + "'"
        else:
            ret += ('/' if ret else '') + str(elem)
    return ret


def bip32_path_string_to_n(path_str):
    if path_str.startswith('m/'):
        path_str = path_str[2:]
    path_str = path_str.strip('/')
    elems = [int(elem[:-1]) + 0x80000000 if elem.endswith("'") else int(elem) for elem in path_str.split('/')]
    return elems


def compose_tx_locking_script(dest_address, polis_newtork: str):
    """
    Create a Locking script (ScriptPubKey) that will be assigned to a transaction output.
    :param dest_address: destination address in Base58Check format
    :return: sequence of opcodes and its arguments, defining logic of the locking script
    """

    pubkey_hash = bytearray.fromhex(bitcoin.b58check_to_hex(dest_address)) # convert address to a public key hash
    if len(pubkey_hash) != 20:
        raise Exception('Invalid length of the public key hash: ' + str(len(pubkey_hash)))

    if dest_address[0] in get_chain_params(polis_newtork).B58_PREFIXES_PUBKEY_ADDRESS:
        # sequence of opcodes/arguments for p2pkh (pay-to-public-key-hash)
        scr = OP_DUP + \
              OP_HASH160 + \
              int.to_bytes(len(pubkey_hash), 1, byteorder='little') + \
              pubkey_hash + \
              OP_EQUALVERIFY + \
              OP_CHECKSIG
    elif dest_address[0] in get_chain_params(polis_newtork).B58_PREFIXES_SCRIPT_ADDRESS:
        # sequence of opcodes/arguments for p2sh (pay-to-script-hash)
        scr = OP_HASH160 + \
              int.to_bytes(len(pubkey_hash), 1, byteorder='little') + \
              pubkey_hash + \
              OP_EQUAL
    else:
        raise Exception('Invalid dest address prefix: ' + dest_address[0])
    return scr


def extract_pkh_from_locking_script(script):
    if len(script) == 25:
        if script[0:1] == OP_DUP and script[1:2] == OP_HASH160:
            if read_varint_from_buf(script, 2)[0] == 20:
                return script[3:23]
            else:
                raise Exception('Non-standard public key hash length (should be 20)')
    raise Exception('Non-standard locking script type (should be P2PKH)')


class COutPoint(object):
    def __init__(self, hash: str, index: int):
        self.hash: bytes = bytes.fromhex(hash)
        self.index: int = index

    def serialize(self):
        ser_str = self.hash[::-1].hex()
        ser_str += int(self.index).to_bytes(4, byteorder='little').hex()
        return ser_str


class CTxIn(object):
    def __init__(self, prevout: COutPoint):
        self.prevout: COutPoint = prevout
        self.script = ''
        self.sequence = 0xffffffff

    def serialize(self):
        return self.prevout.serialize() + '00' + self.sequence.to_bytes(4, byteorder='little').hex()


class CMasternodePing(object):
    def __init__(self, mn_outpoint: COutPoint, block_hash, sig_time):
        self.mn_outpoint: COutPoint = mn_outpoint  # protocol >= 70209
        self.mn_tx_in = CTxIn(mn_outpoint)  # protocol <= 70208
        self.block_hash: str = block_hash
        self.sig_time: int = sig_time
        self.sig = None

    def sign_message(self, priv_key, polis_network):
        s = f'CTxIn(COutPoint({self.mn_outpoint.hash.hex()}, {self.mn_outpoint.index}), scriptSig=){self.block_hash}' \
            f'{str(self.sig_time)}'
        r = ecdsa_sign(s, priv_key, polis_network)
        self.sig = base64.b64decode(r)
        return self.sig

    def serialize(self, dest_node_version: int):
        if dest_node_version <= 70208:
            ser_str = self.mn_tx_in.serialize()
        else:
            ser_str = self.mn_outpoint.serialize()
        ser_str += bytes.fromhex(self.block_hash)[::-1].hex()
        ser_str += self.sig_time.to_bytes(8, byteorder='little').hex()
        ser_str += num_to_varint(len(self.sig)).hex() + self.sig.hex()
        return ser_str


class CMasternodeBroadcast(object):
    def __init__(self, mn_ip: str, mn_port: int, pubkey_collateral: bytes, pubkey_masternode: bytes,
                 collateral_tx: str, collateral_tx_index: int, block_hash: str, sig_time: int, protocol_version: int):
        self.mn_ip: str = mn_ip
        self.mn_port: int = mn_port
        self.pubkey_collateral: bytes = pubkey_collateral
        self.pubkey_masternode: bytes = pubkey_masternode
        self.sig = None
        self.sig_time: int = sig_time
        self.protocol_version: int = protocol_version
        self.collateral_outpoint = COutPoint(collateral_tx, int(collateral_tx_index))
        self.mn_ping: CMasternodePing = CMasternodePing(self.collateral_outpoint, block_hash, sig_time)

    def sign_message(self, collateral_bip32_path: str, hw_sign_message_fun: typing.Callable, hw_session,
                     mn_privkey_wif: str, polis_network: str):

        self.mn_ping.sign_message(mn_privkey_wif, polis_network)

        str_for_serialize = self.mn_ip + ':' + str(self.mn_port) + str(self.sig_time) + \
            binascii.unhexlify(bitcoin.hash160(self.pubkey_collateral))[::-1].hex() + \
            binascii.unhexlify(bitcoin.hash160(self.pubkey_masternode))[::-1].hex() + \
            str(self.protocol_version)

        self.sig = hw_sign_message_fun(hw_session, collateral_bip32_path, str_for_serialize)
        return self.sig

    def serialize(self, dest_node_version, protocol_version):
        if not self.sig:
            raise Exception('Message not signed.')

        if dest_node_version <= 70208:
            ser_str = self.mn_ping.mn_tx_in.serialize()
        else:
            ser_str = self.mn_ping.mn_outpoint.serialize()

        addr = '00000000000000000000ffff'
        ip_elems = map(int, self.mn_ip.split('.'))
        for i in ip_elems:
            addr += i.to_bytes(1, byteorder='big').hex()
        addr += int(self.mn_port).to_bytes(2, byteorder='big').hex()

        ser_str += addr
        ser_str += num_to_varint(len(self.pubkey_collateral)).hex() + self.pubkey_collateral.hex()
        ser_str += num_to_varint(len(self.pubkey_masternode)).hex() + self.pubkey_masternode.hex()
        ser_str += num_to_varint(len(self.sig.signature)).hex() + self.sig.signature.hex()
        ser_str += self.sig_time.to_bytes(8, byteorder='little').hex()
        ser_str += int(protocol_version).to_bytes(4, byteorder='little').hex()
        ser_str += self.mn_ping.serialize(dest_node_version)

        if dest_node_version == 70208:
            ser_str += '0001000100'

        return ser_str
