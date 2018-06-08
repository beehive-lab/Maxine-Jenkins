import re

class BenchMiner:

    def __init__(self, console):
        #contains the whole console output of the pipeline
        self.console_inp = console

        #contains dacapo console
        self.console_dacapo = ""

        #contains specjvm_console
        self.console_spec_jvm = ""

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


    def mine_dacapo(self, sub_bench):

        search_term = r"===== DaCapo 9.12 " + sub_bench + r" PASSED in [0-9]+ msec ====="
        search_result = re.search(search_term, self.console_dacapo)

        #subtest missing or failed
        if search_result == None:
            return "0"

        # the raw benchmark value is second word from the end, in the result line
        raw_benchmark = search_result.group().split(" ")[-3]

        return raw_benchmark

    def mine_all_dacapos(self):

        #firstly, we narrow the search for the dacapo results
        search_term = r".*mx.*vm.*-jar.*dacapo-9.12-bach.jar.*"
        search_result = re.search(search_term, self.console_inp)
        self.console_dacapo = self.console_inp[search_result.start():]

        #avrora batik eclipse fop h2 jython luindex lusearch pmd sunflow tomcat tradebeans tradesoap xalan

        return {
            'avrora': self.mine_dacapo('avrora'),
            'batik': self.mine_dacapo('batik'),
            'eclipse': self.mine_dacapo('eclipse'),
            'fop': self.mine_dacapo('fop'),
            'h2': self.mine_dacapo('h2'),
            'jython': self.mine_dacapo('jython'),
            'luindex': self.mine_dacapo('luindex'),
            'lusearch': self.mine_dacapo('lusearch'),
            'pmd': self.mine_dacapo('pmd'),
            'sunflow': self.mine_dacapo('sunflow'),
            'tomcat': self.mine_dacapo('tomcat'),
            'tradebeans': self.mine_dacapo('tradebeans'),
            'tradesoap': self.mine_dacapo('tradesoap'),
            'xalan': self.mine_dacapo('xalan')
        }
