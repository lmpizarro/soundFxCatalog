#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division 

import os
import sys

qeXmlLibPath = os.path.abspath('/home/lmpizarro/python/djangoApps/soundFxDb/qeXml/lib')
sys.path.append(qeXmlLibPath)

import xmlQe  as xq

def example01():
    fd = {'numerics': {
        'ecutWfc': 18.0,
        'diagonalization': 'cg',
        'mixing_mode': 'plain',
        'mixing_beta': 0.7,
        'convthreshold': 1.0E-8,
    },
        'inputoutput': {
        'restart_mode': 'from_scratch',
        'pseudodir': '/home/lmpizarro/python/materiales/espresso-5.2.1/atomic/examples/pseudo-LDA-0.5/',
        'outdir': '/home/lmpizarro/tmp',
        'tstress': 'True',
        'tprnfor': 'True'},
        'options': {
        'occupations': 'smearing',
        'smearing': 'marzari-vanderbilt',
        'degauss': 0.05
    }}

    (inout, nums, opts) = xq.setFields(fd)

    especies = [{'name': 'Si', 'pseudofile': 'Si.pz-vbc.UPF', 'mass': 28.086},
                {'name': 'Al', 'pseudofile': 'Al.pz-vbc.UPF', 'mass': 13.086}]

    ae_d = xq.setAtomicSpecies(especies)

    k_p_d = xq.setK_points('automatic', [1, 1, 1, 1, 1, 1])

    pos_si1 = xq.setPosition('Si', [0.0, 0.0, 0.0])
    pos_si2 = xq.setPosition('Al', [0.25, 0.25, 0.25])

    al_d = xq.setAtomicList([pos_si1, pos_si2], 'alat')

    ce_d = xq.setCell(2, 10.2, [0.0, 0.0, 0.0, 0.0, 0.0, ])

    in_d = xq.setInput('scf', 'silicon', [
                    ce_d, ae_d, al_d, inout, nums, opts, k_p_d])

    QExmlTree = xq.createXML(in_d)

    xq.writeQe(QExmlTree, 'si.xml')


if __name__ == '__main__':
    example01()
