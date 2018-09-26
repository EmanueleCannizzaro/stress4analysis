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

@pytest.fixture(scope="module")
def pch() :
    pch = punch.Punch()
    pch.read(os.path.join('..', 'data', 'sol101.pch'))
    return pch
    
def test_cases(pch) :
    cases = pch.cases
    np.testing.assert_array_equal(cases[['ID']].drop_duplicates().values.T, np.array([[100, 200, 300]]))

def test_displacements_first(pch) :
    displacements = pch.displacements
    np.testing.assert_array_equal(displacements[(displacements['Case'] == 100) & 
                                                    (displacements['Node'] == 2001)][['x', 'y', 'z', 'rx', 'ry', 'rz']].values,
                              np.array([[ 4.462737E-06, -1.781939E-06,  1.273970E-05,
                                          2.820892E-04,  4.496019E-04, -6.605602E-05]]))

def test_displacements_last(pch) :
    displacements = pch.displacements
    np.testing.assert_array_equal(displacements[(displacements['Case'] == 300) & 
                                                 (displacements['Node'] == 2019)][['x', 'y', 'z', 'rx', 'ry', 'rz']].values,
                              np.array([[ 2.042521E-06, -2.708797E-04,  1.606910E-03, 
                                          2.706233E-02,  2.130588E-04,  9.613780E-05]]))

def test_spcfs_first(pch) :
    spcfs = pch.spcfs
    np.testing.assert_array_equal(spcfs[(spcfs['Case'] == 100) & 
                                                 (spcfs['Node'] == 999999)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values,
                              np.array([[-5.542533E+01, -1.122658E-12, -3.232414E-12, 
                                         -4.064908E-13, -5.993325E-02,  3.391945E+00]]))

def test_spcfs_last(pch) :
    spcfs = pch.spcfs
    np.testing.assert_array_equal(spcfs[(spcfs['Case'] == 300) & 
                                                 (spcfs['Node'] == 999999)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values,
                              np.array([[ 1.574133E-11,  1.004176E-10, -5.542533E+01, 
                                         -3.391945E+00, -1.079453E-11,  3.451849E-12]]))

def test_forces_cbush_first(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 100) & (forces['Element'] == 3000)][                                ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, np.array([[  7.242149E+00,  9.107042E+00,  6.346119E-01,                                                                             -8.025691E-04,  4.582147E-03, -1.816432E-05]]))

def test_forces_cbush_last(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 300) &  (forces['Element'] == 3001)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, np.array([[ 1.220864E+01, 3.471715E+00, -8.398896E+00,
-3.642999E-01,  5.762820E-04, -4.105315E-03]]))

def test_forces_celas2_first(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 100) & 
                                                (forces['Element'] == 4002)]['Fx'].values, -2.134340E-12)

def test_forces_celas2_last(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 300) & 
                                                (forces['Element'] == 4000)]['Fx'].values, -2.280053E-10)


def test_strains_cbush_first(pch) :
    strains = pch.strains
    np.testing.assert_array_equal(strains[(strains['Case'] == 100) & (strains['Element'] == 3001)][['XX', 'YY', 'ZZ', 'XY', 'XZ', 'YZ']].values, np.array([[-7.242150E-09,  9.107042E-09,  6.346119E-10,
                                                                                          -8.025691E-10, -4.582147E-09,  1.816432E-11]]))

def test_strains_cbush_last(pch) :
    strains = pch.strains
    np.testing.assert_array_equal(strains[(strains['Case'] == 300) & (strains['Element'] == 3000)][['XX', 'YY', 'ZZ', 'XY', 'XZ', 'YZ']].values, np.array([[ 1.220864E-08, -3.471715E-09,  8.398897E-09,
                                                                                          3.642999E-07,  5.762820E-10, -4.105315E-09]]))

def test_strains_celas2_last(pch) :
    strains = pch.strains
    np.testing.assert_array_equal(strains[(strains['Case'] == 100) & 
                                                (strains['Element'] == 4002)]['XX'].values,  0.000000E+00)

def test_strains_celas2_last(pch) :
    strains = pch.strains
    np.testing.assert_array_equal(strains[(strains['Case'] == 300) & 
                                                (strains['Element'] == 4000)]['XX'].values,  0.000000E+00)

def test_mpcfs_first(pch) :
    mpcfs = pch.mpcfs
    np.testing.assert_array_equal(mpcfs[(mpcfs['Case'] == 100) & 
                                                 (mpcfs['Node'] == 1005)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values,
                              np.array([[-4.489394E+00,  1.206788E+01,  1.730485E-01,
                                          3.772811E-03,  7.498462E-04,  3.944828E-06]]))

def test_mpcfs_last(pch) :
    mpcfs = pch.mpcfs
    np.testing.assert_array_equal(mpcfs[(mpcfs['Case'] == 300) & 
                                                 (mpcfs['Node'] == 999999)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values,
                              np.array([[-1.574110E-11, -1.004177E-10, 5.542533E+01, 
                                         3.391945E+00, 1.079242E-11, -3.451865E-12]]))

def test_mpcfs_vs_spcfs(pch) :
    spcfs = pch.spcfs 
    mpcfs = pch.mpcfs
    for case in pch.cases['ID'].unique() :
        np.testing.assert_almost_equal(spcfs[(spcfs['Case'] == case) & (spcfs['Node'] == 999999)]
                                    [['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, 
                                    -mpcfs[(mpcfs['Case'] == case) & (mpcfs['Node'] == 999999)]
                                    [['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, 5)
