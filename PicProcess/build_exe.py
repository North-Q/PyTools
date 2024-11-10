# build_exe.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    './main.py',  # Path to the main script
    '--name=图片处理工具',  # Name of the executable
    '--onefile',  # Create a one-file bundled executable
    '--windowed',  # Do not provide a console window for standard I/O
    '--add-data=./batch_move_files.py;PicProcess',  # Include additional files
    '--add-data=./ios_pic_process.py;.',  # Include additional files
    '--icon=app.ico'  # Path to the icon file
])
