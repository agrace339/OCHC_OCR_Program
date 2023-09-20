import easyocr
import os

def makeTextFile(file_name):
	output_name = file_name.split(".")[0] + ".txt"
	print(output_name)
	
	result = reader.readtext(file_name, detail = 0, rotation_info = [90, 180 ,270], slope_ths = .5, width_ths = .6, height_ths = .6)
	print(result)

reader = easyocr.Reader(['en'], gpu = True)
path = r"/Users/annagrace/Desktop/Python OCR"
dir_list = os.listdir(path)

for i in range(len(dir_list)):
	if ".jpg" in dir_list[i]:
		makeTextFile(dir_list[i])
