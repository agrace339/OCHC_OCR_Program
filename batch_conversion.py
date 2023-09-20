import sys
import img2pdf

def jpg_to_pdf():
#Converts single JPEG file to a PDF.
	#If no JPEG or TIFF file given, raise error.
	if (len(sys.argv) <= 1):
		raise Exception("No file given.")

	#Take argument from command line as input file.
	input_file = sys.argv[1]
	print(input_file)

	#Open input file and convert to pdf.
	with open("name.pdf","wb") as f:
		f.write(img2pdf.convert(input_file))

def main():
	jpg_to_pdf()

if __name__ == '__main__':
	main()
