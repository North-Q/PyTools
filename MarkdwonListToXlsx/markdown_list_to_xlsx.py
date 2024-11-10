import re

from openpyxl import Workbook
from openpyxl.styles import Font


def parse_markdown(md_file):
    with open(md_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    current_module = None
    current_description = []
    only_uorb = 0
    unrelated_to_drone = 0
    code_lines = 0

    for line in lines:
        line = line.strip()
        if line.startswith('- **`') and '：' in line:
            if current_module:
                data.append([current_module, only_uorb, unrelated_to_drone, code_lines, ' '.join(current_description)])
            current_module = re.search(r'\*\*`(.*?)`\*\*', line).group(1)
            description = line.split('：', 1)[1].strip()
            current_description = [description]
            only_uorb = 0
            unrelated_to_drone = 0
            code_lines = 0
        elif line.startswith('- '):
            if '仅依赖`uORB`' in line:
                only_uorb = 1
            elif '与多旋翼无人机无关' in line:
                unrelated_to_drone = 1
            elif '代码量：' in line:
                code_lines = int(re.search(r'代码量：(\d+)', line).group(1))
            else:
                current_description.append(line[2:])

    if current_module:
        data.append([current_module, only_uorb, unrelated_to_drone, code_lines, ' '.join(current_description)])

    return data


def write_to_excel(data, output_file):
    wb = Workbook()
    ws = wb.active
    headers = ['模块', '是否仅依赖uORB', '是否仅与多旋翼无人机有关', '代码量', '备注']
    ws.append(headers)

    # Apply bold font to headers
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in data:
        ws.append(row)

    # Adjust column widths
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    wb.save(output_file)


if __name__ == '__main__':
    md_file = 'PX4_Module.md'
    output_file = 'output.xlsx'
    data = parse_markdown(md_file)
    write_to_excel(data, output_file)
    print(f"Data written to {output_file}")
