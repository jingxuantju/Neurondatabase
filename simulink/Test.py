import random
import xlwt
comp = [[0 for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        a =  random.randint(0, 8)
        comp[i][j] = a

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Sheet")

for i in range(len(comp)):
    for j in range(len(comp[i])):
        sheet.write(i, j, comp[i][j])

workbook.save("test.xls")
