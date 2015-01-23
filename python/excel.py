#!/usr/bin/python

import xlwt
import xlrd

def write_price(path, content):
	""" write something to xlsx """
	book = xlwt.Workbook()
	sheet1 = book.add_sheet("Price")
	headers = ['product_id', 'qty', 'price']
	rows = len(content)
	cols = len(headers)
	# write the header
	for x in xrange(cols):
		sheet1.write(0, x, headers[x])

	# write the content
	for row in xrange(1, rows+1):
		for col in xrange(cols):
			sheet1.write(row, col, content[row-1][col])

	# for num in range(4):
	# 	row = sheet1.row(num)
	# 	for index, col in enumerate(cols):
	# 		value = txt % (num, col)
	# 		row.write(index, value)
			#or sheet1.write(row, index, value)
			# or write a value with style
			# style = 'pattern: pattern solid, fore_colour blue;'
       		# sheet.row(0).write(0, value, xlwt.Style.easyxf(style))

	book.save(path)



def open_file(path):
	book = xlrd.open_workbook(path)
	#print book.nsheets # number of sheets
	#print book.sheet_names() # sheet names
	firstSheet = book.sheet_by_index(0)
	#read a row
	firstRow =  firstSheet.row_values(0) 
	colIndexStart =  firstRow.index('1mg')
	totalCols = len(firstRow)

	firstCol = firstSheet.col_values(0)
	totalRows = len(firstCol)
	#print totalRows

	result = []
	for row in xrange(1,totalRows):
		# get product ID
		productId = int(firstSheet.cell_value(row, 0))
		for col in xrange(colIndexStart,totalCols):
			# get this cell's value
			cellValue = firstSheet.cell_value(row, col)
			# if cell's value is not empty
			if isinstance(cellValue, float):
				result.append((productId,firstRow[col], cellValue))

	return result


	#read a cell
	# cell = first_sheet.cell(0,0)
	# print cell
	# print cell.value
	# print first_sheet.row_slice(rowx=0, start_colx=2, end_colx=4)

if __name__ == "__main__":
	content = open_file("/home/jason/projects/python/pricing.xlsx")
	path = "/home/jason/projects/python/pb_attr.xls"
	write_price(path, content)
	print "Over"
