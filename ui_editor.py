# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(825, 550)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.main_hbox = QHBoxLayout()
        self.main_hbox.setObjectName(u"main_hbox")
        self.folderlist_vbox = QVBoxLayout()
        self.folderlist_vbox.setObjectName(u"folderlist_vbox")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.folder_label = QLabel(self.centralwidget)
        self.folder_label.setObjectName(u"folder_label")

        self.horizontalLayout_3.addWidget(self.folder_label)

        self.sort_mode_combo = QComboBox(self.centralwidget)
        self.sort_mode_combo.addItem("")
        self.sort_mode_combo.addItem("")
        self.sort_mode_combo.addItem("")
        self.sort_mode_combo.addItem("")
        self.sort_mode_combo.setObjectName(u"sort_mode_combo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sort_mode_combo.sizePolicy().hasHeightForWidth())
        self.sort_mode_combo.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.sort_mode_combo)

        self.open_folder_btn = QPushButton(self.centralwidget)
        self.open_folder_btn.setObjectName(u"open_folder_btn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.open_folder_btn.sizePolicy().hasHeightForWidth())
        self.open_folder_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.open_folder_btn)

        self.rename_folder_btn = QPushButton(self.centralwidget)
        self.rename_folder_btn.setObjectName(u"rename_folder_btn")
        sizePolicy1.setHeightForWidth(self.rename_folder_btn.sizePolicy().hasHeightForWidth())
        self.rename_folder_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.rename_folder_btn)


        self.folderlist_vbox.addLayout(self.horizontalLayout_3)

        self.folderlist = QListWidget(self.centralwidget)
        self.folderlist.setObjectName(u"folderlist")

        self.folderlist_vbox.addWidget(self.folderlist)


        self.main_hbox.addLayout(self.folderlist_vbox)

        self.buttons_vbox = QVBoxLayout()
        self.buttons_vbox.setObjectName(u"buttons_vbox")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.buttons_vbox.addItem(self.verticalSpacer_3)

        self.add_file_to_playlist_btn = QPushButton(self.centralwidget)
        self.add_file_to_playlist_btn.setObjectName(u"add_file_to_playlist_btn")

        self.buttons_vbox.addWidget(self.add_file_to_playlist_btn)

        self.add_to_playlist_btn = QPushButton(self.centralwidget)
        self.add_to_playlist_btn.setObjectName(u"add_to_playlist_btn")

        self.buttons_vbox.addWidget(self.add_to_playlist_btn)

        self.remove_from_playlist_btn = QPushButton(self.centralwidget)
        self.remove_from_playlist_btn.setObjectName(u"remove_from_playlist_btn")

        self.buttons_vbox.addWidget(self.remove_from_playlist_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.buttons_vbox.addItem(self.verticalSpacer)

        self.move_up_btn = QPushButton(self.centralwidget)
        self.move_up_btn.setObjectName(u"move_up_btn")

        self.buttons_vbox.addWidget(self.move_up_btn)

        self.move_down_btn = QPushButton(self.centralwidget)
        self.move_down_btn.setObjectName(u"move_down_btn")

        self.buttons_vbox.addWidget(self.move_down_btn)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.buttons_vbox.addItem(self.verticalSpacer_2)

        self.show_folder_list_cb = QCheckBox(self.centralwidget)
        self.show_folder_list_cb.setObjectName(u"show_folder_list_cb")

        self.buttons_vbox.addWidget(self.show_folder_list_cb)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.buttons_vbox.addItem(self.verticalSpacer_4)


        self.main_hbox.addLayout(self.buttons_vbox)

        self.playlist_vbox = QVBoxLayout()
        self.playlist_vbox.setObjectName(u"playlist_vbox")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.playlist_label = QLabel(self.centralwidget)
        self.playlist_label.setObjectName(u"playlist_label")

        self.horizontalLayout_4.addWidget(self.playlist_label)

        self.clear_btn = QPushButton(self.centralwidget)
        self.clear_btn.setObjectName(u"clear_btn")
        sizePolicy1.setHeightForWidth(self.clear_btn.sizePolicy().hasHeightForWidth())
        self.clear_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.clear_btn)

        self.open_playlist_btn = QPushButton(self.centralwidget)
        self.open_playlist_btn.setObjectName(u"open_playlist_btn")
        sizePolicy1.setHeightForWidth(self.open_playlist_btn.sizePolicy().hasHeightForWidth())
        self.open_playlist_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.open_playlist_btn)

        self.save_playlist_btn = QToolButton(self.centralwidget)
        self.save_playlist_btn.setObjectName(u"save_playlist_btn")
        sizePolicy1.setHeightForWidth(self.save_playlist_btn.sizePolicy().hasHeightForWidth())
        self.save_playlist_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.save_playlist_btn)


        self.playlist_vbox.addLayout(self.horizontalLayout_4)

        self.playlist = QListWidget(self.centralwidget)
        self.playlist.setObjectName(u"playlist")

        self.playlist_vbox.addWidget(self.playlist)


        self.main_hbox.addLayout(self.playlist_vbox)


        self.verticalLayout_3.addLayout(self.main_hbox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 825, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.folder_label.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.sort_mode_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Sort by Title (\u2193)", None))
        self.sort_mode_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"Sort by Title (\u2191)", None))
        self.sort_mode_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"Sort By Artist (\u2193)", None))
        self.sort_mode_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"Sort by Artist (\u2191)", None))

        self.open_folder_btn.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.rename_folder_btn.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.add_file_to_playlist_btn.setText(QCoreApplication.translate("MainWindow", u"Add file to playlist", None))
        self.add_to_playlist_btn.setText(QCoreApplication.translate("MainWindow", u"Add selected to playlist", None))
        self.remove_from_playlist_btn.setText(QCoreApplication.translate("MainWindow", u"Remove from playlist", None))
        self.move_up_btn.setText(QCoreApplication.translate("MainWindow", u"Move up", None))
        self.move_down_btn.setText(QCoreApplication.translate("MainWindow", u"Move down", None))
        self.show_folder_list_cb.setText(QCoreApplication.translate("MainWindow", u"Show Folder List", None))
        self.playlist_label.setText(QCoreApplication.translate("MainWindow", u"Playlist", None))
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.open_playlist_btn.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.save_playlist_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

