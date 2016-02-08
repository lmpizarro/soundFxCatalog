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

class Field:
    types = {}

    def setParameter(self, val, name, type_):
        str_d = getDict(type_, {}, [], str(val))
        return getDict('parameter', {'name': name}, [str_d])

    def getVals(self, cp_params):
        cp_keys = cp_params.keys()

        list_r = []
        for k in cp_keys:
            p_d = self.setParameter(cp_params[k], k, self.types[k])
            list_r.append(p_d)
        return list_r


class Fields(Field):
    types = {'nspin': 'integer'}

    def getField(self, params):
        return getDict('field', {'name': 'Fields'}, self.getVals(params))


class CP(Field):
    types = {
        'nstep': 'integer',
        'dt': 'real',
        'ion_dynamics': 'string',
        'isave': 'integer',
        'nr1b': 'integer',
        'nr2b': 'integer',
        'nr3b': 'integer',
        'electron_dynamics': 'string',
        'electron_damping': 'real',
        'emass': 'real',
        'emass_cutoff': 'real',
        'ndr': 'integer',
        'ndw': 'integer',
        'ampre': 'real'
    }

    def getField(self, params):
        return getDict('field', {'name': 'CP'}, self.getVals(params))


class Options(Field):
    types = {
        'degauss': 'real',
        'smearing': 'string',
        'occupations': 'string',
        'nbnd': 'integer',
        'qcutz': 'real',
        'q2sigma': 'real',
        'ecfixed': 'real'
    }

    def getField(self, params):
        return getDict('field', {'name': 'Options'}, self.getVals(params))

class MD(Field):
    types = {
        'dt':'real',
	'nstep':'integer',
        'pot_extrapolation':'string',
        'wfc_extrapolation':'string'
    }
    def getField(self, params):
        return getDict('field', {'name': 'MD'}, self.getVals(params))



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


def setIprint(val):
    str_d = getDict('integer', {}, [], str(val))
    return getDict('parameter', {'name': 'iprint'}, [str_d])


def setStartingWfc(val):
    str_d = getDict('string', {}, [], val)
    return getDict('parameter', {'name': 'startingwfc'}, [str_d])

def setDisk_Io(val):
    str_d = getDict('string', {}, [], val)
    return getDict('parameter', {'name': 'disk_io'}, [str_d])

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
            elif k == 'iprint':
                list_r.append(setIprint(dict_[k]))
            elif k == 'startingwfc':
                list_r.append(setStartingWfc(dict_[k]))
            elif k == 'disk_io':
                list_r.append(setDisk_Io(dict_[k]))


        return list_r

    def getField(self, params):
        return getDict('field', {'name': 'InputOutput'}, self.getVals(params))


# field Numerics

def setEcutWfc(ecut):
    ''' ecutwfc: kinetic energy cutoff for WAVEFUNCTION [in Ry] '''
    str_d = getDict('real', {}, [], str(ecut))
    return getDict('parameter', {'name': 'ecutwfc'}, [str_d])


def setEcutRho(ecut):
    ''' ecutwfc: kinetic energy cutoff for WAVEFUNCTION [in Ry] '''
    str_d = getDict('real', {}, [], str(ecut))
    return getDict('parameter', {'name': 'ecutrho'}, [str_d])


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


def setNoSym(bool_):
    thr_ = str(bool_)
    str_d = getDict('logical', {}, [], thr_)
    return getDict('parameter', {'name': 'nosym'}, [str_d])

class Numerics:

    def getVals(self, dict_):

        keys = dict_.keys()

        list_r = []
        for k in keys:
            if k == 'ecutWfc':
                list_r.append(setEcutWfc(dict_[k]))
            if k == 'ecutrho':
                list_r.append(setEcutRho(dict_[k]))
            elif k == 'diagonalization':
                list_r.append(setDiagonalization(dict_[k]))
            elif k == 'mixing_mode':
                list_r.append(setMixingMode(dict_[k]))
            elif k == 'mixing_beta':
                list_r.append(setMixingBeta(dict_[k]))
            elif k == 'convthreshold':
                list_r.append(setConvThr(dict_[k]))
            elif k == 'nosym':
                list_r.append(setNoSym(dict_[k]))
        return list_r

    def getField(self, params):
        return getDict('field', {'name': 'Numerics'}, self.getVals(params))


def setPosition(pos_d):
    name = pos_d['name']
    pos = pos_d['position']
    str_pos = str(pos[0]) + ' ' + str(pos[1]) + ' ' + str(pos[2])
    re1_d = getDict('real', {'rank': '1', 'n1': '3', 'n2': '0'}, [], str_pos)
    p1_d = getDict('position', {}, [re1_d])
    sp_d = getDict('atom',  {'name': name}, [p1_d])
    return sp_d


def setAtomicList(positions, units):
    ''' nat: number of atoms in the unit cell '''
    nat = len(positions)
    al_d = getDict('atomic_list',  {'units': 'alat',
                                    'nat': str(nat)}, positions)
    return al_d


def setCell(ibrav, alat, celldm):
    celldm_ = ''
    for c in celldm:
        celldm_ += str(c) + ' '
    re2_d = getDict('real', {'rank': '1', 'n1': '5',
                             'n2': '0'}, [], celldm_)
    qe_d = getDict('qecell', {'ibrav': str(ibrav), 'alat': str(alat)}, [re2_d])
    ce_d = getDict('cell', {'type': 'qecell'}, [qe_d])
    return ce_d


def setInput(calculation, prefix, elements):
    if calculation not in ['scf', 'cp', 'md']:
        raise qeError("Calculation error")
    else:
        in_d = getDict('input', {'calculation': calculation,
                                 'prefix': prefix}, elements)
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


def setK_points(k_points):
    type_ = k_points['type']

    if type_ not in ['automatic', 'tpiba']:
        raise qeError('k_points bad type %s' % type_)
    else:
        if type_ == 'automatic':
            int_ = getDict('integer', {'rank': '1', 'n1': '6'}, [], k_points['text'])
            m = getDict('mesh', {}, [int_])
            k_p_d = getDict('k_points',  {'type': type_}, [m])
        elif type_ == 'tpiba':
            int_ = getDict('real', {'rank': '2', 'n1': '4', 'n2':  str(k_points['npoints'])}, [], k_points['text'])
            m = getDict('mesh', {'npoints': str(k_points['npoints'])}, [int_])
            k_p_d = getDict('k_points',  {'type': type_}, [m])


    return k_p_d



def setFields(fd):

    fd_num = fd['numerics']
    fd_io = fd['inputoutput']
    fd_opts = fd['options']

    nums = Numerics()
    inout = InputOutput()
    opts = Options()
    fnums = nums.getField(fd['numerics'])
    fios = inout.getField(fd['inputoutput'])
    fopts = opts.getField(fd_opts)

    return (fios, fnums, fopts)



def test_scf():
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
                {'name': 'Al', 'pseudofile': 'Al.pz-vbc.UPF', 'mass': 13.086}]

    ae_d = setAtomicSpecies(especies)

    k_points = {'type':'automatic','text':'1 1 1 1 1 1'}

    k_p_d = setK_points(k_points)

    positions = [{'name':'Si', 'position':[0.0, 0.0, 0.0]}, {'name':'Al', 'position':[0.25, 0.25, 0.25]}]
    pos_si1 = setPosition(positions[0])
    pos_si2 = setPosition(positions[1])

    al_d = setAtomicList([pos_si1, pos_si2], 'alat')

    ce_d = setCell(2, 10.2, [0.0, 0.0, 0.0, 0.0, 0.0, ])

    in_d = setInput('scf', 'silicon', [
                    ce_d, ae_d, al_d, inout, nums, opts, k_p_d])

    QExmlTree = createXML(in_d)

    writeQe(QExmlTree, 'si.xml')


def readPositions(filename):
    f = open(filename)
    pos_l = f.readlines()
    f.close()
    pos = []

    for l in pos_l:
        s = l.split()
	pos_d ={'name': s[0], 'position': [s[1], s[2], s[3]]}
        pos.append(setPosition(pos_d))

    return pos


import os

def test_cp():
    prefix = 'sio2cp'

    root_calc = os.getenv('HOME')

    calc_dir = '/python/materiales/espresso/' + prefix
    calc_path = os.path.abspath(root_calc + '/' + calc_dir +'/')

    if os.path.isdir(calc_path) == False:
        os.makedirs(calc_path)

    fd = {'numerics': {
        'ecutWfc': 20.0,
        'ecutrho': 150.0,
    },
        'inputoutput': {
        'restart_mode': 'from_scratch',
        'pseudodir': '/home/lmpizarro/python/materiales/espresso-5.2.1/atomic/examples/pseudo-LDA-0.5/',
        'outdir': calc_path,
        'iprint': 20,
        'startingwfc': 'random'
    },
        'options': {
        'nbnd': 48,
        'qcutz': 150,
        'q2sigma': 2.05,
        'ecfixed': 16.0
    },
        'fields': {
        'nspin': 1
    },
        'cp': {
        'nstep': 100,
        'dt': 5.0,
        'ion_dynamics': 'none',
        'isave': 20,
        'nr1b': 16,
        'nr2b': 16,
        'nr3b': 16,
        'electron_dynamics': 'damp',
        'electron_damping': 0.2,
        'emass': 700.0,
        'emass_cutoff': 3.0,
        'ndr': 90,
        'ndw': 91,
        'ampre': 0.01
    }
    }

    cp = CP()
    nums = Numerics()
    ios = InputOutput()
    opts = Options()
    fields = Fields()

    cp_params = fd['cp']
    num_params = fd['numerics']
    ios_params = fd['inputoutput']
    opts_params = fd['options']
    fields_params = fd['fields']

    inout_d = ios.getField(ios_params)
    nums_d = nums.getField(num_params)
    opts_d = opts.getField(opts_params)
    field_d = fields.getField(fields_params)
    cp_d = cp.getField(cp_params)

    especies = [{'name': 'O', 'pseudofile': 'O.pz-rrkjus.UPF', 'mass': 16.086},
                {'name': 'Si', 'pseudofile': 'Si.pz-vbc.UPF', 'mass': 28.086},
                ]

    ae_d = setAtomicSpecies(especies)

    positions = readPositions('cpsio2pos.txt')
    al_d = setAtomicList(positions, 'bohr')

    ce_d = setCell(8, 9.28, [1.73206, 1.09955, 0.0, 0.0, 0.0, ])

    in_d = setInput('cp', prefix, [
                    ce_d, ae_d, al_d, inout_d, nums_d, opts_d, field_d, cp_d])

    QExmlTree = createXML(in_d)

    writeQe(QExmlTree, 'sio2cp.xml')


if __name__ == '__main__':
    test_cp()
    test_scf()
