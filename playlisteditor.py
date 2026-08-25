#  Copyright (C) 2026  leonhardw
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (QApplication, QAbstractItemView, QMainWindow, QListWidgetItem,
                               QHeaderView, QFileDialog, QMessageBox, QDialog, QHBoxLayout, QLineEdit,
                               QVBoxLayout, QLabel, QDialogButtonBox, QTableWidget, QTableWidgetItem,
                               QPushButton)

from song_manager import load_m3u, get_song_metadata, save_as_m3u, batch_rename
from ui_editor import Ui_MainWindow


class PlaylistEditor(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Playlist Editor')
        
        self.icon_size = 32
        
        self.playlist_opened = False
        self.current_folderlist = None
        self.folder_metadata = None
        
        self.playlist.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.playlist.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.playlist.setDropIndicatorShown(True)
        
        self.folderlist.setIconSize(QSize(self.icon_size, self.icon_size))
        self.playlist.setIconSize(QSize(self.icon_size, self.icon_size))
        
        self.folderlist.setDragDropMode(QAbstractItemView.DragOnly)
        self.folderlist.setAutoScroll(False)
        
        self.show_folder_list_cb.toggled.connect(self.show_folder_list)
        self.show_folder_list(False)
        
        self.open_folder_btn.clicked.connect(self.open_folder)
        
        self.open_playlist_btn.clicked.connect(self.open_playlist)
        self.save_playlist_btn.clicked.connect(self.save_playlist)
        self.clear_btn.clicked.connect(self.clear_playlist)
        
        self.move_up_btn.clicked.connect(self.move_up)
        self.move_down_btn.clicked.connect(self.move_down)
        self.add_to_playlist_btn.clicked.connect(self.add_to_playlist)
        self.add_file_to_playlist_btn.clicked.connect(self.add_file_to_playlist)
        self.remove_from_playlist_btn.clicked.connect(self.remove_from_playlist)
        self.rename_folder_btn.clicked.connect(self.rename)
        self.sort_mode_combo.currentIndexChanged.connect(self.change_sort_mode)
        
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(lambda: AboutDialog(self).exec())
        
        self.remove_from_playlist_btn.setEnabled(False)
        self.save_playlist_btn.setEnabled(False)
        
        self.add_to_playlist_btn.setEnabled(False)
        self.rename_folder_btn.setEnabled(False)
        self.sort_mode_combo.setEnabled(False)
        
        self._original_playlist_drop = self.playlist.dropEvent
        self.playlist.dropEvent = self.custom_drop_event
        self.playlist.itemSelectionChanged.connect(self.check_move_buttons)
    
    def custom_drop_event(self, event):
        self._original_playlist_drop(event)
        self.handle_size_dependent_buttons()
    
    def show_folder_list(self, state):
        if state:  # show
            self.set_layout_visibility(self.folderlist_vbox, True)
            self.main_hbox.removeItem(self.playlist_vbox)
            self.main_hbox.addLayout(self.playlist_vbox)
            if self.folderlist.count() > 0:
                self.add_to_playlist_btn.setEnabled(True)
        else:  # hide
            self.set_layout_visibility(self.folderlist_vbox, False)
            self.main_hbox.removeItem(self.buttons_vbox)
            self.main_hbox.addLayout(self.buttons_vbox)
            self.add_to_playlist_btn.setEnabled(False)
    
    def set_layout_visibility(self, layout, state):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            
            if item.widget():
                widget = item.widget()
                if state:
                    widget.show()
                else:
                    widget.hide()
            
            elif item.layout():
                sub_layout = item.layout()
                self.set_layout_visibility(sub_layout, state)
    
    def open_playlist(self):
        will_delete_playlist = False
        
        if self.playlist_opened:
            message_box = QMessageBox(self)
            message_box.setWindowTitle('Playlist already opened')
            message_box.setText('A playlist is already opened. Delete current playlist or append to existing?')
            btn_append = message_box.addButton("Append", QMessageBox.ButtonRole.AcceptRole)
            btn_delete = message_box.addButton("Delete", QMessageBox.ButtonRole.ActionRole)
            message_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            
            message_box.exec()
            
            if message_box.clickedButton() == btn_append:
                pass
            elif message_box.clickedButton() == btn_delete:
                will_delete_playlist = True
            else:
                return
        
        path = QFileDialog.getOpenFileName(self, 'Open File', filter='M3U Files (*.m3u)')[0]
        if not path:
            return
        if will_delete_playlist:
            self.playlist.clear()
        songs = load_m3u(path)
        playlist_metadata = get_song_metadata(songs, os.path.dirname(path), cover_as_bytes=True)
        self.display_songs(playlist_metadata, self.playlist)
        self.handle_size_dependent_buttons()
        self.playlist_label.setText(os.path.basename(path))
    
    def open_folder(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory')
        if not path:
            return
        songs = [i for i in os.listdir(path) if os.path.splitext(i)[1].lower() == '.flac']
        if len(songs) == 0:
            QMessageBox.warning(self, 'Error', 'No FLAC files found.')
            return
        self.folder_metadata = get_song_metadata(songs, path, cover_as_bytes=True)
        self.folder_metadata.sort(key=lambda x: x['title'].lower())
        self.display_songs(self.folder_metadata, self.folderlist)
        if self.folderlist.count() > 0:
            self.add_to_playlist_btn.setEnabled(True)
            self.rename_folder_btn.setEnabled(True)
            
            self.current_folderlist = path
            self.sort_mode_combo.setEnabled(True)
            self.folder_label.setText(os.path.basename(path))
    
    def display_songs(self, metadata, listwidget):
        for song in metadata:
            if song['cover']:
                pixmap = QPixmap()
                pixmap.loadFromData(song['cover'])
                del song['cover']
            else:
                pixmap = QPixmap('disc.png')
            
            scaled_pixmap = pixmap.scaled(
                self.icon_size, self.icon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon = QIcon(scaled_pixmap)
            item = QListWidgetItem(icon, song['text'])
            item.setData(Qt.UserRole, song)
            listwidget.addItem(item)
    
    def save_playlist(self):
        if not self.playlist_opened:
            return
        
        message_box = QMessageBox(self)
        message_box.setWindowTitle('Path handling')
        message_box.setText('How should paths be saved?')
        btn_abs = message_box.addButton("Absolute", QMessageBox.ButtonRole.AcceptRole)
        btn_rel = message_box.addButton("Relative", QMessageBox.ButtonRole.ActionRole)
        message_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        
        message_box.exec()
        
        if message_box.clickedButton() == btn_abs:
            rel_paths = False
        elif message_box.clickedButton() == btn_rel:
            rel_paths = True
        else:
            return
        path = QFileDialog.getSaveFileName(self, 'Save File', filter='M3U Files (*.m3u)')[0]
        if not path:
            return
        new_metadata = []
        for i in range(self.playlist.count()):
            song_data = self.playlist.item(i).data(Qt.UserRole)
            new_metadata.append(song_data)
        
        print(new_metadata)
        save_as_m3u(path, new_metadata, rel_paths)
        QMessageBox.information(self, 'Success', 'Playlist saved successfully.')
    
    def clear_playlist(self):
        reply = QMessageBox.question(self, 'Clear playlist', 'Are you sure you want to clear the playlist?',
                                     QMessageBox.StandardButton.Yes
                                     | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No, )
        if reply == QMessageBox.StandardButton.Yes:
            self.playlist.clear()
        self.handle_size_dependent_buttons()
    
    def add_to_playlist(self):
        current_row = self.folderlist.currentRow()
        if current_row >= 0:
            item = self.folderlist.currentItem()
            print(item.data(Qt.UserRole))
            self.playlist.addItem(item.clone())
            self.handle_size_dependent_buttons()
            self.playlist.scrollToBottom()
            self.playlist.setCurrentRow(self.playlist.count() - 1)
    
    def add_file_to_playlist(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', filter='FLAC files (*.flac)')[0]
        if not path:
            return
        songs = [path]
        playlist_metadata = get_song_metadata(songs, os.path.dirname(path), cover_as_bytes=True)
        self.display_songs(playlist_metadata, self.playlist)
        self.handle_size_dependent_buttons()
        self.playlist.scrollToBottom()
        self.playlist.setCurrentRow(self.playlist.count() - 1)
    
    def remove_from_playlist(self):
        current_row = self.playlist.currentRow()
        if current_row >= 0:
            self.playlist.takeItem(current_row)
        
        self.handle_size_dependent_buttons()
    
    def move_up(self):
        current_row = self.playlist.currentRow()
        
        if current_row > 0:
            item = self.playlist.takeItem(current_row)
            self.playlist.insertItem(current_row - 1, item)
            self.playlist.setCurrentRow(current_row - 1)
    
    def move_down(self):
        current_row = self.playlist.currentRow()
        total_items = self.playlist.count()
        
        if 0 <= current_row < total_items - 1:
            item = self.playlist.takeItem(current_row)
            self.playlist.insertItem(current_row + 1, item)
            self.playlist.setCurrentRow(current_row + 1)
    
    def rename(self):
        self.rename_dialog = RenameDialog(self, self.current_folderlist)
        if self.rename_dialog.exec():
            batch_rename(self.current_folderlist, self.rename_dialog.pattern_edit.text(), False)
            QMessageBox.information(self, 'Success', 'All files renamed successfully.')
    
    def change_sort_mode(self, index):
        print(index)
        items = [self.folderlist.takeItem(0) for _ in range(self.folderlist.count())]
        match index:
            case 0:
                items.sort(key=lambda x: x.data(Qt.ItemDataRole.UserRole)['title'].lower())
            case 1:
                items.sort(key=lambda x: x.data(Qt.ItemDataRole.UserRole)['title'].lower(), reverse=True)
            case 2:
                items.sort(key=lambda x: x.data(Qt.ItemDataRole.UserRole)['artists'].lower())
            case 3:
                items.sort(key=lambda x: x.data(Qt.ItemDataRole.UserRole)['artists'].lower(), reverse=True)
        
        for item in items:
            self.folderlist.addItem(item)
    
    def check_move_buttons(self):
        if self.playlist.count() > 0:
            if self.playlist.currentRow() > 0:
                self.move_up_btn.setEnabled(True)
            else:
                self.move_up_btn.setEnabled(False)
            
            if self.playlist.currentRow() < self.playlist.count() - 1:
                self.move_down_btn.setEnabled(True)
            else:
                self.move_down_btn.setEnabled(False)
    
    def handle_size_dependent_buttons(self):
        if self.playlist.count() > 0:
            self.playlist_opened = True
            self.remove_from_playlist_btn.setEnabled(True)
            self.save_playlist_btn.setEnabled(True)
        else:
            self.playlist_opened = False
            self.remove_from_playlist_btn.setEnabled(False)
            self.save_playlist_btn.setEnabled(False)
        
        if self.playlist.count() > 1:
            self.check_move_buttons()
        else:
            self.move_up_btn.setEnabled(False)
            self.move_down_btn.setEnabled(False)
    
    def keyPressEvent(self, event):
        shift = bool(event.modifiers() & Qt.ShiftModifier)
        
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.add_to_playlist()
        
        elif event.key() == Qt.Key_Delete:
            self.remove_from_playlist()
        
        # elif shift and event.key() == Qt.Key_Up:
        #     self.move_up()
        # elif shift and event.key() == Qt.Key_Down:
        #     self.move_down()
        # elif shift and event.key() == Qt.Key_Left:
        #     self.remove_from_playlist()
        # elif shift and event.key() == Qt.Key_Down:
        #     self.add_to_playlist()
        
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        if self.playlist_opened:
            reply = QMessageBox.question(self, 'Unsaved changes', 'Close without saving?',
                                         QMessageBox.StandardButton.Yes |
                                         QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.ignore()


class RenameDialog(QDialog):
    def __init__(self, parent=None, folder=None):
        super().__init__(parent)
        
        self.folder = folder
        
        self.setWindowTitle('Rename files')
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.resize(600, 600)
        
        self.pattern_hbox = QHBoxLayout()
        self.pattern_hbox.addWidget(QLabel('Pattern:'))
        self.pattern_edit = QLineEdit(self)
        self.pattern_edit.setPlaceholderText('%T = Title, %A = Artists')
        self.pattern_hbox.addWidget(self.pattern_edit)
        
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(2)
        
        self.table_widget.setHorizontalHeaderLabels(["Old filename", "New filename"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.table_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table_widget.setStyleSheet(
            """
            QTableWidget::item:hover {
                background-color: transparent;
            }
        """
        )
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        self.pattern_edit.textChanged.connect(self.update_preview)
        
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.pattern_hbox)
        self.vbox.addWidget(self.table_widget)
        self.vbox.addWidget(self.button_box)
        self.setLayout(self.vbox)
    
    def update_preview(self):
        data = batch_rename(self.folder, self.pattern_edit.text(), True)
        self.update_tableview(data)
    
    def update_tableview(self, data: list[tuple[str, str]]):
        self.table_widget.setRowCount(len(data))
        for i, row in enumerate(data):
            self.table_widget.setItem(i, 0, QTableWidgetItem(row[0]))
            self.table_widget.setItem(i, 1, QTableWidgetItem(row[1]))


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About YouTube History Visualizer')
        
        self.vbox = QVBoxLayout()
        self.license_text = '''Copyright (C) 2026  leonhardw
<br>
Source code available on <a href="https://github.com/leonhardw">GitHub</a>
<br><br>
Disc icon (disc.png):<br>
Image by <a href="https://pixabay.com/users/clker-free-vector-images-3736/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=34919">
Clker-Free-Vector-Images</a> from
<a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=34919">Pixabay</a>
<br>
<a href="https://pixabay.com/vectors/dvd-music-disk-compact-disc-cd-34919/">https://pixabay.com/vectors/dvd-music-disk-compact-disc-cd-34919/</a>
<br><br>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <a href="https://www.gnu.org/licenses/">&lt;https://www.gnu.org/licenses/&gt;</a>.'''
        self.license_label = QLabel()
        self.license_label.setTextFormat(Qt.RichText)
        self.license_label.setWordWrap(True)
        self.license_label.setText(self.license_text)
        self.license_label.setOpenExternalLinks(True)
        
        self.hbox = QHBoxLayout()
        self.about_qt_btn = QPushButton('About Qt')
        self.about_qt_btn.clicked.connect(self.show_about_qt_dialog)
        
        self.close_btn = QPushButton('Close')
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setDefault(True)
        
        self.hbox.addWidget(self.about_qt_btn)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.close_btn)
        
        self.vbox.addWidget(self.license_label)
        self.vbox.addLayout(self.hbox)
        
        self.setLayout(self.vbox)
    
    def show_about_qt_dialog(self):
        QMessageBox.aboutQt(self, 'About Qt')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlaylistEditor()
    window.show()
    # r = RenameDialog()
    # r.update_tableview([('ABC', 'DEF'), ('GHI', 'JKL')])
    # r.exec()
    sys.exit(app.exec())
