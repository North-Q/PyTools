import os
import shutil

import openpyxl


def get_file_names(target_dir, xlsx_file='file_names.xlsx'):
    """List all files in the target directory and save their names and extensions to an Excel file."""
    all_items = os.listdir(target_dir)
    file_names = [item for item in all_items if os.path.isfile(os.path.join(target_dir, item))]

    wb = openpyxl.Workbook()
    ws = wb.active

    ws['A1'] = 'File Name'
    ws['B1'] = 'Extension'

    for index, file_name in enumerate(file_names, start=2):
        base_name, extension = os.path.splitext(file_name)
        ws[f'A{index}'] = base_name
        ws[f'B{index}'] = extension

    wb.save(os.path.join(target_dir, xlsx_file))


def move_files(file_name_table, target_dir, source_dir):
    """Move files listed in the Excel file from the source directory to the target directory."""
    wb = openpyxl.load_workbook(file_name_table)
    ws = wb.active

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for row in ws.iter_rows(min_row=2, values_only=True):
        file_name, extension = row
        if not extension.startswith('.'):
            extension = '.' + extension
        full_file_name = f"{file_name}{extension}"

        source_path = os.path.join(source_dir, full_file_name)
        target_path = os.path.join(target_dir, full_file_name)

        if os.path.exists(source_path):
            shutil.move(source_path, target_path)
