class RawDataMaker:

    def __init__(self, benchmarks, delimiter=","):
        self.data = benchmarks
        self.delimiter = delimiter

    def get_raw_data(self):

        output = ""

        for key in self.data:
            output += key + self.delimiter
        output = output[:-1] + "\n"

        for key, value in self.data.iteritems():
            output += value + self.delimiter
        output = output[:-1] + "\n"

        return output