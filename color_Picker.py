from unicodedata import name
import cv2
import numpy as np
#import sys
from pyrsistent import b
import webcolors
from scipy.spatial import KDTree
#im1 = Image.open(sys.argv[1])

color_explore = np.zeros((150,150,3), np.uint8)  
color_selected = np.zeros((150,150,3), np.uint8)


# converting rgb to hex
def rgb_to_hex(r, g, b):
  hex = ('{:2X}{:2X}{:2X}').format(r, g, b)
  if("0" not in hex):
    temp=hex.split()
    final="0".join(temp)
    print("Hex Value = ",final)
def rgb_to_hex_file(r, g, b):
  hex = ('{:2X}{:2X}{:2X}').format(r, g, b)
  if("0" not in hex):
    temp=hex.split()
    final="0".join(temp)
    return final


def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = webcolors.CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(webcolors.hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'

#save selected color RGB in file
def write_to_file(R,G,B):
	f = open("saved_color.txt", "a")
	RGB_color= str("The R G B Values is : ")+ str(R) + "," + str(G) + "," + str(B) + str("\n")
	temp = rgb_to_hex_file(R,G,B)
	var = str("The Hex value : ") + str(temp) + str("\n")
	name = convert_rgb_to_names((R, G, B))
	namec = str("The Closest Color Name is : ") + str(name) + str("\n")
	f.write(RGB_color)
	f.write(var)
	f.write(namec)
	f.close()

#Mouse Callback function
def show_color(event,x,y,flags,param): 
	# font
	font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
	org = (x, y)
  
# fontScale
	fontScale = 0.5
   
# Blue color in BGR
	color = (0, 0, 0)
  
# Line thickness of 2 px
	thickness = 1
	
	B=img[y,x,0]
	G=img[y,x,1]
	R=img[y,x,2]
	color_explore [:] = (B,G,R)

	if event == cv2.EVENT_LBUTTONDOWN:
		color_selected [:] = (B,G,R)


	if event == cv2.EVENT_RBUTTONDOWN:
		B=color_selected[0,0,0]
		G=color_selected[0,0,1]
		R=color_selected[0,0,2]
		rgb = (R, G, B)

		#print(webcolors.rgb_to_name((R,G,B)))
		#print("R G B Values = ",R,G,B)
		write_to_file(R,G,B)
		rgb_to_hex(R, G, B)
		name = convert_rgb_to_names((R,G,B))
		cv2.putText(img,str(name), org, font, 
                  fontScale, color, thickness, cv2.LINE_AA)
		#cv2.putText(img,str(rgb), org, font, 
                   #fontScale, color, thickness, cv2.LINE_AA)
		
#live update color with cursor
#cv2.namedWindow('color_explore')
#cv2.resizeWindow("color_explore", 50,50);

#Show selected color when left mouse button pressed
#cv2.namedWindow('color_selected')
#cv2.resizeWindow("color_selected", 50,50);

#image window for sample image
cv2.namedWindow('image')
img_path = 'test1.jpg'

#read sample image
img=cv2.imread(img_path)

#mouse call back function declaration
cv2.setMouseCallback('image',show_color)

#while loop to live update
while (1):
	
	cv2.imshow('image',img)
	#cv2.imshow('color_explore',color_explore)
	#cv2.imshow('color_selected',color_selected)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()