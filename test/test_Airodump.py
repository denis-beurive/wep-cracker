import unittest
from aircrack.airodump import * #@UnresolvedImport
from csvsimple import * #@UnresolvedImport

CSV = 'data/out-01.csv'

class TestAirodump(unittest.TestCase):
    
	def setUp(self):
		### Do it only once.
		# setFormat('legend right align', 20)
		self.csv_data = loadCsv(CSV)
        
	def test_associated(self):
		getAssociatedStations(self.csv_data)
		
	def test_getBestAssociatedStation(self):
		best = getBestAssociatedStation(self.csv_data)
		if len(best) > 0: print ("Best candidate is %s" % best)
		
	def test_print(self):
		#print("Number of APs: %d" % len(self.csv_data['AP']))
		#print("Number of STATIONs: %d" % len(self.csv_data['STATION']))
		print(csv2str(self.csv_data))
		print ("ok")

if __name__ == '__main__':
    unittest.main()
