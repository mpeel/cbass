#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Convert the C-BASS maps into a more user-friendly format for publication
# 
# Mike Peel		04 Nov 2020		v1 - start
# Mike Peel		05 Nov 2020		v2 - expand
# Mike Peel     06 Nov 2020     v3 - tweaks to comments
#
import numpy as np
import healpy as hp
import os
import astropy.io.fits as fits

def get_header_val(hdr,search):
	for i in range(0,len(hdr)):
		if search in hdr[i][0]:
			return hdr[i][1]
	return ''

def reformat_fits(outfile, iqu_file, cov_file,comment='',date='',unit='',coorsys='', version=''):

	# Check that we aren't going to over-write anything.
	if os.path.isfile(outfile):
		print("You already have a file with the output name " + outfile + "! Not going to overwrite it. Move it, or set a new output filename, and try again!")
		return

	# Read in the maps and headers
	try:
		iqu,h = hp.read_map(iqu_file,field=None,h=True)
	except:
		print('Unable to read in ' + str(iqu_file))
		return False
	try:
		cov,h_cov = hp.read_map(cov_file,field=None, h=True)
	except:
		print('Unable to read in ' + str(cov_file))
		return False

	# Make sure that the covariance values are hp.UNSEEN when the map is hp.UNSEEN
	for i in range(0,len(cov)):
		cov[i][iqu[0] == hp.UNSEEN] = hp.UNSEEN

	# print(h)
	# print(h_cov)

	# Use either a user-input unit; the header unit; or the default unit, in that order
	if unit == '':
		unit = get_header_val(h,'TUNIT1')
	if unit == '' or unit == 'unknown':
		unit = 'mK'

	# Use either a user-input unit; the header unit; or the default unit, in that order
	if coorsys == '':
		coorsys = get_header_val(h,'COORSYS')
	if coorsys == '':
		coorsys = get_header_val(h,'COORDSYS')
	if coorsys == '':
		coorsys = 'C'

	# Prepare the set of columns to write out
	cols = []
	cols.append(fits.Column(name='TEMPERATURE', format='1E', unit=unit,array=np.asarray(iqu[0])))
	cols.append(fits.Column(name='Q_POLARISATION', format='1E', unit=unit, array=np.asarray(iqu[1])))
	cols.append(fits.Column(name='U_POLARISATION', format='1E', unit=unit, array=np.asarray(iqu[2])))
	# Note that the covariance order is not the same as in the file header...
	cols.append(fits.Column(name='II_COV', format='1E', unit='('+unit+')^2', array=np.asarray(cov[0])))
	cols.append(fits.Column(name='QQ_COV', format='1E', unit='('+unit+')^2', array=np.asarray(cov[1])))
	cols.append(fits.Column(name='QU_COV', format='1E', unit='('+unit+')^2', array=np.asarray(cov[5])))
	cols.append(fits.Column(name='UU_COV', format='1E', unit='('+unit+')^2', array=np.asarray(cov[2])))
	# (NB: IQ and IU are dropped as they are 0)
	cols = fits.ColDefs(cols)
	bin_hdu = fits.BinTableHDU.from_columns(cols)

	# Copy over the headers that we want, and add extra ones
	bin_hdu.header.comments['TTYPE1'] = 'Intensity brightness temperature'
	bin_hdu.header.comments['TTYPE2'] = 'Q polarisation brightness temperature'
	bin_hdu.header.comments['TTYPE3'] = 'U polarisation brightness temperature'
	bin_hdu.header.comments['TTYPE4'] = 'Intensity covariance'
	bin_hdu.header.comments['TTYPE5'] = 'QQ covariance'
	bin_hdu.header.comments['TTYPE6'] = 'QU covariance'
	bin_hdu.header.comments['TTYPE7'] = 'UU covariance'
	bin_hdu.header['POLAR'] = 'T'
	bin_hdu.header['POLCCONV'] = 'IAU'
	bin_hdu.header['OBJECT'] = 'FULLSKY'
	bin_hdu.header['COORDSYS'] = coorsys
	bin_hdu.header['PIXTYPE'] = get_header_val(h,'PIXTYPE')
	bin_hdu.header['ORDERING'] = get_header_val(h,'ORDERING')
	bin_hdu.header['NSIDE'] = get_header_val(h,'NSIDE')
	bin_hdu.header['FIRSTPIX'] = 0
	bin_hdu.header['LASTPIX'] = len(iqu[0])
	bin_hdu.header['INDXSCHM'] = 'IMPLICIT'
	bin_hdu.header['BAD_DATA'] = (hp.UNSEEN, 'standard healpix value')
	bin_hdu.header['TELESCOP'] = 'CBASSN'
	bin_hdu.header['FREQUENC'] = (4.76e9,'[Hz] nominal centre observation frequency')
	# bin_hdu.comments['FREQUENC'] = 'Hz'
	if date != '':
		bin_hdu.header['DATE'] = date
	if version != '':
		bin_hdu.header['VERSION'] = version
	if comment != '':
		bin_hdu.header['COMMENT'] = comment

	# Write out the file
	bin_hdu.writeto(outfile)

	# All done!
	return True

# EOF