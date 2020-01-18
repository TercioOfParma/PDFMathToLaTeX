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

mathchar = ['+', '-', '*', '/', '\u00F7']
removechar = ['\t', '\n', '.', ',', ';', ':']

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

print(text)

pageLength = len(text)

i = 0
testString = ""
spacing = 3

for rchr in removechar:
	text.replace(rchr, ".")
while i < pageLength:
	if i > spacing and i < (pageLength - spacing):
		print(str(i - spacing) + " to " + str(i+spacing))
		testString = text[i-spacing:i+spacing]
	elif i <= spacing:
		print("To" + str(i+spacing))
		testString = text[:i+spacing]
	else:
		print("From" + str(i-spacing))
		testString = text[i-spacing:]
	isMaths = isCharacterMaths(testString)
	if isMaths == False:
		text = text[:i] + "." + text[i+1:]
	i = i + 1
	#print("Text " + str(i) + " :" + text)

formulae = text.split(".")

print("New Text: ")
formulae = list(filter(None, formulae))
print(formulae)

for formula in formulae:
	output = output + "$" + formula + "$" + "\n"

outputFile = open("output.tex", "w")

output = output + "\\end{document}"

outputFile.write(output)

fp.close()
outputFile.close()
