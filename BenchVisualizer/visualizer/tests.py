# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.test import TestCase
import unittest
from utilities import BenchMiner

# Create your tests here.


class MinerTests(unittest.TestCase):

    def setUp(self):
        self.f = open("static/test_files/console_whole", "r")
        self.spec_miner = BenchMiner(self.f.read())

    def tearDown(self):
        self.f.close()

    def test_mine_all_specjvms_onemissing(self):

        spec_result = self.spec_miner.mine_all_specjvms()

        expected = {
            'startup': "8.62",
            'compiler': "25.14",
            'compress': "21",
            'crypto': "21.78",
            'derby': "10.76",
            'mpegaudio': "10.76",
            'scimark': "0",
            'serial': "6.94",
            'spec_sunflow': "21.74",
            'xml': "21.96"
        }

        self.assertEquals(spec_result, expected)




if __name__ == '__main__':
    unittest.main()
