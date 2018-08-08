'''
Transfrom COWC dataset & labels into Pascal VOC format
(still requires the use of object_detection's pascal transformation tool:
	python object_detection/dataset_tools/create_pascal_tf_record.py -h)

Inputs:
Directory containing extracted COWC images (subdirectories of COWC/extracted/)
Columbus_CSUAV_AFRL/, Potsdam_ISPRS/, Selwyn_LINZ/, etc.
N.B. All input .jpg files in must have unique file names.

Outputs: 
Annotation XMLs -> conversion_to_Pascal_VOC/Annotations

David Yu Jul 9, 2018
'''
import os

IMAGE_SIZE = 600.0

# path to input COWC/extracted/subdir/
inpath = '/COWC/extracted/Vaihingen_ISPRS'

# path to where the actual JPEG imgs will be stored for training
inpath2 = '/your/path/VOC2012/JPEGImages'

if __debug__:
	outpath = '/your/path/COWC/test'
	print("Running in debug mode...")
	count = 0
else:
	outpath = '/your/path/VOC2012/Annotations'
	print("Running", end="")
	
for filename in os.listdir(inpath):

	if filename.endswith('.txt'):

		input_file = os.path.join(inpath, filename)
		input_file2 = os.path.join(inpath2, filename)
		output_file = os.path.join(outpath, filename.replace(".txt", ".xml"))

		if __debug__:
			if count >= 10:
				exit()
			count += 1
			print("\ncurrent count:"+str(count))
			print("Using input_file:"+input_file)
			print("Using output_file:"+output_file)
		else:
			print(".", end="")

		with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:

			outfile.write("<annotation>\n")
			outfile.write("\t<folder>VOC2012</folder>\n")
			outfile.write("\t<filename>"+filename.replace(".txt", ".jpg")+"</filename>\n")
			outfile.write("\t<path>"+input_file2.replace(".txt", ".jpg")+"</path>\n")
			outfile.write("\t<source>\n")
			outfile.write("\t\t<database>Unknown</database>\n")
			outfile.write("\t</source>\n")
			outfile.write("\t<size>\n")
			outfile.write("\t\t<width>600</width>\n")
			outfile.write("\t\t<height>600</height>\n")
			outfile.write("\t\t<depth>3</depth>\n")
			outfile.write("\t</size>\n")
			outfile.write("\t<segmented>0</segmented>\n")

			lines = infile.readlines()
			if __debug__:
				print("input line:"+str(lines))

			for obj in lines:
				if __debug__:
					print("Extracting object:"+obj)

				items = obj.split(" ")
				x_loc = float(items[1])
				y_loc = float(items[2])
				h = float(items[3])
				w = float(items[4])

				xmin = max((x_loc - w/2.0) * IMAGE_SIZE, 0.0)
				ymin = max((y_loc - h/2.0) * IMAGE_SIZE, 0.0)
				xmax = min((x_loc + w/2.0) * IMAGE_SIZE, IMAGE_SIZE)
				ymax = min((y_loc + h/2.0) * IMAGE_SIZE, IMAGE_SIZE)

				outfile.write("\t<object>\n")
				outfile.write("\t\t<name>car</name>\n")
				outfile.write("\t\t<pose>Unspecified</pose>\n")
				outfile.write("\t\t<truncated>0</truncated>\n")
				outfile.write("\t\t<difficult>0</difficult>\n")
				outfile.write("\t\t<bndbox>\n")
				outfile.write("\t\t\t<xmin>"+str(xmin)+"</xmin>\n")
				outfile.write("\t\t\t<ymin>"+str(ymin)+"</ymin>\n")
				outfile.write("\t\t\t<xmax>"+str(xmax)+"</xmax>\n")
				outfile.write("\t\t\t<ymax>"+str(ymax)+"</ymax>\n")
				outfile.write("\t\t</bndbox>\n")
				outfile.write("\t</object>\n")

			outfile.write("</annotation>\n")
