import os

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QMessageBox, QHBoxLayout, QFrame, QCheckBox
from tqdm import tqdm

from PicProcess.batch_move_files import get_file_names, move_files
from ios_pic_process import copy_file, is_livp, unzip_livp, livp_to_jpg, heic_to_jpg


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Path processing widgets
        self.path_label = QLabel("处理路径:", self)
        self.path_edit = QLineEdit(self)
        self.path_edit.textChanged.connect(self.validate_path_input)
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
        self.source_dir_edit.textChanged.connect(self.validate_source_dir_input)
        self.source_dir_button = QPushButton('浏览', self)
        self.source_dir_button.clicked.connect(self.choose_source_dir)

        self.file_name_table_label = QLabel("文件列表:", self)
        self.file_name_table_edit = QLineEdit(self)
        self.file_name_table_edit.textChanged.connect(self.validate_file_name_input)
        self.process_sub_folder_checkbox = QCheckBox("处理子文件夹", self)
        self.get_file_list_button = QPushButton('获取文件列表', self)
        self.get_file_list_button.clicked.connect(self.get_file_list)

        self.target_dir_label = QLabel("目标文件夹:", self)
        self.target_dir_edit = QLineEdit(self)
        self.target_dir_edit.textChanged.connect(self.validate_target_dir_input)
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
        processing_buttons_layout = QHBoxLayout()
        processing_buttons_layout.addWidget(self.unzip_livp_button)
        processing_buttons_layout.addWidget(self.livp2jpg_button)
        processing_buttons_layout.addWidget(self.heic2jpg)
        layout.addLayout(processing_buttons_layout)

        # Set the same width for all processing buttons
        button_width = max(self.unzip_livp_button.sizeHint().width(), self.livp2jpg_button.sizeHint().width(), self.heic2jpg.sizeHint().width())
        self.unzip_livp_button.setFixedWidth(button_width)
        self.livp2jpg_button.setFixedWidth(button_width)
        self.heic2jpg.setFixedWidth(button_width)

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

        # File operations layout
        file_operations_layout = QHBoxLayout()
        file_operations_layout.addWidget(self.process_sub_folder_checkbox)
        file_operations_layout.addWidget(self.get_file_list_button)
        file_operations_layout.addWidget(self.move_files_button)
        layout.addLayout(file_operations_layout)

        # Set the same width for all file operation buttons
        button_width = max(self.process_sub_folder_checkbox.sizeHint().width(), self.get_file_list_button.sizeHint().width(), self.move_files_button.sizeHint().width())
        self.process_sub_folder_checkbox.setFixedWidth(button_width)
        self.get_file_list_button.setFixedWidth(button_width)
        self.move_files_button.setFixedWidth(button_width)

        # Target directory layout
        target_dir_layout = QHBoxLayout()
        target_dir_layout.addWidget(self.target_dir_label)
        target_dir_layout.addWidget(self.target_dir_edit)
        target_dir_layout.addWidget(self.target_dir_button)
        layout.addLayout(target_dir_layout)

        self.setAcceptDrops(True)
        self.resize(500, 270)
        self.setWindowTitle("图片处理工具")  # Set window title

    def validate_path_input(self):
        path = self.path_edit.text()
        self.validate_path(path)

    def validate_source_dir_input(self):
        source_dir = self.source_dir_edit.text()
        self.validate_directory(source_dir)

    def validate_target_dir_input(self):
        target_dir = self.target_dir_edit.text()
        self.validate_directory(target_dir)

    def validate_file_name_input(self):
        file_name = self.file_name_table_edit.text()
        self.validate_file_name(file_name, valid_extensions=['.xlsx'])

    def show_temporary_message(self, title, message, duration=1000):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        QTimer.singleShot(duration, msg_box.close)
        msg_box.exec_()

    def validate_path(self, path):
        if not path or not os.path.exists(path):
            self.show_temporary_message('Warning', '路径无效或不存在')
            return False
        return True

    def validate_file_name(self, file_name, valid_extensions=None):
        if not file_name:
            self.show_temporary_message('Warning', '文件名不能为空')
            return False
        if valid_extensions and not any(file_name.lower().endswith(ext) for ext in valid_extensions):
            self.show_temporary_message('Warning', f'文件名必须以 {", ".join(valid_extensions)} 结尾')
            return False
        return True

    def validate_directory(self, directory):
        if not directory or not os.path.exists(directory):
            self.show_temporary_message('Warning', '文件夹路径无效或不存在')
            return False
        return True

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
        process_sub_folder = self.process_sub_folder_checkbox.isChecked()
        if not source_dir:
            QMessageBox.warning(self, 'Warning', '请填写源文件夹路径')
            return
        if not file_name_table:
            QMessageBox.warning(self, 'Warning', '请填写文件列表名称')
            return
        try:
            get_file_names(source_dir, process_sub_folder, file_name_table)
            QMessageBox.information(self, 'Info', '文件列表已生成')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'生成文件列表时出错: {e}')

    def move_files(self):
        target_dir = self.target_dir_edit.text()
        source_dir = self.source_dir_edit.text()
        file_name_table = self.file_name_table_edit.text()
        if not target_dir:
            QMessageBox.warning(self, 'Warning', '请填写目标文件夹路径')
            return
        if not source_dir:
            QMessageBox.warning(self, 'Warning', '请填写源文件夹路径')
            return
        if not file_name_table:
            QMessageBox.warning(self, 'Warning', '请填写文件列表名称')
            return
        file_name_table_path = os.path.join(source_dir, file_name_table)
        try:
            move_files(file_name_table_path, target_dir)
            QMessageBox.information(self, 'Info', '文件已移动')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'移动文件时出错: {e}')

    def choose_path(self):
        directory_path = QFileDialog.getExistingDirectory(self, '选择目录')
        if directory_path:  # Only update the directory path if a directory was selected
            self.path_edit.setText(directory_path)

    def unzip_livp_process(self):
        livp_path = self.path_edit.text()
        if not livp_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        unzip_path = os.path.join(livp_path, 'unzip')
        if not os.path.exists(unzip_path):
            os.makedirs(unzip_path)
        try:
            img_list = [img for img in os.listdir(livp_path) if img.lower().endswith('.livp')]
            for img_item in tqdm(img_list):
                img_source = os.path.join(livp_path, img_item)
                if is_livp(img_item):
                    unzip_livp(img_item, img_source, unzip_path)
                else:
                    copy_file(img_source, os.path.join(unzip_path, img_item))
            QMessageBox.information(self, 'Info', '图片处理成功')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'解压 livp 文件时出错: {e}')

    def livp2jpg_process(self):
        livp_path = self.path_edit.text()
        if not livp_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        jpg_path = os.path.join(livp_path, 'jpg')
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)
        try:
            img_list = [img for img in os.listdir(livp_path) if img.lower().endswith('.livp')]
            for img_item in tqdm(img_list):
                img_source = os.path.join(livp_path, img_item)
                if is_livp(img_item):
                    livp_to_jpg(img_item, img_source, jpg_path)
                else:
                    copy_file(img_source, os.path.join(jpg_path, img_item))
            QMessageBox.information(self, 'Info', '图片处理成功')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'转换 livp 文件为 jpg 时出错: {e}')

    def heic2jpg_proccess(self):
        heic_path = self.path_edit.text()
        if not heic_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        jpg_path = os.path.join(heic_path, 'jpg')
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)
        try:
            img_list = [img for img in os.listdir(heic_path) if img.lower().endswith('.heic')]
            for img_item in tqdm(img_list):
                img_source = os.path.join(heic_path, img_item)
                heic_to_jpg(img_item, img_source, jpg_path)
            QMessageBox.information(self, 'Info', '图片处理成功')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'转换 heic 文件为 jpg 时出错: {e}')


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("图片处理工具")
    window = MainWindow()
    window.show()
    app.exec_()

# TODO：获取文件列表，包括各种元信息
# 在excel中对列表进行处理与筛选，然后导入进行移动
