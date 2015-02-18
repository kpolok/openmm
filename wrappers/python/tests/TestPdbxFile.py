import unittest
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
import simtk.openmm.app.element as elem

class TestPdbxFile(unittest.TestCase):
    """Test the PDBx/mmCIF file parser"""
 
    def test_Triclinic(self):
        """Test parsing a file that describes a triclinic box."""
        pdb = PDBxFile('systems/triclinic.pdbx')
        self.assertEqual(len(pdb.positions), 8)
        expectedPositions = [
            Vec3(1.744, 2.788, 3.162),
            Vec3(1.048, 0.762, 2.340),
            Vec3(2.489, 1.570, 2.817),
            Vec3(1.027, 1.893, 3.271),
            Vec3(0.937, 0.825, 0.009),
            Vec3(2.290, 1.887, 3.352),
            Vec3(1.266, 1.111, 2.894),
            Vec3(0.933, 1.862, 3.490)]*nanometers
        for (p1, p2) in zip(expectedPositions, pdb.positions):
            self.assertVecAlmostEqual(p1, p2)
        expectedVectors = [
            Vec3(2.5, 0, 0),
            Vec3(0.5, 3.0, 0),
            Vec3(0.7, 0.9, 3.5)]*nanometers
        for (v1, v2) in zip(expectedVectors, pdb.topology.getPeriodicBoxVectors()):
            self.assertVecAlmostEqual(v1, v2, 1e-6)
        self.assertVecAlmostEqual(Vec3(2.5, 3.0, 3.5)*nanometers, pdb.topology.getUnitCellDimensions(), 1e-6)
        for atom in pdb.topology.atoms():
            if atom.index < 4:
                self.assertEqual(elem.chlorine, atom.element)
                self.assertEqual('Cl', atom.name)
                self.assertEqual('Cl', atom.residue.name)
            else:
                self.assertEqual(elem.sodium, atom.element)
                self.assertEqual('Na', atom.name)
                self.assertEqual('Na', atom.residue.name)

    def assertVecAlmostEqual(self, p1, p2, tol=1e-7):
        unit = p1.unit
        p1 = p1.value_in_unit(unit)
        p2 = p2.value_in_unit(unit)
        scale = max(1.0, norm(p1),)
        for i in range(3):
            diff = abs(p1[i]-p2[i])/scale
            self.assertTrue(diff < tol)


if __name__ == '__main__':
    unittest.main()