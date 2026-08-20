import unittest
import workflow_metadata as m

class TestMetadata(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(m.ENHANCE_ID, 'ENH-E8')
        self.assertEqual(m.GATES['G01'], 'SINGLE_EXECUTION')
        self.assertEqual(m.GATES['G02'], 'WORK_PACKAGE')
        self.assertEqual(m.G02_PACKAGES, ['P01','P02','P03'])

if __name__=='__main__': unittest.main()
