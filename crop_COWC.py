'''
Crops the Cars Overhead with Context extracted files into jpeg images.

Inputs:
Directory containing extracted COWC images (subdirectories of COWC/extracted/)
Columbus_CSUAV_AFRL/, Potsdam_ISPRS/, Selwyn_LINZ/, etc.
N.B. All input .jpg files in must have unique file names.

Outputs: 
Cropped JPEGs -> /cropped_jpegs

David Yu Aug 2, 2018
'''
import os
import cv2

IMAGE_SIZE = 600.0 # All COWC images are of this size

# path to input COWC/extracted/subdir/
inpath = '/your/path/extracted/Columbus_CSUAV_AFRL'

if __debug__:
	outpath = '/your/path/COWC/cropped_jpegs_test'
	outpath_neg = '/your/path/COWC/cropped_jpegs_neg_test'
	print("Running in debug mode...")
	count = 0
else:
	outpath = '/your/path/Jupyter_Proj/COWC/cropped_jpegs'
	outpath_neg = '/your/path/COWC/cropped_jpegs_neg'
	print("Running", end="")
	
for filename in os.listdir(inpath):

	if filename.endswith('.txt'):

		input_file_loc = os.path.join(inpath, filename)
		input_file_jpg = os.path.join(inpath, filename.replace(".txt", ".jpg"))

		if __debug__:
			if count >= 10:
				exit()
			count += 1
			print("\ncurrent count:"+str(count))
			print("Using location input file:"+input_file_loc)
			print("Using jpeg input file:"+input_file_jpg)
		else:
			print(".", end="")

		with open(input_file_loc, 'r') as infile:
			img_counter = 0  # counter for all bounding boxes within an image
			lines = infile.readlines()
			img = cv2.imread(input_file_jpg)

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

				xmin = int(max((x_loc - w/2.0) * IMAGE_SIZE, 0.0))
				ymin = int(max((y_loc - h/2.0) * IMAGE_SIZE, 0.0))
				xmax = int(min((x_loc + w/2.0) * IMAGE_SIZE, IMAGE_SIZE))
				ymax = int(min((y_loc + h/2.0) * IMAGE_SIZE, IMAGE_SIZE))

				xmin_neg = int(xmin - 1.5 * (xmax-xmin))
				xmax_neg = int(xmax - 1.5 * (xmax-xmin))
				ymin_neg = int(ymin - 1.5 * (ymax-ymin))
				ymax_neg = int(ymax - 1.5 * (ymax-ymin))
				if xmin_neg <= 0:
					xmin_neg = int(xmin + 1.5 * (xmax-xmin))
					xmax_neg = int(xmax + 1.5 * (xmax-xmin))
				if ymin_neg <= 0:
					ymin_neg = int(ymin + 1.5 * (ymax-ymin))
					ymax_neg = int(ymax + 1.5 * (ymax-ymin))

				crop_img = img[ymin:ymax, xmin:xmax]
				crop_img_neg = img[ymin_neg:ymax_neg, xmin_neg:xmax_neg]
				outfile = os.path.join(outpath, filename.replace(".txt", ""))
				outfile_neg = os.path.join(outpath_neg, filename.replace(".txt", ""))
				cv2.imwrite(outfile+"-"+str(img_counter)+".jpg", crop_img)
				cv2.imwrite(outfile_neg+"-neg-"+str(img_counter)+".jpg", crop_img_neg)
				img_counter += 1