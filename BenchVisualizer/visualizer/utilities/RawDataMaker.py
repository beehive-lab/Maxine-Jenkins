class RawDataMaker:

    """
    This class serializes benchmark data (dicts) to CSV-readable format
    """

    def __init__(self, benchmarks, delimiter=","):
        self.data = benchmarks
        self.delimiter = delimiter

    def get_raw_data(self):

        titles = self.data['titles']
        zipped_list = self.data['zipped_list']

        output = ""

        for title in titles:
            output += title + self.delimiter
        output = output[:-1] + "\n"

        for build in zipped_list:
            for bench in build:
                output += bench + self.delimiter
            output = output[:-1] + "\n"

        return output
