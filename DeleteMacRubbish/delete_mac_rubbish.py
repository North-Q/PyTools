import os
import sys

from PyQt5.QtCore import pyqtSignal, QThread, QThreadPool, QRunnable
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox, QTextEdit, QProgressBar

MaxThreadCount = 4


class RubbishCleaner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mac垃圾清理')
        self.setGeometry(100, 100, 600, 450)
        self.setAcceptDrops(True)

        # Source directory input
        self.source_label = QLabel('清理目录：', self)
        self.source_label.setGeometry(20, 20, 120, 30)

        self.source_input = QLineEdit(self)
        self.source_input.setGeometry(100, 20, 350, 30)
        self.source_input.setPlaceholderText('输入或拖拽目录')
        self.source_input.setAcceptDrops(True)
        self.source_input.dragEnterEvent = self.dragEnterEvent
        self.source_input.dropEvent = self.dropEvent
        self.source_input.textChanged.connect(self.on_text_changed)

        self.browse_button = QPushButton('浏览', self)
        self.browse_button.setGeometry(460, 20, 100, 30)
        self.browse_button.clicked.connect(self.browse_directory)

        # Get rubbish paths button
        self.get_rubbish_button = QPushButton('扫描垃圾', self)
        self.get_rubbish_button.setGeometry(20, 70, 150, 30)
        self.get_rubbish_button.clicked.connect(self.get_rubbish_paths)

        # Open rubbish list button
        self.open_rubbish_button = QPushButton('检查垃圾', self)
        self.open_rubbish_button.setGeometry(200, 70, 150, 30)
        self.open_rubbish_button.clicked.connect(self.open_rubbish_list)

        # Delete rubbish button
        self.delete_rubbish_button = QPushButton('删除垃圾', self)
        self.delete_rubbish_button.setGeometry(380, 70, 150, 30)
        self.delete_rubbish_button.clicked.connect(self.delete_rubbish)

        # Text area to display rubbish paths
        self.rubbish_display = QTextEdit(self)
        self.rubbish_display.setGeometry(20, 120, 560, 250)
        self.rubbish_display.setReadOnly(True)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 390, 560, 30)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        # Rubbish count label
        self.rubbish_count_label = QLabel('垃圾数量：0', self)
        self.rubbish_count_label.setGeometry(20, 390, 560, 30)
        self.rubbish_count_label.hide()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        try:
            urls = event.mimeData().urls()
            if urls:
                new_directories = [url.toLocalFile() for url in urls]
                existing_directories = self.source_input.text().split(';') if self.source_input.text() else []
                all_directories = existing_directories + new_directories
                self.source_input.setText(';'.join(all_directories))
        except Exception as e:
            QMessageBox.critical(self, '错误', f'Error during drag-and-drop: {str(e)}')

    def browse_directory(self):
        try:
            directories = []
            while True:
                directory = QFileDialog.getExistingDirectory(self, '选择目录')
                if directory:
                    directories.append(directory)
                else:
                    break
            if directories:
                existing_directories = self.source_input.text().split(';') if self.source_input.text() else []
                all_directories = existing_directories + directories
                self.source_input.setText(';'.join(all_directories))
        except Exception as e:
            QMessageBox.critical(self, '错误', f'Error during directory browsing: {str(e)}')

    def on_text_changed(self, text):
        corrected_text = text.replace('/', '\\')
        if text != corrected_text:
            self.source_input.blockSignals(True)
            self.source_input.setText(corrected_text)
            self.source_input.blockSignals(False)

    def get_rubbish_paths(self):
        source_paths = self.source_input.text().split(';')
        if not source_paths or all(not os.path.isdir(path) for path in source_paths):
            QMessageBox.warning(self, '警告', '请输入有效的清理目录。')
            return

        self.rubbish_display.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.rubbish_count_label.hide()
        self.scan_thread = ScanThread(source_paths)
        self.scan_thread.progress.connect(self.update_progress)
        self.scan_thread.rubbish_found.connect(self.add_rubbish_path)
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def add_rubbish_path(self, path):
        self.rubbish_display.append(path)

    def scan_finished(self):
        self.progress_bar.hide()
        rubbish_paths = list(set(path for path in self.rubbish_display.toPlainText().split('\n') if path.strip()))
        self.rubbish_display.clear()
        for path in rubbish_paths:
            self.rubbish_display.append(path)
        self.output_rubbish_paths(rubbish_paths)
        rubbish_count = len(rubbish_paths)
        self.rubbish_count_label.setText(f'垃圾数量：{rubbish_count}')
        self.rubbish_count_label.show()
        QMessageBox.information(self, '提示', '扫描完成。')

    def open_rubbish_list(self):
        try:
            if os.path.exists('rubbish.txt'):
                os.system('notepad rubbish.txt')
            else:
                QMessageBox.warning(self, '警告', '垃圾列表文件不存在。')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'Error during opening rubbish list: {str(e)}')

    def delete_rubbish(self):
        if self.rubbish_display is None or self.rubbish_display.toPlainText() == '':
            QMessageBox.warning(self, '警告', '请先扫描垃圾。')
            return
        else:
            reply = QMessageBox.question(self, 'Confirmation', '是否确定删除所有垃圾', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    rubbish_paths = self.rubbish_display.toPlainText().split('\n')
                    for rubbish_path in rubbish_paths:
                        try:
                            if os.path.exists(rubbish_path):
                                os.remove(rubbish_path)
                        except Exception as e:
                            QMessageBox.critical(self, '错误', f'Error during deleting file {rubbish_path}: {str(e)}')

                    if os.path.exists('rubbish.txt'):
                        os.remove('rubbish.txt')
                    self.rubbish_display.clear()
                    self.rubbish_count_label.hide()
                    QMessageBox.information(self, '提示', '垃圾清理完成。')
                except Exception as e:
                    QMessageBox.critical(self, '错误', f'Error during deletion: {str(e)}')

                try:
                    self.source_input.clear()
                    self.rubbish_display.clear()
                    if os.path.exists('rubbish.txt'):
                        os.remove('rubbish.txt')
                    self.rubbish_count_label.hide()
                except Exception as e:
                    QMessageBox.critical(self, '错误', f'Error during reset: {str(e)}')

    def output_rubbish_paths(self, rubbish_paths):
        try:
            with open('rubbish.txt', 'w', encoding='utf-8') as f:
                for rubbish_path in rubbish_paths:
                    f.write(rubbish_path.replace('\\', '/') + '\n')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'Error during writing rubbish paths: {str(e)}')


class ScanThread(QThread):
    progress = pyqtSignal(int)
    rubbish_found = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, source_paths):
        super().__init__()
        self.source_paths = source_paths

    def run(self):
        rubbish_paths = []
        total_files = sum([len(files) for source_path in self.source_paths for r, d, files in os.walk(source_path)])
        scanned_files = 0

        # Create a thread pool
        thread_pool = QThreadPool.globalInstance()
        thread_pool.setMaxThreadCount(MaxThreadCount)  # Adjust the number of threads as needed

        # Divide the directories into chunks
        directories = [os.path.join(root, d) for source_path in self.source_paths for root, dirs, files in os.walk(source_path) for d in dirs]
        chunk_size = len(directories) // thread_pool.maxThreadCount()
        chunks = [directories[i:i + chunk_size] for i in range(0, len(directories), chunk_size)]

        # Create and start threads
        for chunk in chunks:
            runnable = ScanRunnable(chunk, self.rubbish_found, self.progress, total_files, scanned_files)
            thread_pool.start(runnable)

        thread_pool.waitForDone()
        self.progress.emit(100)
        self.finished.emit(len(rubbish_paths))


class ScanRunnable(QRunnable):
    def __init__(self, directories, rubbish_found_signal, progress_signal, total_files, scanned_files):
        super().__init__()
        self.directories = directories
        self.rubbish_found_signal = rubbish_found_signal
        self.progress_signal = progress_signal
        self.total_files = total_files
        self.scanned_files = scanned_files

    def run(self):
        for directory in self.directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file == '.DS_Store' or (file.startswith('._') and os.path.getsize(file_path) == 4096):
                        self.rubbish_found_signal.emit(file_path)
                    self.scanned_files += 1
                    progress = int((self.scanned_files / self.total_files) * 100)
                    self.progress_signal.emit(progress)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    ex = RubbishCleaner()
    ex.show()
    sys.exit(app.exec_())

# pyinstaller --onefile --windowed --icon=icon.ico main.py
