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
        :return:  The result of the benchmark/ "0" if missing/ "-1" if failed or interrupted
        """

        search_term = r".*mx.*vm.*-jar.*SPECjvm2008.jar.*" + sub_bench

        search_result = re.search(search_term, self.console_specjvm)

        # if the sub-benchmark was not executed, return 0
        if search_result == None:
            return "0"

        sub_console = self.console_specjvm[search_result.start():]
        # "+ true" comes after the interrupt signal
        search_term = r".*\+ true.*"
        search_result = re.search(search_term, sub_console)
        '''
        All the specjvm commands should ALWAYS be followed by a 'true' command.
        For the sake of coverage, in the non - likely event that 'true is not found' treat the benchmark as missing.
        '''
        if search_result == None:
            return "0"
        sub_bench_output = sub_console[0:search_result.end()]

        # look for the composite result inside the output of the sub benchmark
        search_term = r".*Noncompliant composite result: .*"
        search_result = re.search(search_term, sub_bench_output)

        # if the benchark was interrupted (no result printed), return -1
        if search_result == None:
            return "-1"

        # the raw benchmark value is second word from the end, in the result line
        raw_benchmark = search_result.group().split(" ")[-2]

        return raw_benchmark

    def mine_all_specjvms(self):

        """
        Looks for the result of all the specjvm benchmarks

        :return:  A dict containing the results of the sub-benchmarks
        """

        # narrow the search by finding the execution of the first test
        search_term = r".*mx.*vm.*-jar.*SPECjvm2008.jar.*"

        search_result = re.search(search_term, self.console_inp)

        if search_result == None:
            return {
                'startup': "0", 'compiler': "0", 'compress': "0", 'crypto': "0", 'derby': "0",
                'mpegaudio': "0", 'scimark': "0", 'serial': "0", 'spec_sunflow': "0", 'xml': "0"
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
        :return:  The result of the benchmark/ "0" if missing/ "-1" if failed or interrupted
        """

        search_term = r".*mx.*vm.*-jar.*dacapo-9.12-bach.jar.*" + sub_bench
        search_result = re.search(search_term, self.console_dacapo)

        #subtest missing
        if search_result == None:
            return "0"

        sub_console = self.console_dacapo[search_result.start():]

        search_term = r"===== DaCapo 9.12 " + sub_bench + r" PASSED in [0-9]+ msec ====="
        search_result = re.search(search_term, sub_console)

        #subtest failed
        if search_result == None:
            return "-1"

        # the raw benchmark value is second word from the end, in the result line
        raw_benchmark = search_result.group().split(" ")[-3]

        return raw_benchmark

    def mine_all_dacapos(self):

        """
        Looks for the result of all the dacapo benchmarks

        :return:  A dict containing the results of the sub-benchmarks
        """

        # firstly, we narrow the search for the dacapo results
        search_term = r".*mx.*vm.*-jar.*dacapo-9.12-bach.jar.*"
        search_result = re.search(search_term, self.console_inp)

        if search_result == None:
            return {
                'avrora': "0", 'batik': "0", 'eclipse': "0", 'fop': "0", 'h2': "0", 'jython': "0", 'luindex': "0",
                'lusearch': "0", 'pmd': "0", 'sunflow': "0", 'tomcat': "0", 'tradebeans': "0", 'tradesoap': "0", 'xalan': "0"
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
