from PIL import Image
import pytesseract
import pandas
import os
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def makeTextFile(file_name):
	output_name = file_name.split(".")[0] + ".txt"
	print(output_name)
	
	orientation = pytesseract.image_to_osd(Image.open(file_name))
	print(orientation)
	#rotated = imutils.rotate_bound(image, angle=results["rotate"])
	
	text = pytesseract.image_to_data(Image.open(file_name), lang='eng', output_type='data.frame')
	text = text[text.conf != -1]

	lines = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['text'].apply(lambda x: ' '.join(list(x))).tolist()
	confs = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['conf'].mean().tolist()

	line_conf = []
   
	for i in range(len(lines)):
		if lines[i].strip() and confs[i] > 40:
			line_conf.append(lines[i].strip())
	
	with open(output_name, "w") as text_file:
		for line in line_conf:
			text_file.write("".join(line) + "\n")

path = r"/Users/annagrace/Desktop/Python OCR"
dir_list = os.listdir(path)

for i in range(len(dir_list)):
	if ".jpg" in dir_list[i]:
		makeTextFile(dir_list[i])

