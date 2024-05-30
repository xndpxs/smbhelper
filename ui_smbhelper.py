# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'smbhelper_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_SMBWindow(object):
    def setupUi(self, SMBWindow):
        if not SMBWindow.objectName():
            SMBWindow.setObjectName(u"SMBWindow")
        SMBWindow.resize(852, 486)
        self.actionQuit = QAction(SMBWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionAbout = QAction(SMBWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(SMBWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.button_apply = QPushButton(self.centralwidget)
        self.button_apply.setObjectName(u"button_apply")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_apply.sizePolicy().hasHeightForWidth())
        self.button_apply.setSizePolicy(sizePolicy)
        self.button_apply.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.button_apply, 1, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_search = QPushButton(self.centralwidget)
        self.button_search.setObjectName(u"button_search")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy1)
        self.button_search.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.button_search, 0, 2, 1, 1)

        self.label_password = QLabel(self.centralwidget)
        self.label_password.setObjectName(u"label_password")

        self.gridLayout.addWidget(self.label_password, 1, 3, 1, 1)

        self.line_samba_domain = QLineEdit(self.centralwidget)
        self.line_samba_domain.setObjectName(u"line_samba_domain")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_samba_domain.sizePolicy().hasHeightForWidth())
        self.line_samba_domain.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.line_samba_domain, 2, 4, 1, 1)

        self.label_smb_share = QLabel(self.centralwidget)
        self.label_smb_share.setObjectName(u"label_smb_share")

        self.gridLayout.addWidget(self.label_smb_share, 2, 0, 1, 1)

        self.line_samba_ip = QLineEdit(self.centralwidget)
        self.line_samba_ip.setObjectName(u"line_samba_ip")

        self.gridLayout.addWidget(self.line_samba_ip, 1, 1, 1, 2)

        self.label_domain = QLabel(self.centralwidget)
        self.label_domain.setObjectName(u"label_domain")

        self.gridLayout.addWidget(self.label_domain, 2, 3, 1, 1)

        self.label_smb_ip = QLabel(self.centralwidget)
        self.label_smb_ip.setObjectName(u"label_smb_ip")

        self.gridLayout.addWidget(self.label_smb_ip, 1, 0, 1, 1)

        self.line_samba_user = QLineEdit(self.centralwidget)
        self.line_samba_user.setObjectName(u"line_samba_user")
        sizePolicy2.setHeightForWidth(self.line_samba_user.sizePolicy().hasHeightForWidth())
        self.line_samba_user.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.line_samba_user, 0, 4, 1, 1)

        self.label_folder = QLabel(self.centralwidget)
        self.label_folder.setObjectName(u"label_folder")

        self.gridLayout.addWidget(self.label_folder, 0, 0, 1, 1)

        self.line_samba_share = QLineEdit(self.centralwidget)
        self.line_samba_share.setObjectName(u"line_samba_share")
        sizePolicy2.setHeightForWidth(self.line_samba_share.sizePolicy().hasHeightForWidth())
        self.line_samba_share.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.line_samba_share, 2, 1, 1, 2)

        self.label_user = QLabel(self.centralwidget)
        self.label_user.setObjectName(u"label_user")

        self.gridLayout.addWidget(self.label_user, 0, 3, 1, 1)

        self.line_samba_pass = QLineEdit(self.centralwidget)
        self.line_samba_pass.setObjectName(u"line_samba_pass")
        sizePolicy2.setHeightForWidth(self.line_samba_pass.sizePolicy().hasHeightForWidth())
        self.line_samba_pass.setSizePolicy(sizePolicy2)
        self.line_samba_pass.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.line_samba_pass, 1, 4, 1, 1)

        self.line_local_folder = QLineEdit(self.centralwidget)
        self.line_local_folder.setObjectName(u"line_local_folder")
        sizePolicy2.setHeightForWidth(self.line_local_folder.sizePolicy().hasHeightForWidth())
        self.line_local_folder.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.line_local_folder, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.text_edit = QTextEdit(self.centralwidget)
        self.text_edit.setObjectName(u"text_edit")
        self.text_edit.setReadOnly(True)

        self.verticalLayout.addWidget(self.text_edit)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 3)

        self.button_cancel = QPushButton(self.centralwidget)
        self.button_cancel.setObjectName(u"button_cancel")
        sizePolicy.setHeightForWidth(self.button_cancel.sizePolicy().hasHeightForWidth())
        self.button_cancel.setSizePolicy(sizePolicy)
        self.button_cancel.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.button_cancel, 1, 1, 1, 1)

        SMBWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SMBWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 852, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        SMBWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SMBWindow)
        self.statusbar.setObjectName(u"statusbar")
        SMBWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_local_folder, self.button_search)
        QWidget.setTabOrder(self.button_search, self.line_samba_ip)
        QWidget.setTabOrder(self.line_samba_ip, self.line_samba_share)
        QWidget.setTabOrder(self.line_samba_share, self.line_samba_user)
        QWidget.setTabOrder(self.line_samba_user, self.line_samba_pass)
        QWidget.setTabOrder(self.line_samba_pass, self.line_samba_domain)
        QWidget.setTabOrder(self.line_samba_domain, self.text_edit)
        QWidget.setTabOrder(self.text_edit, self.button_cancel)
        QWidget.setTabOrder(self.button_cancel, self.button_apply)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(SMBWindow)

        QMetaObject.connectSlotsByName(SMBWindow)
    # setupUi

    def retranslateUi(self, SMBWindow):
        SMBWindow.setWindowTitle(QCoreApplication.translate("SMBWindow", u"SMBHelper", None))
        self.actionQuit.setText(QCoreApplication.translate("SMBWindow", u"Quit", None))
        self.actionAbout.setText(QCoreApplication.translate("SMBWindow", u"About", None))
        self.button_apply.setText(QCoreApplication.translate("SMBWindow", u"Apply", None))
        self.button_search.setText(QCoreApplication.translate("SMBWindow", u"Search", None))
        self.label_password.setText(QCoreApplication.translate("SMBWindow", u"Samba Password:", None))
        self.label_smb_share.setText(QCoreApplication.translate("SMBWindow", u"Samba Server Share Name: ", None))
        self.label_domain.setText(QCoreApplication.translate("SMBWindow", u"Samba Domain: ", None))
        self.label_smb_ip.setText(QCoreApplication.translate("SMBWindow", u"Samba Server IP Address: ", None))
        self.label_folder.setText(QCoreApplication.translate("SMBWindow", u"Local Folder Address: ", None))
        self.label_user.setText(QCoreApplication.translate("SMBWindow", u"Samba Username:", None))
        self.button_cancel.setText(QCoreApplication.translate("SMBWindow", u"Quit", None))
        self.menuFile.setTitle(QCoreApplication.translate("SMBWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("SMBWindow", u"Help", None))
    # retranslateUi

