import unittest
from aircrack.airodumpap import AirodumpAp #@UnresolvedImport

class TestAirodumpAp(unittest.TestCase):
	
	def setUp(self):
		self.ap = AirodumpAp()

	def test_initLoad(self):
		data =	[	[1,'2012-05-10 11:53:54','2012-05-10 11:53:54',4,5,6,7,8,9,10,11,12,13,14,15],
					[2,'2012-05-10 11:53:54','2012-05-10 11:53:54',4,5,6,7,8,9,10,11,12,13,14,150]	]
		ap = AirodumpAp(data)
		self.assertTrue(len(ap) == 2)
		record = ap[0]
		self.assertTrue(record[0] == 1)
		self.assertTrue(record[14] == 15)
		record = ap[1]
		self.assertTrue(record[0] == 2)
		self.assertTrue(record[14] == 150)

	def test_set_get(self):
		self.ap.add([1,'2012-05-10 11:53:54','2012-05-10 11:53:54',4,5,6,7,8,9,10,11,12,13,14,15])
		self.assertTrue(len(self.ap) == 1)
		record = self.ap[0]
		self.assertTrue(record[0] == 1)
		self.assertTrue(record[14] == 15)
		
	def test_print(self):
		self.ap.add([1,'2012-05-10 11:53:54','2012-05-10 11:53:54',4,5,6,7,8,9,10,11,12,13,14,15])
		str(self.ap)

if __name__ == '__main__':
	unittest.main()
