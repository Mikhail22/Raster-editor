# Raster Editor v.01
# (C) Mikhail Vasilev 2017

import os
import sys
import pygame
import numpy
from funk import *

def Print_xy(v, x, y) :
	#mark = Font_sys.render(str(v).zfill(5), 1, Col_ink, Col_bg)
	mark = Font_sys.render (str(v).rjust(4), 1, Col_ink, Col_bg)
	DISP.blit (mark, (x, y))

def export_png (fname, A):
	#global q, TILES
	h,w = A.shape
	tmp_surf = pygame.Surface ((w*q, h*q)) 	
	for row in range (0,h):
		for col in range (0,w):
			tmp_surf.blit (TILES [A[row,col]], ( q*col, q*row ) )
	pygame.image.save (tmp_surf, fname)
	del	(tmp_surf)

def Print_xy_c ( v, x, y, fg, bg ) :
	mark = Font_sys.render (str(v).rjust(4), 1, fg, bg )
	DISP.blit (mark, (x, y))

def Print_xy_small ( v, x, y, fg, bg ) :
	mark = Font_sys1.render (str(v).rjust(4), 1, fg, bg )
	DISP.blit (mark, (x, y))

def load_tiles (fname, q, color, col_bg):		# load tile sheet (horizontal)
	tiles = []
	# alpha = load_png_8bit (fname) 			#  
	alpha = load_gray (fname) 					# pygame image.load  
	h, w = alpha.shape
	tmp32 = numpy.zeros ((h, w, 4), dtype="B")
	tmp32 [:] = color
	tmp32 [:, :, 3] = alpha
	print ("loaded set shape:", h, w)
	print ("loaded set dtype:", alpha.dtype)
	amount = w // q
	print ("amount of tiles:", amount )
	print ("check error (0):", w % q )
	#print amount 
	for col in range(0, amount):
		cut = tmp32 [:, q*col:q*(col+1)]
		surf_bg = pygame.Surface ((q, q)) 	
		# surf_bg.fill (col_bg)
		surf = surffromarr (cut)
		surf_bg.blit (surf, (0,0))
		# tiles.append ( surf_bg )
		tiles.append ( surf )
	tt = tuple (tiles)
	del (tiles)
	del (tmp32)
	return tt

def draw_all_tiles():						# draw the tile palette
	global ts_x, ts_y, sp, q, TAM, TILES
	x0 = ts_x + sp
	for i in range (0,TAM):
		DISP.blit (TILES[i], (x0, ts_y))
		pygame.draw.rect (DISP, Col_lgray, (x0-1, ts_y-1, q+2, q+2), 1)
		Print_xy_small (start_row+i, x0-4, ts_y-q, Col_ink2, Col_bg) 
		x0 = x0 + q + sp

def hl_tile (new, prev):					# highlight selected tile 
	w = q + 2
	h = q + 2
	xprev = ts_x + sp + prev * (q + sp)
	xnew = ts_x + sp + new * (q + sp)
	pygame.draw.rect (DISP, Col_lgray, (xprev - 1, ts_y - 1, w, h), 1)
	pygame.draw.rect (DISP, Col_ink, (xnew - 1, ts_y - 1, w, h), 1)
	pygame.draw.rect (DISP, Col_bg, (xprev, ts_y + q + 2, q, q))
	DISP.blit (SPRITES [SP_arrow], (xnew, ts_y + q + 2 ))

def Gen_grid (W, H, q, color):
	s = 3
	ww = W*q; hh = H*q
	ga = numpy.zeros ((hh, ww, 4), dtype = "uint8")			
	p_grid = pygame.Surface ((ww, hh), pygame.SRCALPHA, 32) 
	ga [0:hh:q,::s] = color
	ga [::s,0:ww:q] = color
	ga [0,:] = 0
	ga [hh-1,:] = 0
	ga [:,0] = 0
	ga [:,ww-1] = 0
	put_arr (p_grid, ga)		# copy Raster to Surface
	return p_grid
	#DISP.blit(pig_Raster,(startX, lineY))

def i2v (row, col) :
	t = row - start_row, col - start_col 
	return t
def v2i (row, col) :
	t = row + start_row, col + start_col 
	return t
def ind2rect (row, col, row1, col1, q) :
	t = (col - start_col)*q, (row - start_row)*q, (col1-col)*q, (row1-row)*q
	return t
def show_selection() :
	rec = ind2rect (sel0y,sel0x,sel1y,sel1x,q) 
	#print rec
	pygame.draw.rect (view_surf, Col_red, rec, 1)

def draw_border () :
	rec = (0,0,v_ww,v_hh) 
	pygame.draw.rect (view_surf, Col_lgray, rec, 1)
	if start_row == 0 :
		pygame.draw.line (view_surf, Col_ink2, (0,0),(v_ww,0), 1)
	if start_col == 0 :
		pygame.draw.line (view_surf, Col_ink2, (0,0),(0,v_hh), 1)
	if start_row == start_row_max :
		pygame.draw.line (view_surf, Col_ink2, (0,v_hh-1), (v_ww,v_hh-1), 1)
	if start_col == start_col_max :
		pygame.draw.line (view_surf, Col_ink2, (v_ww-1,0), (v_ww-1,v_hh), 1)

def draw_rulers () :
	for i in range (0,v_h) :
		by = Oy + i*q + 8
		Print_xy_small (start_row+i, Ox-q-10, by, Col_ink2, Col_bg) 
	for j in range (v_w-1,-1,-1) :
		bx = Ox + j*q 
		Print_xy_small (start_col+j, bx, Oy-q+3, Col_ink2, Col_bg) 

def show_center() :
	rec = v_centerx*q+q//2-1, v_centery*q+q//2-1, 3, 3  
	pygame.draw.rect (view_surf, Col_red, rec)

def chck_hover (x, y, xmin, ymin, xmax, ymax):
	hor = x<xmax and x>xmin
	ver = y<ymax and y>ymin
	if hor and ver : return True
	return False

def chck_hover_rect (x,y,xmin,ymin,w,h):
	hor = x<(xmin+w) and x>xmin
	ver = y<ymin+h and y>ymin
	if hor and ver : return True
	return False

def Render_view (A):
	if grid_on :
		view_surf.blit (view_grid_p, (0, 0) )
		# view_surf.blit (view_grid_p, (Ox, Oy) )
	for row in range (0, v_h):
		for col in range (0, v_w):
			view_surf.blit ( TILES[A[row,col]], ( q*col, q*row ) )


#==========\      MAIN      \========== 
ROOT = os.path.dirname (os.path.abspath(__file__))
print ("root dir:", ROOT)
ARG = sys.argv[1:]
proj_file = ROOT + os.sep + "untitled00.txt"
print ("default:", proj_file)
if len(ARG) == 1:
	proj_file = ROOT + os.sep + ARG[0]
	print ("passed: ", proj_file)
proj_png = proj_file[0:-3] + "png"
print ("png file:", proj_png)

pygame.init()
print ("pygame version: ", pygame.version.ver)
window_w = 1000			# display width
window_h = 780				# display height
DISP = pygame.display.set_mode ((window_w, window_h), 0, 32)
pygame.display.set_caption ("Raster editor")
clock = pygame.time.Clock ( ) 
Font_sys = pygame.font.Font (ROOT + os.sep + "CourierStd-Bold.otf", 12)
Font_sys1 = pygame.font.Font (ROOT + os.sep + "CourierStd-Bold.otf", 10)
#================================== Key bindings ====
KQUIT = 			pygame.K_ESCAPE
KSCROLLUP = 			pygame.K_PAGEUP
KSCROLLDOWN = 	pygame.K_PAGEDOWN
KJUMP = 		pygame.K_SPACE
KSETSEL = 		pygame.K_w 
KSELON = 		pygame.K_q
KCOPY = 		pygame.K_c
KPASTE = 		pygame.K_v
KGRIDON = 	pygame.K_t 			# show/hide grid
KGRIDBACK = 	pygame.K_y 			# grid in back/
KFILL = 			pygame.K_F1 		# fill
KST = 			pygame.K_z 			# print mods
KRELOAD = 	pygame.K_F5
KSAVE = 		pygame.K_F10
KEXPORT = 	pygame.K_F11

# - - - - - color constants
Col_ink = 	(17,26,6)					# almost black
Col_ink2 = 	(63,65,57)				# dark
Col_bg = 		(224,222,212)			# background
Col_black = 	(0,0,0)
Col_lgray = 	(187,189,176)			# grey
Col_red = 	(255,10,10)
Col_blue = 	(18,138,154)
Col_orange = (192,122,0)
# - - - - -  colors as arrays
# color_grid = 		numpy.array ([150, 150, 150, 255], "B")
color_grid = 		numpy.array ([170, 170, 160, 255], "B")
color_ink32 = 	numpy.array ([  6,  26,  17, 255], "B")
color_tileface = 	numpy.array ([  6,  26,  17, 255], "B")
color_tilebg =	numpy.array ([  212,  222,  224, 255], "B")
Col_tilebg = 		(224,222,212)		# background

h = 40
w = 60						# canvas array size
#v_h = 10
v_h = 21
v_w = 32 						# view size
v_centery = v_h//2
v_centerx = v_w//2 			# view center cell

q = 25							# square size
#q = 30						# square size

hh = h * q
ww = w * q					# canvas surface size
v_hh = v_h * q
v_ww = v_w * q 				# view surface size

Ox = 140; Oy = 140			# view origin coord
Ex = Ox + v_ww				# right view border
Ey = Oy + v_hh				# bottom view border

ts_x = 220
ts_y = 40						# tileset palette coords
sp = 6							# palette spacing

start_row = 0
start_col = 0					# pan positon 
def setview ():
	global start_row, start_col 
	global end_row, end_col , v_h, v_w
	end_row = start_row + v_h 
	end_col = start_col + v_w 
setview ()

start_row_max = h-v_h
start_col_max = w-v_w		# pan limit 

sel0x = 0
sel0y = 0
sel1x = 1
sel1y = 1						# init selection indices

view_surf = pygame.Surface ((v_ww, v_hh)) 					# view surface 
tiles_fname = ROOT + os.sep +  "tiles_SD12.png" 
sprites_fname = ROOT + os.sep +  "spr0.png" 
TILES = load_tiles (tiles_fname, 25, color_tileface, Col_tilebg) 
TAM = len (TILES)
SPRITES = load_tiles (sprites_fname, q, color_tileface, Col_tilebg) 
SP_arrow = 0							# arrow sprite ID

Canvas = numpy.zeros (( h, w ), dtype = "B" )
selcopy = numpy.copy (Canvas [sel0y:sel1y, sel0x:sel1x]) 
# selcopy = numpy.array ([[0]]) 

if os.path.isfile (proj_file):
	tmp = load_arr (proj_file)
	print ("loaded array size:", tmp.shape)
	blit (Canvas, tmp, 0,0)		 #copy slection
	del (tmp)

view_grid_p = Gen_grid ( v_w, v_h, q, color_grid )
DISP.fill (Col_bg)
draw_all_tiles()
pal_w = (TAM)*(q+sp)
pal_h = q 
DISP.blit (view_grid_p, (Ox, Oy) )
sel_on = False
grid_on = True 
grid_back = True
cur_tile = 0
prev_tile = 0

#================ state init  ================
pygame.event.pump()
key = pygame.key.get_pressed()
key_ = key
msb = pygame.mouse.get_pressed()
msb_ = msb
FPS = 18
MainLoop = True
Running  = True
#================= main loop ======================

while MainLoop :

	if Running : 
		# init running screen
		refresh = True
		refresh_pal = True

		while 1:
			clock.tick (FPS)
			pygame.event.pump()
			key = pygame.key.get_pressed()			# keyboard
			msb = pygame.mouse.get_pressed()		# mouse buttons
			keyd = tuple (x > y for x,y in zip(key, key_)) ;  key_ = key			# keyboard keydown state 
			msbd = tuple (x > y for x,y in zip(msb, msb_)) ;  msb_ = msb		# mouse keydown state
			MODS =  pygame.key.get_mods ()										# mod keys
			Mx, My = pygame.mouse.get_pos ()
			
			Print_xy_c (My, 0, 100, Col_lgray, Col_bg) 
			Print_xy_c (Mx, 40, 100, Col_lgray, Col_bg) 
			Print_xy_c (start_row, 0, 140, Col_orange, Col_bg) 
			Print_xy_c (start_col, 40, 140, Col_orange, Col_bg) 
			
			OMx = Mx - Ox		# mouse view x
			OMy = My - Oy
			v_col = OMx//q		# screen cell 
			v_row = OMy//q 
			C_row, C_col  = v2i (v_row, v_col)		# canvas cell 
			mouse_in = chck_hover (Mx, My, Ox, Oy, Ex, Ey)
			mouse_pal = chck_hover_rect (Mx, My, ts_x + sp//2, ts_y, pal_w, pal_h)
			
			Print_xy_c (v_col, 40, 160, Col_blue, Col_bg) 
			Print_xy_c (v_row, 0, 160, Col_blue, Col_bg) 
			Print_xy_c (C_col, 40, 180, Col_blue, Col_bg) 
			Print_xy_c (C_row, 0, 180, Col_blue, Col_bg) 
			
			if mouse_in : 
				Print_xy (OMy, 0, 120) 
				Print_xy (OMx, 40, 120) 
			if not mouse_in : 
				Print_xy_c (OMy, 0, 120, Col_red, Col_bg) 
				Print_xy_c (OMx, 40, 120, Col_red, Col_bg) 
			if keyd [KQUIT] : 
				Running = False
				MainLoop = False
			if keyd [KST] : 
				print (MODS) 
			if keyd [KSCROLLDOWN] :
				if MODS == 64 : 					#LCTRL
					start_col = up (start_col, 1, start_col_max) 
				else:
					start_row = up (start_row, 1, start_row_max) 
				setview()
				refresh = True
			if keyd [KSCROLLUP] :
				if MODS == 64 : 					#LCTRL
					start_col = dn (start_col, 1, 0) 
				else:
					start_row = dn (start_row, 1, 0) 
				setview()
				refresh = True
			if MODS == 0 : 
				if keyd [KRELOAD] :
					tmp = load_arr (proj_file)
					print ("loaded array size: ", tmp.shape)
					blit (Canvas, tmp, 0,0) #copy slection
					del (tmp)
					refresh = True
				if keyd [KEXPORT] :
					export_png (proj_png, Canvas)
				if keyd [KSAVE] :
					save_arr (proj_file, Canvas)
				if keyd [KSETSEL] :
					sel0y, sel0x = v2i (v_row, v_col)
					sel1y, sel1x = sel0y+1, sel0x+1
					sel_on = True
					refresh = True
				if keyd [KSELON] :
					sel_on = not sel_on
					refresh = True
				if keyd [KGRIDON] :
					grid_on = not grid_on
					refresh = True
				if keyd [KGRIDBACK] :
					grid_back = not grid_back
					refresh = True
				if keyd [KFILL] :		#fill slection
					Canvas [sel0y:sel1y, sel0x:sel1x] = cur_tile 
					refresh = True
				if keyd [KCOPY] : 		#copy slection
					selcopy = numpy.copy (Canvas [sel0y:sel1y, sel0x:sel1x]) 
				if keyd [KPASTE] :		#paste slection
					# if selcopy :
					blit (Canvas, selcopy, C_row, C_col) 
					refresh = True

			if mouse_pal : 
				PMx = Mx - ts_x - sp//2
				#PMy = My - ts_y
				pal_col = PMx // (q+sp)
				Print_xy_c (pal_col, 0, 160, Col_red, Col_bg) 
				Print_xy_c (prev_tile, 40, 160, Col_red, Col_bg) 
				if MODS == 0 :
					if msbd [0] :
						prev_tile = cur_tile
						cur_tile = pal_col
						refresh_pal = True

			if refresh_pal :
				hl_tile(cur_tile, prev_tile)
				refresh_pal = False 

			if mouse_in : 
				if MODS == 0 : 					# No MODS pressed
					if msb [0] :
						Canvas[C_row, C_col] = cur_tile
						refresh = True
					if msb [2] :
						prev_tile = cur_tile
						cur_tile = Canvas[C_row,C_col]
						refresh_pal = True
				if MODS == 1 : 					#LHSIFT
					# if keyd [KSETSEL] :
						# sel0y, sel0x = v2i(v_row, v_col)
						# sel1y, sel1x = sel0y+1, sel0x+1
						# sel_on = True
						# refresh = True
					if msbd [0] :
						new_sel0y, new_sel0x  = v2i(v_row, v_col)
						sel0y = min(new_sel0y, sel1y-1)
						sel0x = min(new_sel0x, sel1x-1)
						sel_on = True
						refresh = True
					if msbd [2] :
						new_sel1y, new_sel1x  = v2i(v_row, v_col)
						sel1y = max(new_sel1y+1, sel0y+1)
						sel1x = max(new_sel1x+1, sel0x+1)
						sel_on = True
						refresh = True
				if keyd [KJUMP] :
					refresh = True
					dif_row = v_row - v_centery
					dif_col = v_col - v_centerx
					if dif_row > 0:
						start_row = up(start_row, dif_row, start_row_max) 
					if dif_row < 0:
						start_row = dn(start_row, -dif_row, 0) 
					if dif_col > 0:
						start_col = up(start_col, dif_col, start_col_max) 
					if dif_col < 0:
						start_col = dn(start_col, -dif_col, 0) 
					setview()
					refresh = True
			# ===== render view ======= 
			if refresh : 
				view_surf.fill (Col_bg)
				Render_view ( Canvas [start_row : end_row, start_col : end_col] )
				draw_border()
				if sel_on:
					show_selection()
				show_center()
				DISP.blit (view_surf, (Ox, Oy) )
				draw_rulers()
				refresh = False 

			pygame.display.flip( )
			if not Running : break

pygame.quit( )

