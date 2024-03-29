# Polis Masternode Tool (PMT) - based on Dash Masternode Tool version 0.19 by Bertrand256

## Contents

 * [Masternodes](#masternodes)
 * [Polis Masternode Tool](#polis-masternode-tool)
   * [Feature list](#feature-list)
   * [Supported hardware wallets](#supported-hardware-wallets)
 * [Configuration](#configuration)
   * [Setting up the hardware wallet type](#setting-up-the-hardware-wallet-type)
   * [Connection setup](#connection-setup)
     * [Connection to a local node](doc/config-connection-direct.md)
     * [Connection to a remote node through an SSH tunnel](doc/config-connection-ssh.md)
     * [Connection to "public" JSON-RPC nodes](doc/config-connection-proxy.md)
   * [Masternode setup](#masternode-setup)
     * [Scenario A: moving masternode management from Polis Core](doc/config-masternodes-a.md)
     * [Scenario B: configuring a new masternode](doc/config-masternodes-b.md)
   * [Command line parameters](#command-line-parameters)
 * [Features](#features)
   * [Starting a masternode](#starting-a-masternode)
   * [Transferring masternode earnings](#transferring-masternode-earnings)
   * [Signing messages with a hardware wallet](#signing-messages-with-a-hardware-wallet)
   * [Changing a hardware wallet PIN/passphrase](#changing-a-hardware-wallet-pinpassphrase)
   * [Browsing and voting on proposals](doc/proposals.md)
   * [Hardware wallet initialization/recovery](doc/hw-initialization-recovery.md)
     * [Updating hardware wallet firmware](doc/hw-initr-update-firmware.md)
 * Building the PMT executables
    * [macOS](doc/build-pmt-mac.md)
    * [Windows](doc/build-pmt-windows.md)
    * Linux
       * [Ubuntu](doc/build-pmt-linux-ubuntu.md)
       * [Fedora](doc/build-pmt-linux-fedora.md)
 * [Downloads](https://github.com/Bertrand256/polis-masternode-tool/releases/latest)
 * [Changelog](changelog.md)

## Masternodes

Polis masternodes are full nodes which are incentivized by receiving a share of the block reward as payment in return for the tasks they perform for the network, of which the most important include participation in *InstantSend* and *PrivateSend* transactions. In order to run a masternode, apart from setting up a server which runs the software, you must dedicate 1000 Polis as *collateral*, which is *"tied up"* in your node as long as you want it to be considered a masternode by the network. It is worth mentioning that the private key controlling the funds can (and for security reasons, should) be kept separately from the masternode server itself.

A server with the Polis daemon software installed will operate as a Polis full node, but before the rest of the network accepts it as a legitimate masternode, one more thing must happen: the person controlling the node must prove that they are also in control of the private key to the node's 1000 Polis *collateral*. This is achieved by sending a special message to the network (`start masternode` message), signed by this private key.

This action can be carried out using the *Polis Core* reference software client. As can be expected, this requires sending 1000 Polis to an address controlled by the *Polis Core* wallet. After the recent increase in the value of Polis and a burst in the amount of malware distributed over the Internet, you do not have to be paranoid to conclude that keeping large amounts of funds in a software wallet is not the most secure option. For these reasons, it is highly recommended to use a **hardware wallet** for this purpose.

# Polis Masternode Tool

The main purpose of the application is to give masternode operators (MNOs) the ability to send the `start masternode` command through an easy to use a graphical user interface if the masternode collateral is controlled by a Trezor hardware wallet.

## Feature list

* Sending the `start masternode` command if the collateral is controlled by a hardware wallet
* Transferring masternode earnings safely, without touching the 1000 Polis funding transaction
* Signing messages with a hardware wallet
* Voting on proposals
* Initialization/recovery of hardware wallets seeds

## Supported hardware wallets

- [x] Trezor (model One and T)

Most of the application features are accessible from the main program window:  
![Main window](doc/img/pmt-main-window.png)

# Configuration

## Setting up the hardware wallet type
 * Click the `Configure` button.
 * Select the `Miscellaneous` tab in the configuration dialog that appears.

## Connection setup

Most of the application features involve exchanging data between the application itself and the Polis network. To do this, *PMT* needs to connect to one of the full nodes on the network, specifically one which can handle JSON-RPC requests. This node plays the role of a gateway for *PMT* to the Polis network. It does not matter which full node node provides the service, because all nodes reach consensus by synchronizing information between each other on the Polis network.

Depending on your preferences (and skills) you can choose one of three possible connection types:
 * [Direct connection to a local node](doc/config-connection-direct.md), for example to *Polis Core* running on your normal computer.
 * [Connection to a remote node through an SSH tunnel](doc/config-connection-ssh.md), if you want to work with a remote Polis daemon (like your masternode) through an SSH tunnel.
 * [Connection to "public" JSON-RPC nodes](doc/config-connection-proxy.md), if you want to use nodes provided by other users.

## Masternode setup

Here we make the following assumptions:
  * You already have a server running the Polis daemon software (*polisd*) that you want to use as a masternode.
  * We occasionally refer to the *polisd* configuration file, so it is assumed that *polisd* is running under a Linux operating system (OS), which is the most popular and recommended OS for this purpose.
  * Your server has a public IP address that will be visible on the Internet.
  * You have set up a TCP port on which your *polisd* listens for incoming connections (usually 24126).

Further configuration steps depend on whether you already have a masternode controlled by *Polis Core* which you want to migrate to a hardware wallet managed by *PMT*, or if you are setting up a new masternode.

[Scenario A - moving masternode management from Polis Core](doc/config-masternodes-a.md)  
[Scenario B - configuration of a new masternode](doc/config-masternodes-b.md)

## Command line parameters

The application currently supports the following command-line parameters:
* `--data-dir`: a path to a directory in which the application will create all the needed files, such as: configuration file, cache and log files; it can be useful for users who want to avoid leaving any of the application files on the computer - which by default are created in the user's home directory - and insted to keep them on an external drive
* `--config`: a non-standard path to a configuration file. Example:
  `PolisMasternodeTool.exe --config=C:\pmt-configs\config1.ini`



# Features

## Starting a masternode

Once you set up the Polis daemon and perform the required *PMT* configuration, you need to broadcast the `start masternode` message to the Polis network, so the other Polis nodes recognize your daemon as a masternode and add it to the payment queue.

To do this, click the `Start Masternode using Hardware wallet` button.

### Sequence of actions

This section describes the steps taken by the application while starting the masternode, and possible errors that may occur during the process.

The steps are as follows:

1. Verification that all the required fields are filled with correct values. These fields are: `IP`, `port`, `MN private key`, `Collateral`, `Collateral TX ID` and `TX index`.
  An example message in case of errors:  
  ![Invalid collateral transaction id](doc/img/startmn-fields-validation-error.png)

2. Opening a connection to the Polis network and verifying if the Polis daemon to which it is connected is not still waiting for synchronization to complete.
  Message in case of failure:  
  ![Polis daemon synchronizing](doc/img/startmn-synchronize-warning.png)

3. Verification that the masternode status is not already `ENABLED` or `PRE_ENABLED`. If it is, the following warning appears:  
  ![Warning: masternode state is enabled](doc/img/startmn-state-warning.png)  
  If your masternode is running and you decide to send a `start masternode` message anyway, your masternode's payment queue position will be reset.

4. Opening a connection to the hardware wallet. Message in case of failure:  
  ![Cannot find Trezor device](doc/img/startmn-hw-error.png)

5. If the `BIP32 path` value is empty, *PMT* uses the *collateral address* to read the BIP32 path from the hardware wallet.

6. Retrieving the Polis address from the hardware wallet for the `BIP32 path` specified in the configuration. If it differs from the collateral address provided in the configuration, the following warning appears:  
  ![Polis address mismatch](doc/img/startmn-addr-mismatch-warning.png)  
  The most common reason for this error is mistyping the hardware wallet passphrase. Remember that different passphrases result in different Polis addresses for the same BIP32 path.

7. Verification that the specified transaction ID exists, points to your collateral address, is unspent and is equal to exactly 1000 Polis. Messages in case of failure:  
  ![Could not find the specified transaction id](doc/img/startmn-tx-warning.png)  
  ![Collateral transaction output should equal 1000 Polis](doc/img/startmn-collateral-warning.png)  
  If you decide to continue anyway, you probably won't be able to successfully start your masternode.

8. Verification at the Polis network level that the specified transaction ID is valid. Message in case of failure:  
  ![Masternode broadcast message decode failed](doc/img/startmn-incorrect-tx-error.png)

9. After completing all pre-verification, the application will ask you whether you want to continue:  
  ![Press OK to broadcast transaction](doc/img/startmn-broadcast-query.png)  
  This is the last chance to stop the process.

10. Sending the `start masternode` message. Success returns the following message:  
  ![Successfully relayed broadcast message](doc/img/startmn-success.png)  
  In case of failure, the message text may vary, depending on the nature of the problem. Example:  
  ![Failed to start masternode](doc/img/startmn-failed-error.png)

## Transferring masternode earnings

PMT version 0.9.4 and above allows you to transfer your masternode earnings. Unlike other Polis wallets, PMT gives you a 100% control over which *unspent transaction outputs* (utxo) you want to transfer. This has the same effect as the `Coin control` functionality implemented in the *Polis Core* wallet.

The `Transfer funds` window shows all *UTXOs* of the currently selected Masternode (mode 1), all Masternodes in current configuration (mode 2) or any address controlled by a hardware wallet (mode 3). All *UTXOs* not used as collateral are initially selected. All collateral *UTXOs* (1000 Polis) are initially hidden to avoid unintentionally spending collateral funds and thus breaking MN. You can show these hidden entries by unchecking the `Hide collateral utxos` option.

To show the `Transfer funds` window, click the `Tools` menu. Then, from the popup menu choose:
 * `Transfer funds from current Masternode's address` (mode 1)
 * `Transfer funds from all Masternodes addresses` (mode 2)
 * `Transfer funds from any address` (mode 3)

The same you can achieve by clicking of the three buttons from the right side of the app's toolbar:
![Transfer masternode funds window](doc/img/pmt-transfer-funds-tool-buttons.png)

Transferring funds from masternode collateral addresses (mode 2):  
![Transfer masternode funds window](doc/img/pmt-transfer-funds.png)

Transferring funds from any address controlled by a hardware wallet, using BIP32 path as an input (mode 3):  
![Transfer funds from any address window](doc/img/pmt-transfer-funds-any-address.png)

and using *wallet account* as an input (mode 3):  
![Transfer funds from any address window](doc/img/pmt-transfer-funds-any-address-account.png)

> Important: rows with a red font in the *Confirmations* column and a gray background are related to so-called *coinbase* transactions, that don't have the required number of confirmations to forward them. You should restrain from sending them and wait for them to receive at least 100 confirmations.

To send funds, select all *UTXOs* you wish to include in your transaction, enter the details of the recipient(s), verify the transaction fee and click the `Prepare Transaction` button on the bottom:
![Broadcast signed transaction confirmation](doc/img/pmt-transfer-funds-select-utxos.png)

After signing the transaction with your hardware wallet, the application will display a summary and will ask you for confirmation for broadcasting the signed transaction to the Polis network.  
![Broadcast signed transaction confirmation](doc/img/pmt-transfer-funds-broadcast.png)

After clicking `Send Transaction`, the application broadcasts the transaction and then shows a confirmation with a transaction ID as a hyperlink directing to a Polis block explorer:  
![Transaction sent](doc/img/pmt-transfer-funds-confirmation.png)

## Signing messages with a hardware wallet

To sign a message with your hardware wallet, click the `Tools` button and then select the `Sign message with HW for current Masternode's address` menu item. The `Sign message` window appears:  
![Sign message window](doc/img/pmt-hw-sign-message.png)

## Changing hardware wallet PIN/passphrase

Click the `Tools` button and select the `Hardware wallet PIN/Passphrase configuration` item. The following window will appear to guide you through the steps of changing the PIN/passphrase:  
![Hardware wallet setup window](doc/img/pmt-hardware-wallet-config.png)

## Downloads

This application is written in Python 3, but requires several additional libraries to run. These libraries in turn require the installation of a C++ compiler. All in all, compiling PMT from source is not trivial for non-technical people, especially the steps carried out under Linux (though this will be documented soon).

For this reason, in addition to providing the source code on GitHub, binary versions for all three major operating systems - macOS, Windows (32 and 64-bit) and Linux - are available for download directly. The binaries are compiled and tested under the following OS distributions:
* Windows 7 64-bit
* macOS 10.13.2 High Sierra
* Linux Debian Jessie

Binary versions of the latest release can be downloaded from: https://github.com/hlooman/polis-masternode-tool/releases/latest.
