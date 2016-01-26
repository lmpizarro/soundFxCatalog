from __future__ import division
import sys

FLAGS = ["IsMark", "IsRangeMarker",
         "IsCDMarker", "IsAutoLoop", "IsSessionRange"]


class Location(object):
    '''
    <Location id="295" name="range_1" start="42840" end="176400" flags="IsRangeMarker" locked="no" position-lock-style="AudioTime"/>
    '''

    def __init__(self, name, start, end, flags=["IsRangeMarker"]):
        self._id = 0
        self._name = name
        self.start = start
        self.end = start
        self._locked = "no"
        self.positionLockStyle = "AudioTime"
        self.flags = []
        for f in flags:
            if f in FLAGS:
                self.flags.append(f)
            else:
                print f, "is not a flags"
        if len(self.flags) == 0:
            self.flags = ["IsMark"]

    def setId(self, value):
        self._id = value

    def getId(self):
        return self._id

    def delId(self):
        del self._id

    def flagsToString(self):
        str_ = ''
        for l in self.flags:
            str_ += l + ','
        return (str_)

    def __repr__(self):
        str_ = 'id= ' + str(self.id)
        str_ += ' name= ' + self.name
        str_ += ' start= ' + str(self.start)
        str_ += ' end= ' + str(self.end)
        str_ += ' flags= ' + self.flagsToString()
        str_ += ' locked=' + self.locked
        str_ += ' position-lock-style=' + self.positionLockStyle
        str_ += ' \n'
        return str_

    def setLocked(self, b):
        if b == True:
            self._locked = "yes"
        elif b == False:
            self._locked = "no"
    
    def getLocked(self):
        return self._locked

    def delLocked(self):
        del self._locked

    def setName(self, value):
        self._name = value

    def getName(self):
        return self._name

    def delName(self):
        del self._name

    name = property(getName, setName, delName, "name property docs")
    id = property(getId, setId, delId, "id property docs")
    locked = property(getLocked, setLocked, delLocked, "locked property docs")


class Range(Location):

    def __init__(self, name, start, end):
        Location.__init__(self, name, start, end)


class ToSamples(object):

    def __init__(self, sr=44100, fps=24):
        self.sr = sr
        self.fps = fps

    def convert(self, hmsf):
        samples = (3600 * hmsf[0] + 60 * hmsf[1] +
                   hmsf[2] + hmsf[3] / self.fps) * self.sr
        return (samples)

    # convert hh:mm:ss:ff to [hh:mm:ss:ff]
    def hhmmssfftolist(self, hmsf):
        l = hmsf.split(':')
        for i, ll in enumerate(l):
            l[i] = int(ll)

        if l[0] < 24 and l[1] < 60 and l[2] < 60 and l[3] < self.fps:
            return (l)
        else:
            return [0, 0, 0, 0]


class AdrCue(object):
    # tc_range = ["hh:mm:ss:ff","hh:mm:ss:ff"]

    def __init__(self, tc_range, text, id=0):
        self.tc_range = tc_range
        self.text = text
        self.id = id

    def __repr__(self):
        mstr = 'id: ' + str(self.id)
        mstr += " range start: " + str(self.tc_range[0]) + " range end:" + str(
            self.tc_range[1]) + " text: " + self.text + '\n'
        return mstr

    def getRange(self):
        rg = Range('range' + str(self.id), self.tc_range[0], self.tc_range[1])
        return rg


class Movie(object):
    list_Adr = []

    def __init__(self, title, sr, fps):
        self.ts = ToSamples(sr, fps)
        self.title = title

    def addAdr(self, tc_range, text):
        tc_range_samples = []

        hmsf = self.ts.hhmmssfftolist(tc_range[0])
        tc_range_samples.append(self.ts.convert(hmsf))
        hmsf = self.ts.hhmmssfftolist(tc_range[1])
        tc_range_samples.append(self.ts.convert(hmsf))

        self.list_Adr.append(
            AdrCue(tc_range_samples, text, len(self.list_Adr) + 1))

    def __repr__(self):
        str_ = 'Title: ' + self.title + '\n'
        for l in self.list_Adr:
            str_ += str(l)
        return str_

    def toRanges(self):
        list_Range = []
        for i, l in enumerate(self.list_Adr):
            rg = l.getRange()
            rg.name = 'lll' + str(rg.id)
            rg.setId(i + 1)
            list_Range.append(rg)
        return list_Range

    def readAdrs(self, fileName):
        f = open(fileName, 'r')
        lines = f.readlines()
        f.close()

        for l in lines:
            dat = l.strip().split(',')
            if len(dat) == 3:
                tc_range = dat[0:2]
                text = dat[2]
                self.addAdr(tc_range, text)


if __name__ == '__main__':

    ts = ToSamples()
    loc = Range("mark1", 100000, 144100)
    print loc.flags
    print ts.fps
    print int(ts.convert(ts.hhmmssfftolist('1:23:32:10')))

    try:
        import lxml as etree
        print "lxml"
    except ImportError:
        import xml.etree.ElementTree as etree

    ardour_config = "/media/usb0/ardour/testingMarkers/testingMarkers.ardour"
    tree = etree.parse(ardour_config)
    root = tree.getroot()
    locs = root.findall('Locations')

    for lcs in locs[0]:
        print lcs

    mv = Movie("lo inmediato", 44100, 25)
    mv.addAdr(['1:1:2:4', '1:1:32:21'], "hola mundo Adr")
    mv.addAdr(['0:1:2:4', '0:1:32:21'], "hola todo bien?")
    mv.addAdr(['0:10:2:4', '0:10:32:21'], "No hay todo bien?")
    mv.readAdrs("adr_list.csv")
    print mv.toRanges()
    print mv
