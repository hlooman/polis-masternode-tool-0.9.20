# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/blogin/PycharmProjects/PMT-git/src/ui/ui_send_payout_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SendPayoutDlg(object):
    def setupUi(self, SendPayoutDlg):
        SendPayoutDlg.setObjectName("SendPayoutDlg")
        SendPayoutDlg.resize(832, 507)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SendPayoutDlg.sizePolicy().hasHeightForWidth())
        SendPayoutDlg.setSizePolicy(sizePolicy)
        SendPayoutDlg.setSizeGripEnabled(True)
        SendPayoutDlg.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SendPayoutDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pnl_input = QtWidgets.QWidget(SendPayoutDlg)
        self.pnl_input.setObjectName("pnl_input")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pnl_input)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lay_input = QtWidgets.QHBoxLayout()
        self.lay_input.setSpacing(8)
        self.lay_input.setObjectName("lay_input")
        self.label_3 = QtWidgets.QLabel(self.pnl_input)
        self.label_3.setObjectName("label_3")
        self.lay_input.addWidget(self.label_3)
        self.cbo_address_source_mode = QtWidgets.QComboBox(self.pnl_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbo_address_source_mode.sizePolicy().hasHeightForWidth())
        self.cbo_address_source_mode.setSizePolicy(sizePolicy)
        self.cbo_address_source_mode.setMinimumSize(QtCore.QSize(0, 0))
        self.cbo_address_source_mode.setMaximumSize(QtCore.QSize(160, 16777215))
        self.cbo_address_source_mode.setObjectName("cbo_address_source_mode")
        self.cbo_address_source_mode.addItem("")
        self.cbo_address_source_mode.addItem("")
        self.cbo_address_source_mode.addItem("")
        self.lay_input.addWidget(self.cbo_address_source_mode)
        self.sw_address_source = QtWidgets.QStackedWidget(self.pnl_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sw_address_source.sizePolicy().hasHeightForWidth())
        self.sw_address_source.setSizePolicy(sizePolicy)
        self.sw_address_source.setObjectName("sw_address_source")
        self.wdg_address_source_1 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wdg_address_source_1.sizePolicy().hasHeightForWidth())
        self.wdg_address_source_1.setSizePolicy(sizePolicy)
        self.wdg_address_source_1.setObjectName("wdg_address_source_1")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.wdg_address_source_1)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lbl_account = QtWidgets.QLabel(self.wdg_address_source_1)
        self.lbl_account.setObjectName("lbl_account")
        self.horizontalLayout_6.addWidget(self.lbl_account)
        self.cbo_hw_account_nr = QtWidgets.QComboBox(self.wdg_address_source_1)
        self.cbo_hw_account_nr.setObjectName("cbo_hw_account_nr")
        self.horizontalLayout_6.addWidget(self.cbo_hw_account_nr)
        self.btn_add_hw_account_nr = QtWidgets.QToolButton(self.wdg_address_source_1)
        self.btn_add_hw_account_nr.setObjectName("btn_add_hw_account_nr")
        self.horizontalLayout_6.addWidget(self.btn_add_hw_account_nr)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.lbl_hw_account_base_path = QtWidgets.QLabel(self.wdg_address_source_1)
        self.lbl_hw_account_base_path.setObjectName("lbl_hw_account_base_path")
        self.horizontalLayout_6.addWidget(self.lbl_hw_account_base_path)
        self.sw_address_source.addWidget(self.wdg_address_source_1)
        self.wdg_address_source_2 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wdg_address_source_2.sizePolicy().hasHeightForWidth())
        self.wdg_address_source_2.setSizePolicy(sizePolicy)
        self.wdg_address_source_2.setObjectName("wdg_address_source_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.wdg_address_source_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblSourceBip32Path = QtWidgets.QLabel(self.wdg_address_source_2)
        self.lblSourceBip32Path.setObjectName("lblSourceBip32Path")
        self.horizontalLayout_2.addWidget(self.lblSourceBip32Path)
        self.edt_src_bip32_path = QtWidgets.QLineEdit(self.wdg_address_source_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edt_src_bip32_path.sizePolicy().hasHeightForWidth())
        self.edt_src_bip32_path.setSizePolicy(sizePolicy)
        self.edt_src_bip32_path.setMaximumSize(QtCore.QSize(100, 16777215))
        self.edt_src_bip32_path.setStyleSheet("background-color: lightgray;")
        self.edt_src_bip32_path.setReadOnly(True)
        self.edt_src_bip32_path.setObjectName("edt_src_bip32_path")
        self.horizontalLayout_2.addWidget(self.edt_src_bip32_path)
        self.btn_src_bip32_path = QtWidgets.QToolButton(self.wdg_address_source_2)
        self.btn_src_bip32_path.setObjectName("btn_src_bip32_path")
        self.horizontalLayout_2.addWidget(self.btn_src_bip32_path)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.sw_address_source.addWidget(self.wdg_address_source_2)
        self.wdg_address_source_3 = QtWidgets.QWidget()
        self.wdg_address_source_3.setObjectName("wdg_address_source_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.wdg_address_source_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_src_masternode = QtWidgets.QLabel(self.wdg_address_source_3)
        self.lbl_src_masternode.setObjectName("lbl_src_masternode")
        self.horizontalLayout.addWidget(self.lbl_src_masternode)
        self.cbo_src_masternodes = QtWidgets.QComboBox(self.wdg_address_source_3)
        self.cbo_src_masternodes.setObjectName("cbo_src_masternodes")
        self.horizontalLayout.addWidget(self.cbo_src_masternodes)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.sw_address_source.addWidget(self.wdg_address_source_3)
        self.lay_input.addWidget(self.sw_address_source)
        self.btnLoadTransactions = QtWidgets.QPushButton(self.pnl_input)
        self.btnLoadTransactions.setAutoDefault(False)
        self.btnLoadTransactions.setObjectName("btnLoadTransactions")
        self.lay_input.addWidget(self.btnLoadTransactions)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lay_input.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.lay_input)
        self.verticalLayout.addWidget(self.pnl_input)
        self.splitter = QtWidgets.QSplitter(SendPayoutDlg)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.main_widget = QtWidgets.QWidget(self.splitter)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_message_2 = QtWidgets.QLabel(self.main_widget)
        self.lbl_message_2.setText("")
        self.lbl_message_2.setOpenExternalLinks(True)
        self.lbl_message_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lbl_message_2.setObjectName("lbl_message_2")
        self.verticalLayout_2.addWidget(self.lbl_message_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 8, -1, -1)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnCheckAll = QtWidgets.QToolButton(self.main_widget)
        self.btnCheckAll.setToolTip("")
        self.btnCheckAll.setIconSize(QtCore.QSize(12, 12))
        self.btnCheckAll.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btnCheckAll.setObjectName("btnCheckAll")
        self.horizontalLayout_4.addWidget(self.btnCheckAll)
        self.btnUncheckAll = QtWidgets.QToolButton(self.main_widget)
        self.btnUncheckAll.setToolTip("")
        self.btnUncheckAll.setIconSize(QtCore.QSize(12, 12))
        self.btnUncheckAll.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btnUncheckAll.setObjectName("btnUncheckAll")
        self.horizontalLayout_4.addWidget(self.btnUncheckAll)
        self.chbHideCollateralTx = QtWidgets.QCheckBox(self.main_widget)
        self.chbHideCollateralTx.setStyleSheet("")
        self.chbHideCollateralTx.setObjectName("chbHideCollateralTx")
        self.horizontalLayout_4.addWidget(self.chbHideCollateralTx)
        self.lbl_message = QtWidgets.QLabel(self.main_widget)
        self.lbl_message.setStyleSheet("margin-left:20px;\n"
"font-size:11px;\n"
"background-color: rgb(56, 181, 255);\n"
"color: rgb(255, 255, 255);")
        self.lbl_message.setWordWrap(False)
        self.lbl_message.setOpenExternalLinks(True)
        self.lbl_message.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lbl_message.setObjectName("lbl_message")
        self.horizontalLayout_4.addWidget(self.lbl_message)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.tableView = QtWidgets.QTableView(self.main_widget)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setShowGrid(True)
        self.tableView.setSortingEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setCascadingSectionResizes(True)
        self.tableView.verticalHeader().setHighlightSections(False)
        self.verticalLayout_2.addWidget(self.tableView)
        self.dest_widget1 = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dest_widget1.sizePolicy().hasHeightForWidth())
        self.dest_widget1.setSizePolicy(sizePolicy)
        self.dest_widget1.setObjectName("dest_widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dest_widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.dest_widget = QtWidgets.QFrame(self.dest_widget1)
        self.dest_widget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dest_widget.setObjectName("dest_widget")
        self.verticalLayout_3.addWidget(self.dest_widget)
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.btnSend = QtWidgets.QPushButton(SendPayoutDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSend.sizePolicy().hasHeightForWidth())
        self.btnSend.setSizePolicy(sizePolicy)
        self.btnSend.setMinimumSize(QtCore.QSize(200, 0))
        self.btnSend.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnSend.setAutoDefault(False)
        self.btnSend.setObjectName("btnSend")
        self.horizontalLayout_3.addWidget(self.btnSend)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.btnClose = QtWidgets.QPushButton(SendPayoutDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QtCore.QSize(0, 0))
        self.btnClose.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnClose.setAutoDefault(False)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout_3.addWidget(self.btnClose, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(SendPayoutDlg)
        self.sw_address_source.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(SendPayoutDlg)

    def retranslateUi(self, SendPayoutDlg):
        _translate = QtCore.QCoreApplication.translate
        SendPayoutDlg.setWindowTitle(_translate("SendPayoutDlg", "Dialog"))
        self.label_3.setText(_translate("SendPayoutDlg", "View as"))
        self.cbo_address_source_mode.setItemText(0, _translate("SendPayoutDlg", "Wallet Account"))
        self.cbo_address_source_mode.setItemText(1, _translate("SendPayoutDlg", "BIP32 Path"))
        self.cbo_address_source_mode.setItemText(2, _translate("SendPayoutDlg", "Masternode Address"))
        self.lbl_account.setText(_translate("SendPayoutDlg", "Account  "))
        self.btn_add_hw_account_nr.setToolTip(_translate("SendPayoutDlg", "Add new account number"))
        self.btn_add_hw_account_nr.setText(_translate("SendPayoutDlg", "."))
        self.lbl_hw_account_base_path.setText(_translate("SendPayoutDlg", "..."))
        self.lblSourceBip32Path.setText(_translate("SendPayoutDlg", "BIP32 path"))
        self.btn_src_bip32_path.setToolTip(_translate("SendPayoutDlg", "Change BIP32 path"))
        self.btn_src_bip32_path.setText(_translate("SendPayoutDlg", "..."))
        self.lbl_src_masternode.setText(_translate("SendPayoutDlg", "Masternode"))
        self.btnLoadTransactions.setText(_translate("SendPayoutDlg", "Reload"))
        self.btnCheckAll.setText(_translate("SendPayoutDlg", "Select All"))
        self.btnUncheckAll.setText(_translate("SendPayoutDlg", "Unselect All"))
        self.chbHideCollateralTx.setText(_translate("SendPayoutDlg", "Hide collateral utxos"))
        self.lbl_message.setText(_translate("SendPayoutDlg", "...."))
        self.btnSend.setText(_translate("SendPayoutDlg", "Prepare Transaction"))
        self.btnClose.setText(_translate("SendPayoutDlg", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SendPayoutDlg = QtWidgets.QDialog()
    ui = Ui_SendPayoutDlg()
    ui.setupUi(SendPayoutDlg)
    SendPayoutDlg.show()
    sys.exit(app.exec_())

