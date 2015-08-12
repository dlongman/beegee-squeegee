import csv
import time
from Reading import Reading as Reading

### TODO ### Add documentation to classes and methods

class AccuChekMobileParser(object):

    # this file has some summary data in row 2 with the headers in row 1
    # the result data is then in row 4 with the headers in row 3

    def __init__(self, file_location):
        self.file_path = file_location
        self.serial_number = ''
        self.last_download_date = ''
        self.HEADER_ROW_COUNT = 2
        self.result_data = []

    def read_result_data(self, notifier):

        headers = ['Date', 'Time', 'Result', 'Unit', 'TempWarning', \
                   'OutOfTargetRange', 'Other', 'BeforeMeal', 'AfterMeal', 'ControlTest']

        with open(self.file_path, 'rb') as dataFile:

            reader = csv.DictReader(dataFile, fieldnames=headers, delimiter=';')

            # skip the header rows and the 2 rows of summary data
            for x in range(0, self.HEADER_ROW_COUNT + 1):
                next(reader, None)

            for row in reader: 
                # TODO: Replace with a dict to make sure there are no duplicates
                if row['Result'] != None:
                    reading = Reading(row['Date'], row['Time'], row['Result'], row['Unit'])
                    self.result_data.append(reading)
                    notifier(reading)
                else:
                    pass # this data has no reading so ignore it

    def read_header_data(self):

        headers = ['Serial Number', 'Download Date', 'Download Time']

        with open(self.file_path, 'rb') as df:

            counter = 0
            reader = csv.DictReader(df, headers, delimiter=';')

            for row in reader:
                counter = counter + 1
                if counter == 1:
                    # these are the headers so ignore
                    self.serial_number = ''
                elif counter == 2:
                    # this is the summary data
                    self.serial_number = row['Serial Number']
                    self.last_download_date = self.convert_date_time(row['Download Date'], row['Download Time'])
                else:
                    # this is the start of the real data
                    break

    def convert_date_time(self, d, t):
        return time.strptime(d + t, "%d.%m.%Y%H:%M")

    def __str__(self):
        return 'This is the result data for meter {0}. ' \
               'The data was downloaded on {1}\\{2}\\{3} at {4}:{5}.\n' \
               'It contains {6} readings' \
               .format(self.serial_number, self.last_download_date.tm_mday, self.last_download_date.tm_mon, \
                       self.last_download_date.tm_year, self.last_download_date.tm_hour, \
                       self.last_download_date.tm_min, len(self.result_data))

if __name__ == "__main__":

    def callback(data):
        print "Processed data for {0}".format(data)
        ### TODO ### process data into sql db

    parser = AccuChekMobileParser('./data/DiaryU101341933-14Dec2014.csv')
    #parser = AccuChekMobileParser('./data/DiaryU101341933-12Aug2015.csv')
    parser.read_header_data()
    parser.read_result_data(callback)
    parser.file_path = './data/DiaryU101341933-12Aug2015.csv'
    parser.read_header_data()
    parser.read_result_data(callback)
    print parser
