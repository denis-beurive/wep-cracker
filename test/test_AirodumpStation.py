import unittest
from aircrack.airodumpstation import AirodumpStation #@UnresolvedImport
 
class TestAirodumpStation(unittest.TestCase):
    
    def setUp(self):
        self.ap = AirodumpStation()

    def test_initLoad(self):
        data =    [    [1, '2012-05-10 11:53:54', '2012-05-10 11:53:54', 4, 5, 6, 7],
                       [2, '2012-05-10 11:53:54', '2012-05-10 11:53:54', 4, 5, 6, 70]    ]
        ap = AirodumpStation(data)
        self.assertTrue(len(ap) == 2)
        record = ap[0]
        self.assertTrue(record[0] == 1)
        self.assertTrue(record[6] == 7)
        record = ap[1]
        self.assertTrue(record[0] == 2)
        self.assertTrue(record[6] == 70)

    def test_set_get(self):
        self.ap.add([1,'2012-05-10 11:53:54','2012-05-10 11:53:54',4,5,6,7])
        self.assertTrue(len(self.ap) == 1)
        record = self.ap[0]
        self.assertTrue(record[0] == 1)
        self.assertTrue(record[6] == 7)
        
    def test_print(self):
        self.ap.add([1,'2012-05-10 11:53:54','2012-05-10 11:53:54',4,5,6,7])
        str(self.ap)

if __name__ == '__main__':
    unittest.main()
