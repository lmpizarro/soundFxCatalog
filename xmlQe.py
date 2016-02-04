import lxml.etree as etree


def append(inp, in_d):
    for e in in_d['elements']:
        ce = etree.Element(e['element'], attrib=e['attrib'])
        if e['text'] != '':
            ce.text = e['text']
        inp.append(ce)
        append(ce, e)


def createXML(in_d):
    inp_ = etree.Element(in_d['element'], attrib=in_d['attrib'])

    append(inp_, in_d)
    return inp_


def writeQe(inp_, filename):
    str_ = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
    str_ += (etree.tounicode(inp_, pretty_print=True))
    print str_

    f = open(filename, 'w')

    f.write(str_)

    f.close()


class qeError(Exception):
    pass


def getDict(element, attrib, elements, text=''):
    dict_ = {'element': element, 'attrib': attrib,
             'elements': elements, 'text': text}
    return dict_

# field Options


def setOccupations(val):
    str_d = getDict('string', {}, [], val)
    return getDict('parameter', {'name': 'occupations'}, [str_d])


def setSmearing(val):
    str_d = getDict('string', {}, [], val)
    return getDict('parameter', {'name': 'smearing'}, [str_d])


def setDegauss(val):
    str_d = getDict('real', {}, [], str(val))
    return getDict('parameter', {'name': 'degauss'}, [str_d])


class Options:

    def getVals(self, dict_):

        keys = dict_.keys()

        list_r = []
        for k in keys:
            if k == 'occupations':
                list_r.append(setOccupations(dict_[k]))
            elif k == 'smearing':
                list_r.append(setSmearing(dict_[k]))
            elif k == 'degauss':
                list_r.append(setDegauss(dict_[k]))

        return getDict('field', {'name': 'Options'}, list_r)


# field  InputOuput

def setRestartMode(mode):
    str_d = getDict('string', {}, [], mode)
    return getDict('parameter', {'name': 'restart_mode'}, [str_d])


def setPseudoDir(dir_):
    str_d = getDict('string', {}, [], dir_)
    return getDict('parameter', {'name': 'pseudo_dir'}, [str_d])


def setOutDir(dir_):
    str_d = getDict('string', {}, [], dir_)
    return getDict('parameter', {'name': 'outdir'}, [str_d])


def setTstress(bool_):
    ''' Calculate Stress '''
    str_d = getDict('logical', {}, [], bool_)
    return getDict('parameter', {'name': 'tstress'}, [str_d])


def setTprnfor(bool_):
    ''' Calculate Forces '''
    str_d = getDict('logical', {}, [], bool_)
    return getDict('parameter', {'name': 'tprnfor'}, [str_d])


class InputOutput:

    def getVals(self, dict_):

        keys = dict_.keys()

        list_r = []
        for k in keys:
            if k == 'restart_mode':
                list_r.append(setRestartMode(dict_[k]))
            elif k == 'pseudodir':
                list_r.append(setPseudoDir(dict_[k]))
            elif k == 'outdir':
                list_r.append(setOutDir(dict_[k]))
            elif k == 'tstress':
                list_r.append(setTstress(dict_[k]))
            elif k == 'tprnfor':
                list_r.append(setTprnfor(dict_[k]))
        return getDict('field', {'name': 'InputOutput'}, list_r)


# field Numerics

def setEcutWfc(ecut):
    ''' ecutwfc: kinetic energy cutoff for WAVEFUNCTION [in Ry] '''
    str_d = getDict('real', {}, [], str(ecut))
    return getDict('parameter', {'name': 'ecutwfc'}, [str_d])


def setDiagonalization(diag):
    ''' type of diagonalization
        david
        cg '''
    if diag not in ['cg', 'david']:
        raise qeError('%s Not a diagonalization type' % diag)
    else:
        str_d = getDict('string', {}, [], diag)
    return getDict('parameter', {'name': 'diagonalization'}, [str_d])


def setMixingMode(mm):
    ''' Mixin Mode: 
            plain:, 
            TF:
            local-TF '''
    if mm not in ['plain', 'TF', 'local-TF']:
        raise qeError('%s Not a mixing mode' % mm)
    else:
        str_d = getDict('string', {}, [], mm)

    return getDict('parameter', {'name': 'mixing_mode'}, [str_d])


def setMixingBeta(mb):
    ''' mixing factor for self consistency '''
    str_d = getDict('real', {}, [], str(mb))
    return getDict('parameter', {'name': 'mixing_beta'}, [str_d])


def setConvThr(thr):
    ''' conv_thr: convergence threshold for selfconsistency '''
    thr_ = str(thr)
    str_d = getDict('real', {}, [], thr_)
    return getDict('parameter', {'name': 'conv_thr'}, [str_d])


class Numerics:

    def getVals(self, dict_):

        keys = dict_.keys()

        list_r = []
        for k in keys:
            if k == 'ecutWfc':
                list_r.append(setEcutWfc(dict_[k]))
            elif k == 'diagonalization':
                list_r.append(setDiagonalization(dict_[k]))
            elif k == 'mixing_mode':
                list_r.append(setMixingMode(dict_[k]))
            elif k == 'mixing_beta':
                list_r.append(setMixingBeta(dict_[k]))
            elif k == 'convthreshold':
                list_r.append(setConvThr(dict_[k]))
        return getDict('field', {'name': 'Numerics'}, list_r)


def setFields(fd):

    fd_num = fd['numerics']
    fd_io = fd['inputoutput']
    fd_opts = fd['options']

    nums = Numerics()
    inout = InputOutput()
    opts = Options()
    fnums = nums.getVals(fd['numerics'])
    fios = inout.getVals(fd['inputoutput'])
    fopts = opts.getVals(fd_opts)

    return (fios, fnums, fopts)


def setPosition(name, pos):
    str_pos = str(pos[0]) + ' ' + str(pos[1]) + ' ' + str(pos[2])
    re1_d = getDict('real', {'rank': '1', 'n1': '3', 'n2': '0'}, [], str_pos)
    p1_d = getDict('position', {}, [re1_d])
    sp_d = getDict('atom',  {'name': name}, [p1_d])
    return sp_d


def setAtomicList(positions):
    ''' nat: number of atoms in the unit cell '''
    al_d = getDict('atomic_list',  {'units': 'alat',
                                    'nat': '2'}, positions)
    return al_d


def setCell(ibrav, alat, celldm):
    celldm_ = ''
    for c in celldm:
        celldm_ += str(c) + ' '
    re2_d = getDict('real', {'rank': '1', 'n1': '5',
                             'n2': '0'}, [], '0.0 0.0 0.0 0.0 0.0')
    qe_d = getDict('qecell', {'ibrav': str(ibrav), 'alat': str(alat)}, [re2_d])
    ce_d = getDict('cell', {'type': 'qecell'}, [qe_d])
    return ce_d


def setInput(calculation, prefix, elements):
    if calculation not in ['scf']:
        raise qeError("Calculation error")
    else:
        in_d = getDict('input', {'calculation': 'scf',
                                 'prefix': 'silicon'}, elements)
    return in_d


def setAtomicSpecies(especies_list):
    def setSpecie_(name, pseudofile, mass):

        re1_d = getDict(
            'real', {'rank': '0', 'n1': '0', 'n2': '0'}, [], str(mass))
        str_d = getDict('string', {}, [], pseudofile)
        p1_d = getDict('property', {'name': 'mass'}, [re1_d])
        p2_d = getDict('property', {'name': 'pseudofile'}, [str_d])
        sp_d = getDict('specie',  {'name': name}, [p1_d, p2_d])

        return sp_d

    def setSpecies(especies_list):

        l_e = []

        for e in especies_list:
            mass = e['mass']
            pseudofile = e['pseudofile']
            name = e['name']

            l_e.append(setSpecie_(name, pseudofile, mass))

        return l_e

    ''' ntyp: number of types of atoms in the unit cell '''
    ntyp = len(especies_list)
    ae_d = getDict('atomic_species',  {
                   'ntyp': str(ntyp)}, setSpecies(especies_list))
    return ae_d


def setK_points(type_, data):
    if type_ not in ['automatic']:
        raise qeError('k_points bad type %s' % type_)
    else:
        if type_ == 'automatic':
            str_ = ''
            for d in data:
                str_ += str(d) + ' '
            int_ = getDict('integer', {'rank': '1', 'n1': '6'}, [], str_)
            print 'ggg',  int_
            m = getDict('mesh', {}, [int_])
            k_p_d = getDict('k_points',  {'type': type_}, [m])

    return k_p_d


if __name__ == '__main__':
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

    (inout, nums, opts) = setFields(fd)

    especies = [{'name': 'Si', 'pseudofile': 'Si.pz-vbc.UPF', 'mass': 28.086},
                {'name': 'Al', 'pseudofile': 'Al.pz-vbc.UPF', 'mass': 18.086}]

    ae_d = setAtomicSpecies(especies)

    k_p_d = setK_points('automatic', [1, 1, 1, 1, 1, 1])

    pos_si1 = setPosition('Si', [0.0, 0.0, 0.0])
    pos_si2 = setPosition('Al', [0.25, 0.25, 0.25])

    al_d = setAtomicList([pos_si1, pos_si2])

    ce_d = setCell(2, 10.2, [0.0, 0.0, 0.0, 0.0, 0.0, ])

    in_d = setInput('scf', 'silicon', [
                    ce_d, ae_d, al_d, inout, nums, opts, k_p_d])

    QExmlTree = createXML(in_d)

    writeQe(QExmlTree, 'si.xml')
