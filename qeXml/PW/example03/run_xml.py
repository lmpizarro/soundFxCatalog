#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import os
import sys

qeXmlLibPath = os.path.abspath(
    '/home/lmpizarro/python/djangoApps/soundFxDb/qeXml/lib')
sys.path.append(qeXmlLibPath)

import xmlQe as xq


def setFields(fd):

    fd_num = fd['numerics']
    fd_io = fd['inputoutput']
    fd_md = fd['md']

    nums = xq.Numerics()
    inout = xq.InputOutput()
    md   = xq.MD()
    fnums = nums.getField(fd['numerics'])
    fios = inout.getField(fd['inputoutput'])
    fmd   = md.getField(fd_md)

    return (fios, fnums, fmd)

k_points1 = {'type': 'automatic', 'npoints': 0, 'text': '1 1 1 0 0 0'}
k_points2 = {'type': 'tpiba', 'npoints': 4, 'text': '''0.0 0.0 0.0 1.0
                       				 1.0 0.0 0.0 1.0
		         			 0.0 1.0 0.0 1.0
			        		 0.0 0.0 1.0 1.0'''}

def example03(val, positions, ibrav, k_points):

    PSEUDODIR = '/home/lmpizarro/python/materiales/espresso-5.2.1/atomic/examples/pseudo-LDA-0.5/'

    PREFIX = 'si%s'%val

    root_calc = os.getenv('HOME')

    calc_dir = '/python/materiales/espresso/' + PREFIX
    OUTDIR = os.path.abspath(root_calc + '/' + calc_dir + '/')

    if os.path.isdir(OUTDIR) == False:
        os.makedirs(OUTDIR)

    fd = {'numerics': {
        'ecutWfc': 8.0,
        'mixing_beta': 0.7,
        'convthreshold': '1.0d-8',
	'nosym': 'true'
    },
        'inputoutput': {
        'restart_mode': 'from_scratch',
        'pseudodir': PSEUDODIR,
        'outdir': OUTDIR,
        'disk_io': 'high'
	},
	'md':{
	    'dt':20.0,
            'nstep': 100,
	    'pot_extrapolation': 'second-order',
	    'wfc_extrapolation': 'second-order'
	}
    }

    (inout, nums, fmd) = setFields(fd)

    especies = [{'name': 'Si', 'pseudofile': 'Si.pz-vbc.UPF', 'mass': 28.086}]

    ae_d = xq.setAtomicSpecies(especies)

    k_p_d = xq.setK_points(k_points)

    al_d = xq.setAtomicList(positions, 'alat')

    ce_d = xq.setCell(ibrav, 10.18, [0.0, 0.0, 0.0, 0.0, 0.0, ])

    in_d = xq.setInput('md', PREFIX, [
        ce_d, ae_d, al_d, inout, nums, fmd, k_p_d])

    QExmlTree = xq.createXML(in_d)

    xq.writeQe(QExmlTree, 'si.%s.xml'%val)


if __name__ == '__main__':
    positions = xq.readPositions('mdsipos.txt')
    example03('md2', positions[:2], 2, k_points1)
    example03('md8', positions, 1, k_points1)
    example03('md2_G3X', positions[:2], 2, k_points2)
