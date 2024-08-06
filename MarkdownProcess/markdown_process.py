import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path_label = QLabel("文件路径:", self)
        self.file_path_edit = QLineEdit(self)
        self.level_label = QLabel("提取层级:", self)
        self.level_edit = QLineEdit(self)
        self.level_edit.setText("6")  # 设置默认值为6
        self.open_button = QPushButton('选择文件', self)
        self.process_button = QPushButton('提取大纲', self)
        self.export_button = QPushButton('生成表格', self)
        self.open_button.clicked.connect(self.open_file)
        self.process_button.clicked.connect(self.process_file)
        self.export_button.clicked.connect(self.export_to_excel)

        layout = QVBoxLayout(self)
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.file_path_edit)
        layout.addWidget(self.level_label)
        layout.addWidget(self.level_edit)
        layout.addWidget(self.open_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.export_button)

        self.setAcceptDrops(True)
        self.resize(600, 400)

        self.setWindowTitle("Markdown 大纲提取")  # 设置窗口标题

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Markdown Files (*.md)')
        if file_path:  # Only update the file path if a file was selected
            self.file_path_edit.setText(file_path)

    def process_file(self):
        file_path = self.file_path_edit.text()
        if not file_path:
            QMessageBox.warning(self, 'Warning', '未选择文件')
            return
        self.save_outline(file_path)
        QMessageBox.information(self, 'Info', '文件处理成功')

    def save_outline(self, md_path):
        dir_name = os.path.dirname(md_path)
        base_name = os.path.basename(md_path)
        name, ext = os.path.splitext(base_name)
        new_file_name = f"{name}_outline{ext}"
        new_file_path = os.path.join(dir_name, new_file_name)

        level = int(self.level_edit.text())

        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(new_file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith('#'):
                    # Count the number of '#' at the start of the line
                    count = len(line) - len(line.lstrip('#'))
                    if count <= level:
                        f.write(line)

    def export_to_excel(self):
        file_path = self.file_path_edit.text()
        if not file_path:
            QMessageBox.warning(self, 'Warning', '未选择文件')
            return

        outline_path = self.get_outline_path(file_path)
        if not os.path.exists(outline_path):
            self.save_outline(file_path)

        self.save_to_excel(outline_path)
        QMessageBox.information(self, 'Info', '表格文件生成成功')

    def get_outline_path(self, md_path):
        dir_name = os.path.dirname(md_path)
        base_name = os.path.basename(md_path)
        name, ext = os.path.splitext(base_name)
        new_file_name = f"{name}_outline{ext}"
        return os.path.join(dir_name, new_file_name)

    def save_to_excel(self, outline_path):
        pass

    # TODO:保存文件名，重名处理，点击没选择文件处理，自动调整列宽

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_path_edit.setText(file_path)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W and event.modifiers() & Qt.ControlModifier:
            self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Markdown 大纲提取")
    window = MainWindow()
    window.show()
    app.exec_()
