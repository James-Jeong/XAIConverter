# -*- coding: utf-8 -*-
# XTIConverter.py
# author: jamesj

import os
import sys
from openpyxl import load_workbook
import configparser

# ----------------------------------------------------------------------------------------- #
# 1) Get Parameters
xlsxPath = None
sheetName = None
iniPath = None

# 1-1) Config mode
if len(sys.argv) == 2:
	print("\n@ Config mode")
	print("- Loading config...")

	converterConfigPath = sys.argv[1]
	if not os.path.exists(converterConfigPath) or not os.path.isfile(converterConfigPath):
		print("! Fail to load the program's config file. (name=" + converterConfigPath + ")\n")
		sys.exit()

	converterConfig = configparser.ConfigParser()
	converterConfig.optionxform = lambda option: option # Preserve case for letters
	converterConfig.read(converterConfigPath)
	
	if not converterConfig.has_section("PATH"):
		print("! Fail to load the section \"PATH\". (name=" + converterConfigPath + ")\n")
		sys.exit()
	if not converterConfig.has_section("XLSX"):
		print("! Fail to load the section \"XLSX\". (name=" + converterConfigPath + ")\n")
		sys.exit()

	xlsxPath = converterConfig.get("PATH", "XLSX_PATH")
	if xlsxPath is None or len(xlsxPath) == 0:
		print("! Fail to load the option \"XLSX_PATH\" in the section \"PATH\". (name=" + converterConfigPath + ")\n")
		sys.exit()

	iniPath = converterConfig.get("PATH", "INI_PATH")
	if iniPath is None or len(iniPath) == 0:
		print("! Fail to load the option \"INI_PATH\" in the section \"PATH\". (name=" + converterConfigPath + ")\n")
		sys.exit()

	sheetName = converterConfig.get("XLSX", "SHEET_NAME")
	if sheetName is None or len(sheetName) == 0:
		print("! Fail to load the option \"SHEET_NAME\" in the section \"XLSX\". (name=" + converterConfigPath + ")\n")
		sys.exit()

# 1-2) Parameter mode
elif len(sys.argv) == 4:
	print("\n@ Parameter mode")
	print("- Loading parameters...")

	xlsxPath = sys.argv[1]
	if len(xlsxPath) == 0:
		print("! Fail to load the xslx path.\n")
		sys.exit()

	sheetName = sys.argv[2]
	if len(sheetName) == 0:
		print("! Fail to load the sheet name.\n")
		sys.exit()

	iniPath = sys.argv[3]
	if len(iniPath) == 0:
		print("! Fail to load the ini path.\n")
		sys.exit()

else:
	print("\n! Parameter error.")
	print("argv[0]: XTIConverter.py\n")
	print("1) Config mode")
	print("argv[1]: {config path}\n")
	print("2) Parameter mode")
	print("argv[1]: {xlsx path}")
	print("argv[2]: {xlsx sheet name}")
	print("argv[3]: {ini path}\n")
	sys.exit()

print("\n@ XLSX Path: [ " + xlsxPath + " ]")
print("@ Sheet Name: [ " + sheetName + " ]")
print("@ INI Path: [ " + iniPath + " ]")

xlsxName, xlsxExtension = os.path.splitext(xlsxPath)
if xlsxExtension != ".xlsx":
        print("! XLSX File type is wrong. (ext=" + xlsxExtension + ")\n")
        sys.exit()

iniName, iniExtension = os.path.splitext(iniPath)
if iniExtension != ".ini":
        print("! INI File type is wrong. (ext=" + iniExtension + ")\n")
        sys.exit()

# ----------------------------------------------------------------------------------------- #
# 2) Check xlsx path
if not os.path.exists(xlsxPath) or not os.path.isfile(xlsxPath):
	print("! Unknown XLSX Path.\n")
	sys.exit()

# ----------------------------------------------------------------------------------------- #
# 3) Load xlsx
load_wb = load_workbook(xlsxPath, data_only = True)
load_ws = load_wb[sheetName]

# 3-1) Parsing
print("\n- Loading xlsx...\n")
all_values = []
for row in load_ws.rows:
	row_value = []
	for cell in row:
		if cell.value is None:
			break
		row_value.append(str(cell.value).strip())
	all_values.append(row_value)

# 3-2) Check result
if len(all_values) <= 1:
	print("! Fail to load. The file is empty.\n")
	sys.exit()
else:
	for row in all_values:
		if len(row) == 0:
			print()
			continue
		if len(row) == 1:
			print("- [" + row[0] + "]")
		elif len(row) == 2:
			print("	- " + row[0] + ": " + row[1])
		else:
			print(row)
	print("\n- Success to load.")

# ----------------------------------------------------------------------------------------- #
# 4) Make & Write ini file
config = configparser.ConfigParser()
config.optionxform = lambda option: option # Preserve case for letters

# 4-1) Parsing
curSection = None
for row in all_values:
	row_value = []
	for cell in row:
		row_value.append(cell)
	# 1. Row 에 section 이 있는 경우
	if len(row_value) == 1:
		curSection = row_value[0]
		config.add_section(curSection)
	# 2. Row 에 key, value 가 있는 경우
	elif len(row_value) == 2 and curSection is not None:
		config.set(curSection, row_value[0], row_value[1])
	# 3. Row 가 비었거나 ini 형식과 일치하지 않는 경우
	else:
		curSection = None

if curSection is None:
	print("! Fail. Not found any section.\n")
	sys.exit()

# 4-2) Writing
with open(iniPath, 'w', encoding='utf8') as configfile:
	config.write(configfile)

# 4-3) Check result
if os.path.exists(iniPath):
	print("\n@ Done.\n")
else:
	print("\n! Fail.\n")

