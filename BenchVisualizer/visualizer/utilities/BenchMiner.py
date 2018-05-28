import re

class BenchMiner:

    def __init__(self, console):
        self.console_inp = console

    def mine_specjvm(self, sub_bench):

        search_term = r".*mx.*vm.*-jar.*SPECjvm2008.jar.*" + sub_bench

        search_result = re.search(search_term, self.console_inp)

        #if the sub-benchmark was not executed, return 0
        if search_result == None:
            return "0"

        sub_console = self.console_inp[search_result.start():]
        search_term = r".*Noncompliant composite result: .*"
        search_result = re.search(search_term, sub_console)

        #if the benchark was interrupted (no result printed), return -1
        if search_result == None:
            return "-1"

        #the raw benchmark value is second word from the end, in the result line
        raw_benchmark = search_result.group().split(" ")[-2]

        return raw_benchmark

    def mine_all_specjvms(self):

        return {
            'startup': self.mine_specjvm('startup'),
            'compiler': self.mine_specjvm('compiler'),
            'compress': self.mine_specjvm('compress'),
            'crypto': self.mine_specjvm('crypto'),
            'derby': self.mine_specjvm('derby'),
            'mpegaudio': self.mine_specjvm('mpegaudio'),
            'scimark': self.mine_specjvm('scimark'),
            'serial': self.mine_specjvm('serial'),
            'spec_sunflow': self.mine_specjvm('sunflow'),
            'xml': self.mine_specjvm('xml')
        }


    def mine_dacapo(self):
        return self.console_inp
