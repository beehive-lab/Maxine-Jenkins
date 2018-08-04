# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.test import TestCase
import unittest
from utilities import BenchMiner

# Create your tests here.


class MinerTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_mine_all_specjvms_onemissing(self):
        f = open("visualizer/static/test_files/console_whole", "r")
        spec_miner = BenchMiner(f.read())

        spec_result = spec_miner.mine_all_specjvms()

        expected = {
            'startup': "8.62",
            'compiler': "25.14",
            'compress': "21",
            'crypto': "21.78",
            'derby': "interpt/failed",
            'mpegaudio': "10.76",
            'scimark': "missing",
            'serial': "6.94",
            'spec_sunflow': "21.74",
            'xml': "21.96"
        }

        f.close()
        self.assertEquals(spec_result, expected)

    def test_mine_all_specjvms_oneinterrupted(self):
        f = open("visualizer/static/test_files/console_one_specjvm_interrupt", "r")
        spec_miner = BenchMiner(f.read())

        spec_result = spec_miner.mine_all_specjvms()

        expected = {
            'startup': "8.62",
            'compiler': "25.14",
            'compress': "interpt/failed",
            'crypto': "21.78",
            'derby': "interpt/failed",
            'mpegaudio': "10.76",
            'scimark': "missing",
            'serial': "6.94",
            'spec_sunflow': "21.74",
            'xml': "21.96"
        }

        f.close()
        self.assertEquals(spec_result, expected)

    def test_mine_all_dacapos_somefailed(self):
        f = open("visualizer/static/test_files/console_dacapos", "r")
        spec_miner = BenchMiner(f.read())

        spec_result = spec_miner.mine_all_dacapos()

        expected = {
            'avrora': "14490",
            'batik': "interpt/failed",
            'eclipse': "119405",
            'fop': "5989",
            'h2': "39575",
            'jython': "69780",
            'luindex': "5145",
            'lusearch': "9180",
            'pmd': "35371",
            'sunflow': "16847",
            'tomcat': "24990",
            'tradebeans': "interpt/failed",
            'tradesoap': "interpt/failed",
            'xalan': "11545",
        }

        f.close()
        self.assertEquals(spec_result, expected)


if __name__ == '__main__':
    unittest.main()
