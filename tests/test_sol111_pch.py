#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test the punch reader with file sol101.pch
----------------------------------

"""

import os
import numpy as np
import pytest

from stress4analysis import punch

fnames = []

#@pytest.fixture()
#@pytest.mark.parametrize('fname', fnames)
#def fname() :
    #return fname

#@pytest.fixture(scope="module", params=['sol111_sort1_real.pch', 
                                        #'sol111_sort2_real.pch', 
                                        #'sol111_sort1_phase.pch', 
                                        #'sol111_sort2_phase.pch'])
@pytest.fixture(scope="module", params=['sol111_sort1_real.pch', 
                                        'sol111_sort1_phase.pch']) 
def pch(request) :
    pch = punch.Punch()
    pch.read(os.path.join('..', 'data', request.param))
    return pch

def test_cases(pch) :
    cases = pch.cases
    np.testing.assert_array_equal(cases[['ID']].drop_duplicates().values.T, np.array([[1, 2, 3]]))

def test_displacements_first(pch) :
    displacements = pch.displacements
    np.testing.assert_array_equal(displacements[(displacements['Case'] == 1) & 
                                                    (displacements['Node'] == 2001) & 
                                                    (displacements['Frequency'] == 5.)][['x', 'y', 'z', 'rx', 'ry', 'rz']].values,
                              np.array([[-9.939638E-03 + 1j * -1.075396E-09, 2.198712E-08 + 1j * 1.291198E-11, 
                                         -1.270445E-07 + 1j * 1.026846E-10, -2.518057E-06 + 1j * 1.291944E-09, 
                                         -3.480340E-06 + 1j * 1.776345E-09, 3.246033E-07 + 1j * -1.688139E-10]]))

def test_displacements_last(pch) :
    displacements = pch.displacements
    np.testing.assert_array_equal(displacements[(displacements['Case'] == 3) & 
                                                    (displacements['Node'] == 2019) & 
                                                    (displacements['Frequency'] == 300.)][['x', 'y', 'z', 'rx', 'ry', 'rz']].values,
                              np.array([[1.660987E-08 + 1j * -1.620602E-12, -9.562576E-07 + 1j * -1.649483E-08, 
                                         2.037582E-06 + 1j * 1.076404E-07, 9.530941E-05 + 1j * 1.651252E-06, 
                                         2.126992E-06 + 1j * -5.775603E-09, 7.811522E-07 + 1j * -4.473947E-11]]))

def test_accelerations_last(pch) :
    accelerations = pch.accelerations
    np.testing.assert_array_equal(accelerations[(accelerations['Case'] == 3) & 
                                                    (accelerations['Node'] == 2019) & 
                                                    (accelerations['Frequency'] == 300.)][['x', 'y', 'z', 'rx', 'ry', 'rz']].values,
                              np.array([[-5.901583E-02 + 1j * 5.758094E-06, 3.397639E+00 + 1j * 5.860707E-02, 
                                         -7.239647E+00 + 1j * -3.824526E-01, -3.386399E+02 + 1j * -5.866992E+00, 
                                         -7.557324E+00 + 1j * 2.052105E-02, -2.775479E+00 + 1j * 1.589619E-04]]))

def test_forces_first(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 1) & 
                                                    (forces['Element'] == 3000) & 
                                                    (forces['Frequency'] == 5.)][['Fx']].values,
                              np.array([[1.812245E-03 + 1j * -9.088075E-07]]))

def test_forces_first(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 3) & 
                                                    (forces['Element'] == 4002) & 
                                                    (forces['Frequency'] == 300.)][['Fx']].values,
                              np.array([[-2.556116E-02 + 1j * -1.003306E-03]]))

#def test_mpcfs_vs_spcfs(pch) :
    #spcfs = pch.spcfs 
    #mpcfs = pch.mpcfs
    #for case in pch.cases['ID'].unique() :
        #for frequency in pch.frequencies['ID'].unique() :
            #np.testing.assert_almost_equal(spcfs[(spcfs['Case'] == case) & (spcfs['Node'] == 999999) & (spcfs['Frequency'] == frequency)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, 
                                        #-mpcfs[(mpcfs['Case'] == case) & (mpcfs['Node'] == 999999) & (mpcfs['Frequency'] == frequency)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, 5)

def test_frequencies(pch):
    frequencies = pch.frequencies
    np.testing.assert_array_almost_equal(frequencies['ID'].values, np.array(range(5, 301)), 4)
