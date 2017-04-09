import os
import logging
from PyQt5 import QtGui, QtCore, QtWidgets

import ftransc
import ftransc_gui.utils
import ftransc.utils
import ftransc.metadata
import ftransc.core.transcoders


logger = logging.getLogger(__name__)


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None, cmdlinefiles=None):
        super(Window, self).__init__(parent)

        self.filename_column_index = 0
        self.title_column_index = 1
        self.artist_column_index = 2
        self.genre_column_index = 3
        self.status_column_index = 4

        add_files_button = self.createButton("&Add Files", self.add_files)
        convert_button = self.createButton("Conv&ert", self.convert)
        cancel_button = QtWidgets.QPushButton("&Close")
        browse_button = self.createButton("&Output Folder", self.browse)

        self.delete_original_checkbox = QtWidgets.QCheckBox("&Delete")
        self.overwrite_checkbox = QtWidgets.QCheckBox("Over&write")
        self.unlock_checkbox = QtWidgets.QCheckBox("&Unlock")
        self.foldername = QtWidgets.QLabel("")
        self.foldername.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        head_layout = QtWidgets.QHBoxLayout()
        body_layout = QtWidgets.QVBoxLayout()
        foot_layout = QtWidgets.QHBoxLayout()
        browse_layout = QtWidgets.QHBoxLayout()
        codec_layout = QtWidgets.QHBoxLayout()

        head_layout.addWidget(add_files_button)
        head_layout.addWidget(browse_button)
        head_layout.addSpacing(500)

        # browse_layout.addWidget(self.foldername)

        codec_label = QtWidgets.QLabel("Convert To:")
        self.codec_combobox = QtWidgets.QComboBox()
        formats = ftransc.utils.get_audio_formats()
        for idx, fmt in enumerate(formats):
            self.codec_combobox.addItem(fmt)
            if fmt == 'mp3':
                self.codec_combobox.setCurrentIndex(idx)

        quality_label = QtWidgets.QLabel("Quality:")
        self.quality_combobox = QtWidgets.QComboBox()
        presets = ['Insane', 'Extreme', 'High', 'Normal', 'Low', 'Tiny']
        for idx, preset in enumerate(presets):
            self.quality_combobox.addItem(preset)
            if preset == 'Normal':
                self.quality_combobox.setCurrentIndex(idx)

        codec_layout.addWidget(codec_label)
        codec_layout.addWidget(self.codec_combobox)
        codec_layout.addWidget(quality_label)
        codec_layout.addWidget(self.quality_combobox)

        head_layout.addLayout(codec_layout)
        foot_layout.addWidget(self.delete_original_checkbox)
        foot_layout.addWidget(self.overwrite_checkbox)
        foot_layout.addWidget(self.unlock_checkbox)
        foot_layout.addSpacing(50)
        foot_layout.addWidget(self.foldername)
        foot_layout.addSpacing(100)
        foot_layout.addWidget(convert_button)
        foot_layout.addWidget(cancel_button)

        self.createFilesTable()

        body_layout.addLayout(head_layout)
        # body_layout.addLayout(browse_layout)
        body_layout.addWidget(self.filesTable)
        body_layout.addLayout(foot_layout)

        self.setLayout(body_layout)
        self.setWindowTitle("ftransc gui {0}".format(ftransc_gui.utils.get_display_version()))
        self.resize(700, 400)

        cancel_button.clicked.connect(self.close)

        if cmdlinefiles is not None:
            self.cmdlinefiles = cmdlinefiles
            self.add_files(noninteractive=True)
            self.cmdlinefiles = None

    def add_files(self, noninteractive=False):
        if noninteractive:
            files = self.cmdlinefiles
        else:
            filt = "All Files (*)";
            filt += ";;Audio Files (*.mp3 *.wma *.aac *.mp4 *.m4a *.flac *.ogg"
            filt += " *.mpc *.mka *.mp+ *.ape *.wv *.wav *.aiff)"
            filt += ";;Video Files (*.avi *.flv *.mpg *.mpeg *.vob *.divx *.mkv *.mp4)"
            files, chosen_filter = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                       'Add files to convert',
                                                       QtCore.QDir.currentPath(),
                                                       filt)

        for i in files:
            tags = {k: v if v is not None else '' for k, v in ftransc.metadata.Metadata(i).input_tags.items()}
            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, self.status_column_index, QtWidgets.QTableWidgetItem('Scheduled'))
            self.filesTable.setItem(row, self.genre_column_index, QtWidgets.QTableWidgetItem(tags['genre']))
            self.filesTable.setItem(row, self.artist_column_index, QtWidgets.QTableWidgetItem(tags['artist']))
            self.filesTable.setItem(row, self.title_column_index, QtWidgets.QTableWidgetItem(tags['title']))
            self.filesTable.setItem(row, self.filename_column_index, QtWidgets.QTableWidgetItem(i))

    def browse(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                        'Add output folder',
                                                        QtCore.QDir.currentPath())
        if folder is not None or folder != '':
            self.foldername.setText(folder)

    def convert(self):
        row_count = self.filesTable.rowCount()
        audio_format = str(self.codec_combobox.currentText()).lower()
        audio_quality = str(self.quality_combobox.currentText()).lower()
        for row_number in range(row_count):
            status = QtWidgets.QTableWidgetItem('Scheduled')
            self.filesTable.setItem(row_number, self.status_column_index, status)
            self.filesTable.repaint()
        for row_number in range(row_count):
            filename = self.filesTable.item(row_number, self.filename_column_index).text()
            status = QtWidgets.QTableWidgetItem('Converting...')
            self.filesTable.setItem(row_number, self.status_column_index, status)
            self.filesTable.repaint()
            self.filesTable.repaint()

            output_folder = self.foldername.text() if self.foldername.text() else './'
            output_filename = os.path.join(
                output_folder,
                os.path.basename(os.path.splitext(filename)[0] + "." + audio_format)
            )

            if not self.overwrite_checkbox.isChecked() and os.path.exists(output_filename):
                logger.info("Skipping %s. File exists. Overwrite mode not enabled.", filename)
                self.filesTable.repaint()
                self.filesTable.repaint()
                status = QtWidgets.QTableWidgetItem('Skipped')
                self.filesTable.setItem(row_number, self.status_column_index, status)
                self.filesTable.repaint()
                self.filesTable.repaint()
                continue

            swp_file = ".%s.swp" % filename
            if os.path.isfile(swp_file):
                if self.unlock_checkbox.isChecked():
                    os.remove(swp_file)
                else:
                    logger.info("Skipping %s. File locked. Unlock mode not enabled.", filename)
                    self.filesTable.repaint()
                    self.filesTable.repaint()
                    status = QtWidgets.QTableWidgetItem('Skipped')
                    self.filesTable.setItem(row_number, self.status_column_index, status)
                    self.filesTable.repaint()
                    self.filesTable.repaint()
                    continue

            audio_preset = ftransc.utils.get_audio_presets(audio_format=audio_format, audio_quality=audio_quality)
            metadata = ftransc.metadata.Metadata(filename)
            is_success = ftransc.core.transcoders.transcode(
                filename,
                audio_format,
                output_folder=output_folder,
                audio_preset=audio_preset
            )
            if not is_success:
                logger.error("Failed converting %s", filename)
                self.filesTable.repaint()
                self.filesTable.repaint()
                status = QtWidgets.QTableWidgetItem('Failed')
                self.filesTable.setItem(row_number, self.status_column_index, status)
                self.filesTable.repaint()
                self.filesTable.repaint()
                continue
            try:
                metadata.insert_tags(output_filename)
            except Exception as err:
                logger.error("%s: %s", err.__class__.__name__, str(err))
                logger.warning("Could not insert metadata to file: %s", filename)

            if self.delete_original_checkbox.isChecked():
                os.remove(filename)

            self.filesTable.repaint()
            self.filesTable.repaint()
            status = QtWidgets.QTableWidgetItem('Success')
            self.filesTable.setItem(row_number, self.status_column_index, status)
            self.filesTable.repaint()
            self.filesTable.repaint()

    def createFilesTable(self):
        self.filesTable = QtWidgets.QTableWidget(0, 5)
        self.filesTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.filesTable.setHorizontalHeaderLabels(["Filename", "Title", "Artist", "Genre", "Status"])
        self.filesTable.horizontalHeader().setSectionResizeMode(self.filename_column_index, QtWidgets.QHeaderView.Stretch)
        self.filesTable.horizontalHeader().setSectionResizeMode(self.title_column_index, QtWidgets.QHeaderView.Stretch)
        self.filesTable.horizontalHeader().setSectionResizeMode(self.artist_column_index, QtWidgets.QHeaderView.Stretch)
        self.filesTable.horizontalHeader().setSectionResizeMode(self.genre_column_index, QtWidgets.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(True)
        self.filesTable.setAlternatingRowColors(True)
        self.filesTable.setUpdatesEnabled(True)
        self.filesTable.keyPressEvent = self.delete_items

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def delete_items(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            items = self.filesTable.selectedIndexes()
            if items:
                rows = [item.row() for item in items]
                rows = list(set(rows))
                rows.sort()
                rows.reverse()
                for row in rows:
                    self.filesTable.removeRow(row)
        else:
            return QtWidgets.QTableWidget.keyPressEvent(self.filesTable, event)


class App(QtWidgets.QApplication):
    pass
