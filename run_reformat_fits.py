#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Example run file for reformat_fits
# 
# Mike Peel		04 Nov 2020		v1
# Mike Peel		05 Nov 2020		v2
#
from reformat_fits import *

indir = '/Users/mpeel/Documents/maps/cbass2020/v33b/NIGHTMERID20/rawest_map/'
outdir = '/Users/mpeel/Documents/maps/cbass2020/v33b/'
iqu_file = indir+'NM20_v33b_allelsNS1_xAS14_masked5pc_C_1024_ol500_lessTol_c_Pipe_map.fits'
cov_file = indir+'NM20_v33b_allelsNS1_xAS14_masked5pc_C_1024_ol500_lessTol_c_Pipe_cov.fits'
out_file = outdir+'NM20_v33b_allelsNS1_xAS14_masked5pc_C_1024_ol500_lessTol_c_Pipe_combined.fits'
comment = 'NM20_v33b_allelsNS1_xAS14_masked5pc_C_1024_ol500_lessTol_c_Pipe' # Ignored if blank
date = '2020-11-01' # Ignored if blank
unit = '' # If blank, the file header unit will be used, or if that's not present, mK will be used
coorsys = '' # If blank, the file header unit will be used, or if that's not present, C will be used
version = 'v33b' # Ignored if blank
test = reformat_fits(out_file, iqu_file, cov_file, comment=comment, date=date, unit=unit, coorsys=coorsys, version=version)
print(test)
check,check_h = hp.read_map(out_file,field=None,h=True)
print(check_h)

# For the ones from after the old post-matlab version
# indir = '/Users/mpeel/Documents/maps/cbass2020/v33b/NIGHTMERID20/calibrated_map/'
# iqu_file = indir+'tauA_cal_NM20_v33b_allelsNS1_xAS14_masked5pc_G_1024_ol500_lessTol_g_Pipe_map.fits'
# cov_file = indir+'tauA_cal_NM20_v33b_allelsNS1_xAS14_masked5pc_G_1024_ol500_lessTol_g_Pipe_cov.fits'
# out_file = outdir+'tauA_cal_NM20_v33b_allelsNS1_xAS14_masked5pc_G_1024_ol500_lessTol_g_Pipe_map_combined.fits'
# test = reformat_fits(out_file, iqu_file, cov_file, comment=comment, date=date, unit=unit, coorsys=coorsys, version=version)
# print(test)
# check,check_h = hp.read_map(out_file,field=None,h=True)
# print(check_h)
