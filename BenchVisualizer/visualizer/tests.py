# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.test import TestCase
import unittest
from utilities import BenchMiner, DatabaseManager

# Create your tests here.


class MinerTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_mine_all_specjvms_onemissing(self):
        f = open("static/test_files/console_whole", "r")
        spec_miner = BenchMiner(f.read())

        spec_result = spec_miner.mine_all_specjvms()

        expected = {
            'startup': "8.62",
            'compiler': "25.14",
            'compress': "21",
            'crypto': "21.78",
            'derby': "-1",
            'mpegaudio': "10.76",
            'scimark': "0",
            'serial': "6.94",
            'spec_sunflow': "21.74",
            'xml': "21.96"
        }

        f.close()
        self.assertEquals(spec_result, expected)

    def test_mine_all_specjvms_oneinterrupted(self):
        f = open("static/test_files/console_one_specjvm_interrupt", "r")
        spec_miner = BenchMiner(f.read())

        spec_result = spec_miner.mine_all_specjvms()

        expected = {
            'startup': "8.62",
            'compiler': "25.14",
            'compress': "-1",
            'crypto': "21.78",
            'derby': "-1",
            'mpegaudio': "10.76",
            'scimark': "0",
            'serial': "6.94",
            'spec_sunflow': "21.74",
            'xml': "21.96"
        }

        f.close()
        self.assertEquals(spec_result, expected)


class DatabaseManagerTests(unittest.TestCase):

    def test_refresh(self):

        '''
        TODO: database tests should be handled differently
        '''

        db = DatabaseManager()
        job1 = {
            'name': "Job1",
            'description': "first job",
            'is_running': "True",
            'is_enabled': "True"
        }
        job2 = {
            'name': "Job2",
            'description': "second job",
            'is_running': "False",
            'is_enabled': "False"
        }
        jobs = [job1, job2]
        result = db.refresh_database(jobs)
        expected = "ok"
        self.assertEquals(result, expected)




if __name__ == '__main__':
    unittest.main()
