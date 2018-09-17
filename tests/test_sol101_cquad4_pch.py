#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test the punch reader with file sol101_cquad4.pch
----------------------------------

"""

import os
import numpy as np
import pytest

from stress4analysis import punch

@pytest.fixture(scope="module")
def pch() :
    pch = punch.Punch()
    pch.read(os.path.join('..', 'data', 'sol101_cquad4.pch'))
    return pch
    

def test_forces_cquad4_first(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 1) & (forces['Element'] == 1002)][                                ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, np.array([[1.270960E+02, -9.627512E+01, -5.036841E+02,
1.624632E-02,  1.608728E-02, -1.942965E-01,
1.671325E+00,  1.242236E+00]]))

def test_forces_cquad4_last(pch) :
    forces = pch.forces
    np.testing.assert_array_equal(forces[(forces['Case'] == 3) &  (forces['Element'] == 1002)][['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, np.array([[-4.316655E+02,  1.420112E+02,  1.075152E+02,
-3.615346E+00, -9.042815E+00,  9.014618E-02,
-8.959941E+01, -5.100823E+02]]))

            
def test_strains_cquad4_first(pch) :
    strains = pch.strains
    np.testing.assert_array_equal(strains[(strains['Case'] == 1) & (strains['Element'] == 1002)][['XX', 'YY', 'ZZ', 'XY', 'XZ', 'YZ']].values, np.array([[  0.000000E+00,  1.134763E-06, -9.872628E-07, 
 -9.569998E-06, -3.874884E+01,  4.974971E-06, 
 -4.827471E-06,  5.659655E-06, -1.000000E+00, 
  2.343754E-04,  2.298427E-04, -1.107490E-02, 
 -4.498827E+01,  5.769558E-03, -5.305340E-03, 
  6.395968E-03]]))
    
                                     

def test_strains_cquad4_last(pch) :
    strains = pch.strains
    np.testing.assert_array_equal(strains[(strains['Case'] == 3) & (strains['Element'] == 1002)][['XX', 'YY', 'ZZ', 'XY', 'XZ', 'YZ']].values, np.array([[ 0.000000E+00, -3.418066E-06,  2.031863E-06,
3.603200E-06,  3.391913E-06, -1.000000E+00,
2.042789E-06,  7.972629E+01,  2.216998E-06,
1.352607E-02, -1.682089E-01,  5.138332E-03,
9.512899E-01, -1.348341E-02, -1.682516E-01,
1.079543E-01]]))

def test_mpcfs_vs_spcfs(pch) :
    spcfs = pch.spcfs 
    mpcfs = pch.mpcfs
    for case in pch.cases['ID'].unique() :
        np.testing.assert_almost_equal(spcfs[(spcfs['Case'] == case) & (spcfs['Node'] == 999999)]
                                    [['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, 
                                    -mpcfs[(mpcfs['Case'] == case) & (mpcfs['Node'] == 999999)]
                                    [['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].values, 5)
