import os
import shutil
import zipfile

import pillow_heif
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QMessageBox
from tqdm import tqdm


def copy_file(source_path, des_path):
    if not os.path.exists(des_path):
        shutil.copy2(source_path, des_path)
    else:
        pass


def is_livp(file_name):
    if os.path.splitext(file_name)[-1] == ".livp" or os.path.splitext(file_name)[-1] == ".LIVP":
        return True
    else:
        return False


def read_image_file_rb(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    return file_data


def unzip_livp(img_item, img_source, des_dir):
    img_id = img_item.split('.')[0]
    livp_zip_name = os.path.join(des_dir, img_id + '.zip')
    print("livp_zip_name:", livp_zip_name)
    copy_file(img_source, livp_zip_name)  # 将文件复制成 zip 归档的形式
    heic_name = ''
    with zipfile.ZipFile(livp_zip_name) as zf:
        for zip_file_item in zf.namelist():
            zf.extract(zip_file_item, des_dir)
            if zip_file_item.split('.')[-1] == 'heic':
                heic_name = zip_file_item
    os.remove(livp_zip_name)  # 删除 zip 文件
    heic_img_path = os.path.join(des_dir, heic_name)
    heif_file = pillow_heif.read_heif(heic_img_path)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
    jpg_save_path = os.path.join(des_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")
    os.remove(heic_img_path)  # 删除 heic 文件


def livp_to_jpg(img_item, img_source, livp_to_jpg_dir):
    img_id = img_item.split('.')[0]
    livp_zip_name = os.path.join(livp_to_jpg_dir, img_id + '.zip')
    copy_file(img_source, livp_zip_name)  # 将文件复制成 zip 归档的形式
    heic_name = ''
    with zipfile.ZipFile(livp_zip_name) as zf:
        for zip_file_item in zf.namelist():
            if zip_file_item.split('.')[-1] == 'heic':
                zf.extract(zip_file_item, livp_to_jpg_dir)
                heic_name = zip_file_item
    os.remove(livp_zip_name)  # 删除 zip 文件
    heic_img_path = os.path.join(livp_to_jpg_dir, heic_name)
    heif_file = pillow_heif.read_heif(heic_img_path)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
    jpg_save_path = os.path.join(livp_to_jpg_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")
    os.remove(heic_img_path)  # 删除 heic 文件


def heic_to_jpg(img_item, img_source, livp_to_jpg_dir):
    img_id = img_item.split('.')[0]
    heif_file = pillow_heif.read_heif(img_source)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
    jpg_save_path = os.path.join(livp_to_jpg_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.path_label = QLabel("处理路径:", self)
        self.info_label = QLabel("使用前请清空处理目录下的 unzip 文件夹和 jpg 文件夹", self)
        self.path_edit = QLineEdit(self)
        self.open_button = QPushButton('选择目录', self)
        self.unzip_livp_button = QPushButton('解压 livp', self)
        self.livp2jpg_button = QPushButton('livp->jpg', self)
        self.heic2jpg = QPushButton('heic->jpg', self)
        self.open_button.clicked.connect(self.choose_path)
        self.unzip_livp_button.clicked.connect(self.unzip_livp_process)
        self.livp2jpg_button.clicked.connect(self.livp2jpg_process)
        self.heic2jpg.clicked.connect(self.heic2jpg_proccess)

        layout = QVBoxLayout(self)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_edit)
        layout.addWidget(self.open_button)
        layout.addWidget(self.unzip_livp_button)
        layout.addWidget(self.livp2jpg_button)
        layout.addWidget(self.heic2jpg)
        layout.addWidget(self.info_label)

        self.setAcceptDrops(True)
        self.resize(600, 400)

        self.setWindowTitle("IOS 照片处理")  # 设置窗口标题

    def choose_path(self):
        directory_path = QFileDialog.getExistingDirectory(self, '选择目录')
        if directory_path:  # Only update the directory path if a directory was selected
            self.path_edit.setText(directory_path)

    def unzip_livp_process(self):
        livp_path = self.path_edit.text()
        unzip_path = livp_path + '/unzip'
        if not os.path.exists(unzip_path):
            os.makedirs(unzip_path)
        if not livp_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        img_list = [img for img in os.listdir(livp_path) if img.lower().endswith('.livp')]
        for img_item in tqdm(img_list):
            print(img_item)
            img_source = os.path.join(livp_path, img_item)
            img_destination = os.path.join(unzip_path, img_item)
            if is_livp(img_item):
                unzip_livp(img_item, img_source, unzip_path)
            else:
                copy_file(img_source, img_destination)
        QMessageBox.information(self, 'Info', '图片处理成功')

    def livp2jpg_process(self):
        livp_path = self.path_edit.text()
        jpg_path = livp_path + '/jpg'
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)
        if not livp_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        img_list = [img for img in os.listdir(livp_path) if img.lower().endswith('.livp')]
        for img_item in tqdm(img_list):
            print(img_item)
            img_source = os.path.join(livp_path, img_item)
            img_destination = os.path.join(jpg_path, img_item)
            if is_livp(img_item):
                livp_to_jpg(img_item, img_source, jpg_path)
            else:
                copy_file(img_source, img_destination)
        QMessageBox.information(self, 'Info', '图片处理成功')

    def heic2jpg_proccess(self):
        heic_path = self.path_edit.text()
        jpg_path = heic_path + '/jpg'
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)
        if not heic_path:
            QMessageBox.warning(self, 'Warning', '未选择路径')
            return
        img_list = [img for img in os.listdir(heic_path) if img.lower().endswith('.heic')]
        for img_item in tqdm(img_list):
            print(img_item)
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
    app.setApplicationName("IOS 照片处理")
    window = MainWindow()
    window.show()
    app.exec_()
