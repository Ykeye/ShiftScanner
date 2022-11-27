import openpyxl

wb = openpyxl.load_workbook("./shifts.xlsx")
sheet = wb['Лист1']

print(sheet['C1'].value)

