"""
#  general purpose functions
#  (C) Mikhail Vasilev, 2017
"""

import os
import pygame
import numpy

def blit (dest, src, y, x):						# blit numpy array 
	H,W = dest.shape
	h,w = src.shape
	yy0 = max (y,0) ;  yy1 = min (y+h,H)
	xx0 = max (x,0) ;  xx1 = min (x+w,W)
	if yy1 <= yy0 : return
	if xx1 <= xx0 : return
	src_offy = 0 ; 	src_endy = h
	if y < 0 :	src_offy = -y
	Ly = y+h - H 
	if Ly > 0:	src_endy = h - Ly
	src_offx = 0; src_endx = w
	if x < 0 :	src_offx = -x
	Lx = x + w - W 
	if Lx > 0:	src_endx = w - Lx
	dest[yy0 : yy1, xx0:xx1] = src[src_offy : src_endy, src_offx:src_endx]

def put_arr(S, A):						# S - surface destination
	bv = S.get_buffer()
	bv.write(A.tostring(), 0)

def save_arr(fname, X):
	numpy.savetxt(fname, X, fmt="%d", delimiter='\t', newline='\n')

def load_arr(fname):
	tmp = numpy.loadtxt(fname, dtype="B")
	return tmp

def surffromarr(A):						# render from string
	h,w = A.shape[0:2]
	S = pygame.Surface((w, h), pygame.SRCALPHA, 32) 
	bv = S.get_buffer()
	bv.write(A.tostring(), 0)
	return S

def diff(a, b): 				# Return mask treshold
	DIFF = abs_dev(a, b)
	Msk = DIFF > 5
	return Msk

def up(x, d, xmax) : 			# saturated increment 
	y = x + d
	if y < xmax : return y
	return xmax

def dn(x, d, xmin) :			# saturated decrement 
	y = x - d
	if y > xmin : return y
	return xmin
	
def rgb2gray(A) :
	r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
	gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
	# grayX = numpy.zeros_like (gray, dtype="uint32")
	grayX = numpy.zeros_like (gray, dtype="uint8")
	grayX[:] = numpy.rint(gray)
	return grayX

def load_png_8bit(filename) :			# pygame.image.load  grayscale png 
	temp = pygame.imread(filename)
	h, w = temp.shape 
	print ("width: ", w)
	print ("height: ", h)
	print ("bytesize: ", temp.dtype)
	return numpy.invert(temp) 
	
def load_gray (f) : 
	a = pygame.image.load (f)
	bs = a . get_bytesize()
	print (f"surf bytesize : {bs}")
	t = pygame.surfarray.array3d(a)
	if t . shape [2] == 1 :
		return numpy.invert(numpy.transpose(t)) 
	if t . shape [2] == 3 :
		t = gray = rgb2gray(t)
		return numpy.invert(numpy.transpose(t)) 

