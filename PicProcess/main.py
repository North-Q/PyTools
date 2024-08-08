import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QMessageBox, QHBoxLayout, QFrame
from tqdm import tqdm

from PicProcess.batch_move_files import get_file_names, move_files
from ios_pic_process import copy_file, is_livp, unzip_livp, livp_to_jpg, heic_to_jpg


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Path processing widgets
        self.path_label = QLabel("处理路径:", self)
        self.path_edit = QLineEdit(self)
        self.open_button = QPushButton('浏览', self)
        self.open_button.clicked.connect(self.choose_path)

        # Processing buttons
        self.unzip_livp_button = QPushButton('解压 livp', self)
        self.livp2jpg_button = QPushButton('livp->jpg', self)
        self.heic2jpg = QPushButton('heic->jpg', self)
        self.unzip_livp_button.clicked.connect(self.unzip_livp_process)
        self.livp2jpg_button.clicked.connect(self.livp2jpg_process)
        self.heic2jpg.clicked.connect(self.heic2jpg_proccess)

        # Info label
        self.info_label = QLabel("注：使用前请清空处理目录下的 unzip 文件夹和 jpg 文件夹", self)

        # Horizontal line
        self.separator_line = QFrame(self)
        self.separator_line.setFrameShape(QFrame.HLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)

        # Batch move files widgets
        self.source_dir_label = QLabel("源文件夹:", self)
        self.source_dir_edit = QLineEdit(self)
        self.source_dir_button = QPushButton('浏览', self)
        self.source_dir_button.clicked.connect(self.choose_source_dir)

        self.file_name_table_label = QLabel("文件列表名字:", self)
        self.file_name_table_edit = QLineEdit(self)
        self.get_file_list_button = QPushButton('获取文件列表', self)
        self.get_file_list_button.clicked.connect(self.get_file_list)

        self.target_dir_label = QLabel("目标文件夹:", self)
        self.target_dir_edit = QLineEdit(self)
        self.target_dir_button = QPushButton('浏览', self)
        self.target_dir_button.clicked.connect(self.choose_target_dir)

        self.move_files_button = QPushButton('移动文件', self)
        self.move_files_button.clicked.connect(self.move_files)

        # Layout setup
        layout = QVBoxLayout(self)

        # Path processing layout
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.open_button)
        layout.addLayout(path_layout)

        # Processing buttons layout
        layout.addWidget(self.unzip_livp_button)
        layout.addWidget(self.livp2jpg_button)
        layout.addWidget(self.heic2jpg)

        # Info label layout
        layout.addWidget(self.info_label)

        # Add the separator line
        separator_line_layout = QHBoxLayout()
        separator_line_layout.addWidget(self.separator_line)
        layout.addLayout(separator_line_layout)

        # Source directory layout
        source_dir_layout = QHBoxLayout()
        source_dir_layout.addWidget(self.source_dir_label)
        source_dir_layout.addWidget(self.source_dir_edit)
        source_dir_layout.addWidget(self.source_dir_button)
        layout.addLayout(source_dir_layout)

        # File name table layout
        file_name_table_layout = QHBoxLayout()
        file_name_table_layout.addWidget(self.file_name_table_label)
        file_name_table_layout.addWidget(self.file_name_table_edit)
        layout.addLayout(file_name_table_layout)
        layout.addWidget(self.get_file_list_button)

        # Target directory layout
        target_dir_layout = QHBoxLayout()
        target_dir_layout.addWidget(self.target_dir_label)
        target_dir_layout.addWidget(self.target_dir_edit)
        target_dir_layout.addWidget(self.target_dir_button)
        layout.addLayout(target_dir_layout)

        # Move files button
        layout.addWidget(self.move_files_button)

        self.setAcceptDrops(True)
        self.resize(600, 380)
        self.setWindowTitle("图片处理工具")  # Set window title

    def choose_source_dir(self):
        directory_path = QFileDialog.getExistingDirectory(self, '选择源文件夹')
        if directory_path:
            self.source_dir_edit.setText(directory_path)

    def choose_target_dir(self):
        directory_path = QFileDialog.getExistingDirectory(self, '选择目标文件夹')
        if directory_path:
            self.target_dir_edit.setText(directory_path)

    def get_file_list(self):
        source_dir = self.source_dir_edit.text()
        file_name_table = self.file_name_table_edit.text()
        if source_dir and file_name_table:
            get_file_names(source_dir, file_name_table)
            QMessageBox.information(self, 'Info', '文件列表已生成')

    def move_files(self):
        source_dir = self.source_dir_edit.text()
        target_dir = self.target_dir_edit.text()
        file_name_table = self.file_name_table_edit.text()
        if source_dir and target_dir and file_name_table:
            move_files(file_name_table, target_dir, source_dir)
            QMessageBox.information(self, 'Info', '文件已移动')

    def choose_path(self):
        directory_path = QFileDialog.getExistingDirectory(self, '选择目录')
        if directory_path:  # Only update the directory path if a directory was selected
            self.path_edit.setText(directory_path)

    def unzip_livp_process(self):
        livp_path = self.path_edit.text()
        unzip_path = os.path.join(livp_path, 'unzip')
        if not os.path.exists(unzip_path):
            os.makedirs(unzip_path)
        if not livp_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        img_list = [img for img in os.listdir(livp_path) if img.lower().endswith('.livp')]
        for img_item in tqdm(img_list):
            img_source = os.path.join(livp_path, img_item)
            if is_livp(img_item):
                unzip_livp(img_item, img_source, unzip_path)
            else:
                copy_file(img_source, os.path.join(unzip_path, img_item))
        QMessageBox.information(self, 'Info', '图片处理成功')

    def livp2jpg_process(self):
        livp_path = self.path_edit.text()
        jpg_path = os.path.join(livp_path, 'jpg')
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)
        if not livp_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        img_list = [img for img in os.listdir(livp_path) if img.lower().endswith('.livp')]
        for img_item in tqdm(img_list):
            img_source = os.path.join(livp_path, img_item)
            if is_livp(img_item):
                livp_to_jpg(img_item, img_source, jpg_path)
            else:
                copy_file(img_source, os.path.join(jpg_path, img_item))
        QMessageBox.information(self, 'Info', '图片处理成功')

    def heic2jpg_proccess(self):
        heic_path = self.path_edit.text()
        jpg_path = os.path.join(heic_path, 'jpg')
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)
        if not heic_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        img_list = [img for img in os.listdir(heic_path) if img.lower().endswith('.heic')]
        for img_item in tqdm(img_list):
            img_source = os.path.join(heic_path, img_item)
            heic_to_jpg(img_item, img_source, jpg_path)
        QMessageBox.information(self, 'Info', '图片处理成功')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.path_edit.setText(file_path)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W and event.modifiers() & Qt.ControlModifier:
            self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("图片处理工具")
    window = MainWindow()
    window.show()
    app.exec_()
