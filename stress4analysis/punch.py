from collections import OrderedDict
import numpy as np
import pandas as pd
import cmath

#pd.set_option('display.float_format', '{:.5E}'.format)


class Cases() :
    def __init__(self) :
        self.id = []
        self.title = []
        self.subtitle = []
        self.label = []
    
class Frequencies() :
    def __init__(self) :
        self.id = []
    
class Nodes() :
    def __init__(self) :
        self.id = []
        self.x = []
        self.y = []
        self.z = []        

class Elements() :
    ETYPES = {12 : 'ELAS2',
             33 : 'QUAD4',
             102 : 'BUSH'}
    
    def __init__(self) :
        self.id = []
        self.type = []
        self.n1 = []
        self.n2 = []
        self.n3 = []
        self.n4 = []

class Coordinates() :
    def __init__(self) :
        self.id = []
        self.title = []

class Displacements() :
    def __init__(self) :
        self.case = []
        self.frequency = []
        self.node = []
        self.x = []
        self.y = []
        self.z = []        
        self.rx = []
        self.ry = []
        self.rz = []        

class Accelerations() :
    def __init__(self) :
        self.case = []
        self.frequency = []
        self.node = []
        self.x = []
        self.y = []
        self.z = []        
        self.rx = []
        self.ry = []
        self.rz = []        

class Spcfs() :
    def __init__(self) :
        self.case = []
        self.frequency = []
        self.node = []
        self.fx = []
        self.fy = []
        self.fz = []        
        self.mx = []
        self.my = []
        self.mz = []        

class Mpcfs() :
    def __init__(self) :
        self.case = []
        self.frequency = []
        self.node = []
        self.fx = []
        self.fy = []
        self.fz = []        
        self.mx = []
        self.my = []
        self.mz = []        

class Forces() :
    def __init__(self) :
        self.case = []
        self.frequency = []
        self.element = []
        self.fx = []
        self.fy = []
        self.fz = []        
        self.mx = []
        self.my = []
        self.mz = []

class Stresses() :
    def __init__(self) :
        self.case = []
        self.frequency = []
        self.element = []
        self.xx = []
        self.yy = []
        self.zz = []        
        self.xy = []
        self.xz = []
        self.yz = []

class Strains() :
    def __init__(self) :
        self.case = []
        self.frequency = []
        self.element = []
        self.xx = []
        self.yy = []
        self.zz = []
        self.xy = []
        self.xz = []
        self.yz = []


class Punch() :
    # define the dictionary
    DATATYPES = {'node': ['displacements', 'accelerations', 'spcfs', 'mpcfs'], 
                 'element' : ['forces', 'stresses', 'strains']}
    CORRELATIONS = OrderedDict([('$DISPLACEMENTS', 'displacements'), 
                                ('$ACCELERATION', 'accelerations'),
                                ('$SPCF', 'spcfs'),
                                ('$MPCF', 'mpcfs'),
                                ('$ELEMENT FORCES', 'forces'),
                                ('$ELEMENT STRESSES', 'stresses'),
                                ('$ELEMENT STRAINS', 'strains')])

    def __init__(self, name = None):
        self.name = name
        self._cases = Cases()
        self._frequencies = Frequencies()
        self._nodes = Nodes()
        self._elements = Elements()
        
        self._displacements = Displacements()
        self._accelerations = Accelerations()
        self._spcfs = Spcfs()
        self._mpcfs = Mpcfs()

        self._forces = Forces()
        self._strains = Strains()
        self._stresses = Stresses()
            
    def __repr__(self):
        pass

    def read(self, filename) :
        data = []
        # start reading
        with open(filename, 'r') as f:
            # read only first 72 characters from the punch file
            for line in f:
                line = line[:72]

                if line.startswith('$TITLE'):
                    title = line.split('=')[1].strip()
                    if data :
                        self.set_values(data, cid, keyword, elementtype, outputtype, frequency)
                    data = []
                    keyword = None
                    elementtype = -1
                    outputtype = -1
                    frequency = 0
                    isdataentry = False
                elif line.startswith('$SUBTITLE') :
                    subtitle = line.split('=')[1].strip()
                elif line.startswith('$LABEL') :
                    label = line.split('=')[1].strip()
                elif line.startswith('$ELEMENT TYPE') :
                    elementtype = np.int64(line[15:27].strip())
                elif line.startswith('$RANDOM ID') :
                    #self.cases.label.append(line.split('=')[1].strip())
                    pass
                elif line.startswith('$SUBCASE ID') :
                    cid = np.int64(line.split('=')[1].strip())
                    if cid not in self._cases.id : 
                        self._cases.title.append(title)
                        self._cases.subtitle.append(subtitle)
                        self._cases.label.append(label)
                        self._cases.id.append(cid)
                    isdataentry = True
                elif any([line.startswith(_) for _ in self.CORRELATIONS.keys()]) :
                    for dataentry in self.CORRELATIONS.keys() :
                        if line.startswith(dataentry) :
                            keyword = self.CORRELATIONS[dataentry]
                            break
                
                ## identify output type
                elif line.startswith('$REAL OUTPUT'):
                    outputtype = 'REAL'
                    continue
                elif line.startswith('$REAL-IMAGINARY OUTPUT'):
                    outputtype = 'REAL-IMAGINARY'
                    continue
                elif line.startswith('$MAGNITUDE-PHASE OUTPUT'):
                    outputtype = 'MAGNITUDE-PHASE'
                    continue

                # parse entity id
                elif line.startswith('$POINT ID ='):
                    #int(line[11:23].strip())
                    continue
                elif line.startswith('$ELEMENT ID ='):
                    #int(line[13:23].strip())
                    continue
                elif line.startswith('$FREQUENCY'):
                    frequency = np.float64(line[12:28].strip())
                    if frequency not in self._frequencies.id :
                        self._frequencies.id.append(frequency)
                    continue

                # ignore other comments
                elif line.startswith('$'):
                    print(line)
                    continue

                #parse of frequency response results
                #if line.find('IDENTIFIED BY FREQUENCY') != -1:
                    #self.is_frequency_response = True
                    #self.output_sort = 2
                #elif line.find('$FREQUENCY =') != -1:
                    #self.is_frequency_response = True
                    #self.output_sort = 1

                # parse element type
                elif isdataentry :
                    # start data parsing
                    line = line.replace('G', ' ')
                    if line.startswith('-CONT-'):
                        line = line.replace('-CONT-', '')
                        data += [np.float64(_.strip()) for _ in line.split()]
                    else:
                        if data :
                          self.set_values(data, cid, keyword, elementtype, outputtype, frequency)
                        data = []
                        # update the last frame with a new data
                        data = [np.float64(_.strip()) for _ in line.split()]
                        for i in range(1, len(data)) :
                            data[i] = np.float64(data[i])
                        if keyword in self.DATATYPES['node'] :
                            nid = data[0]
                            if nid not in self._nodes.id :
                                self._nodes.id.append(nid)
                                self._nodes.x.append(0.0)
                                self._nodes.y.append(0.0)
                                self._nodes.z.append(0.0)
                        elif keyword in self.DATATYPES['element'] :
                            eid = data[0]
                            if eid not in self._elements.id :
                                self._elements.id.append(eid)
                                self._elements.type.append(elementtype)
                                self._elements.n1.append(0)
                                self._elements.n2.append(0)
                                self._elements.n3.append(0)
                                self._elements.n4.append(0)
            if data :
                self.set_values(data, cid, keyword, elementtype, outputtype, frequency)
            data = []

    def set_values(self, data, cid, keyword, elementtype, outputtype, frequency) :
        if outputtype in ['MAGNITUDE-PHASE', 'REAL-IMAGINARY'] :
            data[0] = np.float64(data[0])
            if (len(data) - 1) % 2 != 0 :
                raise ValueError('Wrong number of chunks!', 'Output: %s, num of chunks: %d' % (outputtype, (len(data) - 1)))
            else :
                delta = int((len(data) - 1) / 2)
            if outputtype == 'MAGNITUDE-PHASE' :
                data[1:] = [data[i + 1] * cmath.exp(1j * data[i + 1 + delta] * cmath.pi / 180.0) for i in range(delta)]
            elif outputtype == 'REAL-IMAGINARY' :
                data[1:] = [data[i + 1] + 1j * data[i + 1 + delta] for i in range(delta)]
        else :
            data[0] = np.int64(data[0])
        if keyword == 'displacements' :
            self._displacements.case.append(cid)
            self._displacements.frequency.append(frequency)
            self._displacements.node.append(data[0])
            self._displacements.x.append(data[1])
            self._displacements.y.append(data[2])
            self._displacements.z.append(data[3])
            self._displacements.rx.append(data[4])
            self._displacements.ry.append(data[5])
            self._displacements.rz.append(data[6])
        elif keyword == 'accelerations' :
            self._accelerations.frequency.append(frequency)
            self._accelerations.case.append(cid)
            self._accelerations.node.append(data[0])
            self._accelerations.x.append(data[1])
            self._accelerations.y.append(data[2])
            self._accelerations.z.append(data[3])
            self._accelerations.rx.append(data[4])
            self._accelerations.ry.append(data[5])
            self._accelerations.rz.append(data[6])
        elif keyword == 'spcfs' :
            self._spcfs.case.append(cid)
            self._spcfs.frequency.append(frequency)
            self._spcfs.node.append(data[0])
            self._spcfs.fx.append(data[1])
            self._spcfs.fy.append(data[2])
            self._spcfs.fz.append(data[3])
            self._spcfs.mx.append(data[4])
            self._spcfs.my.append(data[5])
            self._spcfs.mz.append(data[6])
        elif keyword == 'mpcfs' :
            self._mpcfs.case.append(cid)
            self._mpcfs.frequency.append(frequency)
            self._mpcfs.node.append(data[0])
            self._mpcfs.fx.append(data[1])
            self._mpcfs.fy.append(data[2])
            self._mpcfs.fz.append(data[3])
            self._mpcfs.mx.append(data[4])
            self._mpcfs.my.append(data[5])
            self._mpcfs.mz.append(data[6])
        elif keyword == 'forces' :
            self._forces.case.append(cid)
            self._forces.frequency.append(frequency)
            self._forces.element.append(data[0])
            if elementtype == 12 :
                self._forces.fx.append(data[1])
                self._forces.fy.append(0.0)
                self._forces.fz.append(0.0)
                self._forces.mx.append(0.0)
                self._forces.my.append(0.0)
                self._forces.mz.append(0.0)
            elif elementtype == 33 :
                self._forces.fx.append(data[1])
                self._forces.fy.append(data[2])
                self._forces.fz.append(data[3])
                self._forces.mx.append(data[4])
                self._forces.my.append(data[5])
                self._forces.mz.append(data[6])
            elif elementtype == 102 :
                self._forces.fx.append(data[1])
                self._forces.fy.append(data[2])
                self._forces.fz.append(data[3])
                self._forces.mx.append(data[4])
                self._forces.my.append(data[5])
                self._forces.mz.append(data[6])
        elif keyword == 'stresses' :
            self._stresses.case.append(cid)
            self._stresses.frequency.append(frequency)
            self._stresses.element.append(data[0])
            if elementtype == 12 :
                self._stresses.xx.append(data[1])
                self._stresses.yy.append(0.0)
                self._stresses.zz.append(0.0)
                self._stresses.xy.append(0.0)
                self._stresses.xz.append(0.0)
                self._stresses.yz.append(0.0)
            elif elementtype == 33 :
                self._stresses.xx.append(data[1])
                self._stresses.yy.append(data[2])
                self._stresses.zz.append(data[3])
                self._stresses.yz.append(data[6])
                self._stresses.xy.append(data[4])
                self._stresses.xz.append(data[5])
            elif elementtype == 102 :
                self._stresses.xx.append(data[1])
                self._stresses.yy.append(data[2])
                self._stresses.zz.append(data[3])
                self._stresses.yz.append(data[6])
                self._stresses.xy.append(data[4])
                self._stresses.xz.append(data[5])
        elif keyword == 'strains' :
            self._strains.case.append(cid)
            self._strains.frequency.append(frequency)
            self._strains.element.append(data[0])
            if elementtype == 12 :
                self._strains.xx.append(data[1])
                self._strains.yy.append(0.0)
                self._strains.zz.append(0.0)
                self._strains.xy.append(0.0)
                self._strains.xz.append(0.0)
                self._strains.yz.append(0.0)
            elif elementtype == 33 :
                self._strains.xx.append(data[1])
                self._strains.yy.append(data[2])
                self._strains.zz.append(data[3])
                self._strains.yz.append(data[6])
                self._strains.xy.append(data[4])
                self._strains.xz.append(data[5])
            elif elementtype == 102 :
                self._strains.xx.append(data[1])
                self._strains.yy.append(data[2])
                self._strains.zz.append(data[3])
                self._strains.yz.append(data[6])
                self._strains.xy.append(data[4])
                self._strains.xz.append(data[5])

    @property
    def cases(self) :
        if self._cases :
            return pd.DataFrame(data = {'ID' : self._cases.id, 
                                        'Title' : self._cases.title,
                                        'Subtitle' : self._cases.subtitle,
                                        'Label' : self._cases.label})
        else :
            return None

    @property
    def frequencies(self) :
        if self._frequencies :
            return pd.DataFrame(data = {'ID' : self._frequencies.id})
        else :
            return None

    @property
    def nodes(self) :
        if self._nodes :
            return pd.DataFrame(data = {'ID' : self._nodes.id, 
                                        'x' : self._nodes.x,
                                        'y' : self._nodes.y,
                                        'z' : self._nodes.z})
        else :
            return None

    @property
    def elements(self) :
        if self._elements :
            return pd.DataFrame(data = {'ID' : self._elements.id, 
                                        'n1' : self._elements.n1,
                                        'n2' : self._elements.n2,
                                        'n3' : self._elements.n3,
                                        'n4' : self._elements.n4,
                                        'Type' : self._elements.type})
        else :
            return None

    @property
    def displacements(self):
        if self._displacements :
            return pd.DataFrame(data = {'Case' : self._displacements.case,
                                        'Frequency' : self._displacements.frequency,
                                        'Node' : self._displacements.node,
                                        'x' : self._displacements.x,
                                        'y' : self._displacements.y,
                                        'z' : self._displacements.z,
                                        'rx' : self._displacements.rx,
                                        'ry' : self._displacements.ry,
                                        'rz' : self._displacements.rz})
        else :
            return None

    @property
    def accelerations(self):
        if self._accelerations :
            return pd.DataFrame(data = {'Case' : self._accelerations.case,
                                        'Frequency' : self._accelerations.frequency,
                                        'Node' : self._accelerations.node,
                                        'x' : self._accelerations.x,
                                        'y' : self._accelerations.y,
                                        'z' : self._accelerations.z,
                                        'rx' : self._accelerations.rx,
                                        'ry' : self._accelerations.ry,
                                        'rz' : self._accelerations.rz})
        else :
            return None

    @property
    def spcfs(self):
        if self._spcfs :
            return pd.DataFrame(data = {'Case' : self._spcfs.case,
                                        'Frequency' : self._spcfs.frequency,
                                        'Node' : self._spcfs.node,
                                        'Fy' : self._spcfs.fy,
                                        'Fx' : self._spcfs.fx,
                                        'Fz' : self._spcfs.fz,
                                        'Mx' : self._spcfs.mx,
                                        'My' : self._spcfs.my,
                                        'Mz' : self._spcfs.mz})
        else :
            return None

    @property
    def mpcfs(self):
        if self._mpcfs :
            return pd.DataFrame(data = {'Case' : self._mpcfs.case,
                                        'Frequency' : self._mpcfs.frequency,
                                        'Node' : self._mpcfs.node,
                                        'Fx' : self._mpcfs.fx,
                                        'Fy' : self._mpcfs.fy,
                                        'Fz' : self._mpcfs.fz,
                                        'Mx' : self._mpcfs.mx,
                                        'My' : self._mpcfs.my,
                                        'Mz' : self._mpcfs.mz})
        else :
            return None

    @property
    def forces(self):
        if self._forces :
            return pd.DataFrame(data = {'Case' : self._forces.case,
                                        'Frequency' : self._forces.frequency,
                                        'Element' : self._forces.element,
                                        'Fy' : self._forces.fy,
                                        'Fz' : self._forces.fz,
                                        'Mx' : self._forces.mx,
                                        'My' : self._forces.my,
                                        'Fx' : self._forces.fx,
                                        'Mz' : self._forces.mz})
        else :
            return None

    @property
    def stresses(self):
        if self._stresses :
            return pd.DataFrame(data = {'Case' : self._stresses.case,
                                        'Frequency' : self._stresses.frequency,
                                        'Element' : self._stresses.element,
                                        'XX' : self._stresses.xx,
                                        'YY' : self._stresses.yy,
                                        'ZZ' : self._stresses.zz,
                                        'XY' : self._stresses.xy,
                                        'XZ' : self._stresses.xz,
                                        'YZ' : self._stresses.yz})
        else :
            return None

    @property
    def strains(self):
        if self._strains :
            return pd.DataFrame(data = {'Case' : self._strains.case,
                                        'Frequency' : self._strains.frequency,
                                        'Element' : self._strains.element,
                                        'XX' : self._strains.xx,
                                        'YY' : self._strains.yy,
                                        'ZZ' : self._strains.zz,
                                        'XY' : self._strains.xy,
                                        'XZ' : self._strains.xz,
                                        'YZ' : self._strains.yz})
        else :
            return None
