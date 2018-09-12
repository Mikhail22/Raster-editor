# Raster-editor
 

### Start

Tested with Python 3.6.4 on Windows 10, but probably can run on any OS. 
You'll need 3d party libs: Numpy and Pygame. 
Installation with pip:
> pip install numpy
> pip install pygame

To run the app: 
> python raster.py

To open a saved file, e.g. "file01.txt" :
> python raster.py file01.txt

By default it will open the "untitled00.txt" file. 
Documents are stored as an 2-D array in a txt file.


### How  to  draw

Click on a tile in the top palette bar, or right-click on any canvas cell to 
select a tile to draw. Then draw in the main window area.

Draw: 					left click
Eydropper:			right click
Pan:   					Space
Selection:  			Shift + leftclick / rightclick
Reset selection:  	w
Copy:  				c 
Paste:					v 
Fill selection:  		F1
Save file:  			F10
Revert file:  			F5
Export as .png:  		F11
Show/hide grid: 		t 
