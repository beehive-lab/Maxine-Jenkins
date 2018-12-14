import re

class BenchMiner:

    """
    This class provides an API for the retrieval of benchmark data from a string.
    The string has the contents of the console output from the Jenkins Pipeline
    """

    def __init__(self, console):
        #contains the whole console output of the pipeline
        self.console_inp = console

        #contains dacapo console
        self.console_dacapo = ""

        #contains specjvm_console
        self.console_specjvm = ""

    def mine_specjvm(self, sub_bench):

        """
        Looks for the result of a specific SpecJvm benchmark in the console output.

        :param sub_bench: The name of the sub-bench, for example 'startup'
        :return:  The result of the benchmark/ "missing" if missing/ "interpt/failed" if failed or interrupted
        """

        search_term = r".*-jar.*SPECjvm2008.jar.*" + sub_bench

        search_result = re.search(search_term, self.console_specjvm)

        # if the sub-benchmark was not executed, return "missing"
        if search_result == None:
            return "missing"

        sub_console = self.console_specjvm[search_result.start():]
        search_term = r".*\[Pipeline\].*"
        search_result = re.search(search_term, sub_console)
        if search_result == None:
            return "missing"
        sub_bench_output = sub_console[0:search_result.end()]

        # look for the composite result inside the output of the sub benchmark
        search_term = r".*Noncompliant composite result: .*"
        search_result = re.search(search_term, sub_bench_output)

        # if the benchark was interrupted (no result printed), return "interpt/failed"
        if search_result == None:
            return "interpt/failed"

        # the raw benchmark value is second word from the end, in the result line
        raw_benchmark = search_result.group().split(" ")[-2]

        return raw_benchmark

    def mine_all_specjvms(self):

        """
        Looks for the result of all the specjvm benchmarks

        :return:  A dict containing the results of the sub-benchmarks
        """

        # narrow the search by finding the execution of the first test
        search_term = r".*-jar.*SPECjvm2008.jar.*"

        search_result = re.search(search_term, self.console_inp)

        if search_result == None:
            return {
                'startup': "missing", 'compiler': "missing", 'compress': "missing", 'crypto': "missing", 'derby': "missing",
                'mpegaudio': "missing", 'scimark': "missing", 'serial': "missing", 'spec_sunflow': "missing", 'xml': "missing"
            }

        self.console_specjvm = self.console_inp[search_result.start():]

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

        """
        Looks for the result of a specific Dacapo benchmark in the console output.

        :param sub_bench: The name of the sub-bench, for example 'avrora'
        :return:  The result of the benchmark/ "missing" if missing/ "interpt/failed" if failed or interrupted
        """

        search_term = r".*-jar.*dacapo-9.12-MR1-bach.jar.*" + sub_bench
        search_result = re.search(search_term, self.console_dacapo)

        # subtest missing
        if search_result == None:
            return "missing"

        sub_console = self.console_dacapo[search_result.start():]

        search_term = r"===== DaCapo 9.12-MR1 " + sub_bench + r" PASSED in [0-9]+ msec ====="
        search_result = re.search(search_term, sub_console)

        # subtest failed
        if search_result == None:
            return "interpt/failed"

        # the raw benchmark value is second word from the end, in the result line
        raw_benchmark = search_result.group().split(" ")[-3]

        return raw_benchmark

    def mine_all_dacapos(self):

        """
        Looks for the result of all the dacapo benchmarks

        :return:  A dict containing the results of the sub-benchmarks
        """

        # firstly, we narrow the search for the dacapo results
        search_term = r".*-jar.*dacapo-9.12-MR1-bach.jar.*"
        search_result = re.search(search_term, self.console_inp)

        if search_result == None:
            return {
                'avrora': "missing", 'batik': "missing", 'eclipse': "missing", 'fop': "missing", 'h2': "missing", 'jython': "missing", 'luindex': "missing",
                'lusearch': "missing", 'pmd': "missing", 'sunflow': "missing", 'tomcat': "missing", 'tradebeans': "missing", 'tradesoap': "missing", 'xalan': "missing"
            }

        self.console_dacapo = self.console_inp[search_result.start():]

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
