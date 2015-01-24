#!/usr/bin/python

import xlrd
import urllib
from pyquery import PyQuery as pq
import csv
from urlparse import urljoin, urlparse

#open the xls
imgXlsPath = '/home/jason/projects/learning-gist/python/product-img/img-to-download.xls'
book = xlrd.open_workbook(imgXlsPath)
firstSheet = book.sheet_by_index(0)

totalRows = len(firstSheet.col_values(0))

imgDir = '/home/jason/projects/learning-gist/python/product-img/'
searchPage = 'http://www.sigmaaldrich.com/catalog/search?interface=CAS%20No.&term='

csvFile = open('/home/jason/projects/learning-gist/python/product-img/result.csv', 'w')
csvWriter = csv.writer(csvFile,quoting=csv.QUOTE_MINIMAL)

#loop the rows
for row in xrange(1,totalRows):
	#get the product name, id, img name
	productId = firstSheet.cell_value(row, 0)
	productCAS = firstSheet.cell_value(row, 1)
	productImgUrl = firstSheet.cell_value(row, 2)

	isImgGot = False

	#fetch the search page
	page = pq(url=searchPage+productCAS)
	aTag = page('.product-listing-outer .productNumberValue a').eq(0)
	aHref = aTag.attr('href')
	if aHref is not None:
		print 'dowloading product ', productId
		#get the final url, and go into it.
		pUrl = urljoin(searchPage, aHref)
		pPage = pq(url=pUrl)
		#get the image url, and save it to local
		imgUri = pPage('.prodImage img').attr('src')
		if imgUri is not None:
			imgUrl = urljoin(searchPage, imgUri)
			urllib.urlretrieve(imgUrl, imgDir+productImgUrl)
			isImgGot = True

	# save the result, downloaded or not
	csvWriter.writerow([productId, isImgGot])
	
csvFile.close()
print 'Over'

