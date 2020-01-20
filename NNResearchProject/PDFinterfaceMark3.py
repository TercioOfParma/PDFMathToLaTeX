from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.layout import LAParams
import math

from keras.models import Sequential
from keras.layers import Dense
from functions import convert_dic_to_vector
from config import max_letters, language_tags
import numpy as np
'''
Mark 2 Plan:
	1: Import PDF. Condense into text
	2: Remove all characters not within 2 spaces of a math character,
	and replace with a space
		2.1: Have a cursor, and generate a substring containing
		the two closest characters both ways
		2.2: Send to isCharacterMath(chars)
		2.3: If there is a math character or string in there,
		return true and keep, else false
		2.4: On false, the character becomes a space
	3: Remove all tabs, carriage returns and funky characters
	4: Split on newlines, spaces, commas and full stops
	5: (If this removes those characters)



'''

network = Sequential()
network.add(Dense(200, input_dim=128*max_letters - 1, activation='sigmoid'))
network.add(Dense(150, activation='sigmoid'))
network.add(Dense(100, activation='sigmoid'))
network.add(Dense(100, activation='sigmoid'))
network.add(Dense(len(language_tags), activation='softmax'))
network.load_weights('weightslang.hdf5')
network.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])



mathchar = ['+', '-', '*', '/', '\u00F7']
removechar = ['\t', '.', ',', ';', ':', '/r']

output = """\\documentclass{article}[11pt]
\\begin{document}
\\title{LaTeX Output}
\\author{PDF Interface}
\\maketitle
\\section{Data}
"""


def isCharacterMaths(mathString):
	print("String Taken in:" + mathString)
	middleChar = mathString[int(math.floor(len(mathString)/2))]
	for rchr in removechar:
		if middleChar == rchr:
			return False
	for chr in mathString:
		for mchr in mathchar:
			if chr == mchr:
				return True
	return False




fp = open('test.pdf', 'rb')

password = ""
params = LAParams()
retstr = StringIO()
rsrcmgr = PDFResourceManager()

device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=params)

interpreter = PDFPageInterpreter(rsrcmgr, device)


for page in PDFPage.get_pages(fp, set(), 0, "", True, check_extractable=True):
        interpreter.process_page(page)

text = retstr.getvalue()

#print(text)

pageLength = len(text)

i = 0
testString = ""
spacing = 3

for rchr in removechar:
        text.replace(rchr, " ")


replaceString = text.split(" ")
i = 0
dic =[]

print(replaceString)
formulae = []
for remove in replaceString:
	dic = []
	dic.append(remove)
	vct_str = convert_dic_to_vector(dic, max_letters)
	vct = np.zeros((1, 128 * max_letters - 1))
	count = 0
	for digit in vct_str[0]:
		if count == 128 * (max_letters - 1):
			break
		vct[0,count] = int(digit)
		count += 1
	prediction_vct = network.predict(vct)

	langs = list(language_tags.keys())
	for i in range(len(language_tags)):
		lang = langs[i]
		score = prediction_vct[0][i]
		print(remove + " " + lang + ': ' + str(round(100*score, 2)) + '%')
		if(lang == "en"):
			if(round(100*score,2) > 10.0):
				print("Removed A Word!")
				break
			else:
				formulae.append(remove)
print("New Text: ")
formulae = list(filter(None, formulae))
print(formulae)

formula = " ".join(formulae)

output = output + "$" + formula + "$"
outputFile = open("output.tex", "w")

output = output + "\\end{document}"

outputFile.write(output)

fp.close()
outputFile.close()

