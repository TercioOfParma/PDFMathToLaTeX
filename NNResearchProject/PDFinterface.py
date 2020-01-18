from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

from keras.models import Sequential
from keras.layers import Dense
from functions import convert_dic_to_vector
from config import max_letters, language_tags
import numpy as np

network = Sequential()
network.add(Dense(200, input_dim=128*max_letters - 1, activation='sigmoid'))
network.add(Dense(150, activation='sigmoid'))
network.add(Dense(100, activation='sigmoid'))
network.add(Dense(100, activation='sigmoid'))
network.add(Dense(len(language_tags), activation='softmax'))
network.load_weights('weightslang.hdf5')
network.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])


'''
	1. Grab the entire PDF, and place it in text
	2. Split under the following circumstances
		- " "
		- "."
		- ","
		- ":"
		- ";"
		- """
		- The Symbol currently holding this comment
	3. Feed it into the Neural Network
	4. If the value is, between all, in excess of 10%, dump it
	5. This should leave a nice looking mathematical list

'''
'''
fp = open('mypdf.pdf', 'rb')

parser = PDFParser(fp)

document = PDFDocument(parser, password)

if not document.is_extractable:
	raise PDFTextExtractionNotAllowed
rsrcmgr = PDFResourceManager()

device = PDFDevice(rsrcmgr)

interpreter = PDFPageInterpreter(rsrcmgr, device)


for page in PDFPage.create_pages(document):
	interpreter.process_page(page)

'''

testcase = ["This", "Is", "2+1", "Test"]


print("Working")


i = 1


for stri in testcase:
	print(str(i) + ":" +  stri + "\n")
	vct_str = convert_dic_to_vector(stri, max_letters)
	vct = np.zeros((1, 128* max_letters - 1))
	count = 0
	for digit in vct_str[0]:
		if count == 128 * (max_letters - 1):
			break
		vct[0,count] = int(digit)
		count += 1
	prediction_vct = network.predict(vct)
	langs = list(language_tags.keys())
	for j in range(len(language_tags)):
		lang = langs[j]
		score = prediction_vct[0][j]
		print(lang + ': ' + str(round(100*score, 2)) + '%')
	print('\n')
	i = i + 1

