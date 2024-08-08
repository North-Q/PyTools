import os
import shutil
import zipfile

import pillow_heif
from PIL import Image


def copy_file(source_path, des_path):
    if not os.path.exists(des_path):
        shutil.copy2(source_path, des_path)


def is_livp(file_name):
    return os.path.splitext(file_name)[-1].lower() == ".livp"


def read_image_file_rb(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


def unzip_livp(img_item, img_source, des_dir):
    img_id = os.path.splitext(img_item)[0]
    livp_zip_name = os.path.join(des_dir, img_id + '.zip')
    copy_file(img_source, livp_zip_name)  # Copy file as zip archive
    heic_name = ''
    with zipfile.ZipFile(livp_zip_name) as zf:
        for zip_file_item in zf.namelist():
            zf.extract(zip_file_item, des_dir)
            if zip_file_item.lower().endswith('.heic'):
                heic_name = zip_file_item
    os.remove(livp_zip_name)  # Delete zip file
    heic_img_path = os.path.join(des_dir, heic_name)
    heif_file = pillow_heif.read_heif(heic_img_path)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
    jpg_save_path = os.path.join(des_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")
    os.remove(heic_img_path)  # Delete heic file


def livp_to_jpg(img_item, img_source, livp_to_jpg_dir):
    img_id = os.path.splitext(img_item)[0]
    livp_zip_name = os.path.join(livp_to_jpg_dir, img_id + '.zip')
    copy_file(img_source, livp_zip_name)  # Copy file as zip archive
    heic_name = ''
    with zipfile.ZipFile(livp_zip_name) as zf:
        for zip_file_item in zf.namelist():
            if zip_file_item.lower().endswith('.heic'):
                zf.extract(zip_file_item, livp_to_jpg_dir)
                heic_name = zip_file_item
    os.remove(livp_zip_name)  # Delete zip file
    heic_img_path = os.path.join(livp_to_jpg_dir, heic_name)
    heif_file = pillow_heif.read_heif(heic_img_path)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
    jpg_save_path = os.path.join(livp_to_jpg_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")
    os.remove(heic_img_path)  # Delete heic file


def heic_to_jpg(img_item, img_source, livp_to_jpg_dir):
    img_id = os.path.splitext(img_item)[0]
    heif_file = pillow_heif.read_heif(img_source)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
    jpg_save_path = os.path.join(livp_to_jpg_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")
