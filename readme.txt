##
##   Raster Editor 
##
##   Written by Mikhail Vasilev, 2017 
##

This is a demo of a tile-based image editor written in Python. 
You can draw objects using a set of tiles and create various cool geometrical patterns. 
Currently there are only some basic functions supported. 
To customize the tilesets or to extend the functionality, edit the source code.

** Start ** 

Tested with Python 3.6.4 on Windows 10, but probably can run on any OS. 
You'll need 3d party libs: Numpy and Pygame. 
Libraries installation with pip:
> pip install numpy
> pip install pygame

To run the app: 
> python raster.py

To open a saved file, e.g. "file01.txt" :
> python raster.py file01.txt

By default it will open the "untitled00.txt" file. 
Documents are stored as an 2-D array in a txt file.


** How to draw **

Click on a tile in the top palette bar, or right-click on any canvas cell to 
select a tile. Then draw in the main window area.

Draw: 			left click
Eydropper:			right click
Pan:   			Space
Selection:  		Shift + leftclick / rightclick
Reset selection:  	w
Copy:  			c 
Paste:			v 
Fill selection:  		F1
Save file:  		F10
Revert file:  		F5
Export as .png:  		F11
Show/hide grid: 		t 

