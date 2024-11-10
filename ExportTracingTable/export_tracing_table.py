''' 以下为用例：
任务名称：高低压切换控制（无N2双通道传感器故障）
编号：R_10254
追溯：1.3.高低压切换控制[R_10254]
功能：当无N2双通道传感器故障，控制模式应按以下逻辑设置：
a)	发动机状态为慢车状态，应用软件应设置控制模式为高压控制模式，置N2R25最终控制目标N2r25Dmd = N2R25Dem，置N1R最终控制目标N1rDmd = N1RDem。[C-10205]
b)	发动机状态为慢车以上状态，且处于转换逻辑一过程中，应用软件应按照转换逻辑一控制。[C-10206]
c)	发动机状态为慢车以上状态，且处于转换逻辑二过程中，应用软件应按照转换逻辑二控制。[C-10246]
d)	发动机状态为慢车以上状态，PLA不处于慢车域，且不处于转换逻辑一、二过程中，应用软件应设置控制模式为低压控制模式，置N1R最终控制目标N1rDmd = N1RDem，置N2R25最终控制目标N2r25Dmd = N2R25Dem。[C-10248]
e)	发动机状态为慢车以上状态，PLA处于慢车域，且不处于转换逻辑一、二过程中，应用软件应设置控制模式为高压控制模式，置N2R25最终控制目标N2r25Dmd = N2R25Dem，置N1R最终控制目标N1rDmd = N1RDem。[C-10349]
f)	发动机状态为高转速风车起动状态，选定推力等级为反推慢车、地面慢车、空中慢车、进近慢车以外的等级，应用软件应设置控制模式为低压控制模式，置N1R最终控制目标N1rDmd = N1RDem，置N2R25最终控制目标N2r25Dmd = N2R25Dem。[C-11939]
g)	发动机状态为高转速风车起动状态，选定推力等级为反推慢车、地面慢车、空中慢车、进近慢车，应用软件应设置控制模式为高压控制模式，置N2R25最终控制目标N2r25Dmd = N2R25Dem，置N1R最终控制目标N1rDmd = N1RDem。[C-11938]
h)	发动机状态为慢车状态和慢车以上、高转速风车起动状态以外的其它状态，应用软件应设置控制模式为高压控制模式，置N2R25最终控制目标N2r25Dmd = N2R25Dem，置N1R最终控制目标N1rDmd = N1RDem。[C-10471]
前置条件：N2_dual_channel_sensor_fault_flag == false
输入：engine_state, PLA, thrust_level, N2R25Dem, N1RDem, software_control_mode , PD_IdleSwitchPlaThsld
输出：N2r25Dmd, N1rDmd, software_control_mode
公式：
if(engine_state == ES_idle)
{
		software_control_mode = High_Press_Control_Mode;
		N2r25Dmd = N2R25Dem;
		N1rDmd = N1RDem;
}

if(engine_state == ES_above_idle && ((PLA<2 + PD_IdleSwitchPlaThsld && PLA>2) && (last(PLA)<=2 && last(PLA)>=0)) || ((PLA>-6-PD_IdleSwitchPlaThsld && PLA<-6) && (last(PLA)<0 && last(PLA)>-6)))
{
			software_control_mode = Logic1_Control_Mode;
}

if(engine_state == ES_above_idle && (PLA<0 && PLA >=-6 && last(PLA)>=-33 && last(PLA)<-6 || PLA<=2 && PLA >=0 && last(PLA)>2 && last(PLA)<=85))
{
			software_control_mode = Logic2_Control_Mode;
}

if(engine_state == ES_above_idle && (PLA >= 2 + PD_IdleSwitchPlaThsld || PLA <= 2 || last(PLA) > 2 || last(PLA) < 0) && (PLA <= -6 - PD_IdleSwitchPlaThsld || PLA >= -6 || last(PLA) >= 0 || last(PLA) <= -6) && (PLA < -6 || PLA > 2))
{
			software_control_mode = Low_Press_Control_Mode;
N1rDmd = N1RDem;
N2r25Dmd = N2R25Dem;
}

if(engine_state == ES_above_idle && ((PLA >= 2 + PD_IdleSwitchPlaThsld || PLA <= 2 || last(PLA) > 2 || last(PLA) < 0) && (PLA <= -6 - PD_IdleSwitchPlaThsld || PLA >= -6 || last(PLA) >= 0 || last(PLA) <= -6) && (PLA >= 0 || PLA < -6 || last(PLA) < -33 || last(PLA) >= -6) && (PLA > 2 || PLA < 0 || last(PLA) <= 2 || last(PLA) > 85) && PLA <= 2 && PLA >= -6))
{
			software_control_mode = High_Press_Control_Mode;
N1rDmd = N1RDem;
N2r25Dmd = N2R25Dem;
}

if(engine_state == ES_Hwindmill_start && thrust_level != level_RI && thrust_level != level_GI && thrust_level != level_FI && thrust_level != level_AI)
{
			software_control_mode = Low_Press_Control_Mode;
N1rDmd = N1RDem;
N2r25Dmd = N2R25Dem;
}

if(engine_state == ES_Hwindmill_start && thrust_level == level_RI && thrust_level == level_GI && thrust_level == level_FI && thrust_level == level_AI)
{
			software_control_mode = High_Press_Control_Mode;
N1rDmd = N1RDem;
N2r25Dmd = N2R25Dem;
}

if(engine_state != ES_Hwindmill_start && engine_state != ES_above_idle && engine_state != ES_idle)
{
			software_control_mode = High_Press_Control_Mode;
N1rDmd = N1RDem;
N2r25Dmd = N2R25Dem;
}
'''
# 功能需求：
# 1.读取Module.docx文档，该文档包含多个module（每一个的格式都与上述用例类似）；
# 2.对于每一个“module”，执行如下操作：
#  a.将“编号：”后的编号（形如“R_10254”）存储为“formal_requirement_number”
#  b.读取“追溯：”之后，“前置条件：”之前的内容，识别出所有"[""]"之内的编号（例如[R_10254]），将编号（不包括"[]"）存入“natural_language_requirement_number_array”
#  c.将“formal_requirement_number”存入输出文件“TracingTable.xlsx”文件的第一列，将“natural_language_requirement_number_array”存入第二列（若有多个编号在数组中以“、”分割）


import re
from docx import Document
import openpyxl

def extract_requirements(docx_path, xlsx_path):
    # Open the DOCX file
    doc = Document(docx_path)

    # Create a new Excel workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active

    # Set the headers for the Excel file
    ws.append(["formal_requirement_number", "natural_language_requirement_number_array"])

    # Initialize variables
    formal_requirement_number = None
    trace_text = ""

    # Iterate through all paragraphs in the document
    for para in doc.paragraphs:
        text = para.text.strip()

        # Check if the paragraph starts with "编号："
        if text.startswith("编号："):
            formal_requirement_number = text.split("：")[1].strip()

        # Check if the paragraph starts with "追溯："
        elif text.startswith("追溯："):
            trace_text = text.split("：")[1].strip()

        # Continue collecting trace text until "前置条件：" is found
        elif trace_text and not text.startswith("前置条件："):
            trace_text += " " + text

        # When "前置条件：" is found, process the collected trace text
        elif text.startswith("前置条件：") and trace_text:
            # Extract valid requirement numbers and replace hyphens with underscores
            natural_language_requirement_number_array = re.findall(r'\b[A-Z][-_]\d+\b', trace_text)
            natural_language_requirement_number_array = [num.replace('-', '_') for num in natural_language_requirement_number_array]
            natural_language_requirement_number_array = "、".join(natural_language_requirement_number_array)

            # Append the extracted data to the Excel file
            ws.append([formal_requirement_number, natural_language_requirement_number_array])

            # Reset trace_text for the next module
            trace_text = ""

    # Save the Excel file
    wb.save(xlsx_path)

# Example usage
extract_requirements('./Module.docx', './TracingTable.xlsx')