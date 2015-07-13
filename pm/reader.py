#!/usr/bin/env python3

import csv
import xlsxwriter

from xlsxwriter.utility import xl_rowcol_to_cell

class Reader:
    def __init__(self):
        self.project = {}


    def read(self, file_name):
        with open(file_name, 'r') as csv_file:
            data = csv.reader(csv_file, delimiter=';', quotechar='"')

            for line in data:
                if len(line) > 4:
                    self.add_entry(line)
                  

    def add_entry(self, line):
        if line[4] != "E1":
            month = line[0].split("-")[1]
            cost_unit = line[4]
            hours = float(line[-1].replace(",", "."))

            if "Gesamt" not in cost_unit:
                if cost_unit not in self.project.keys():
                    self.project[cost_unit] = {}

                if month not in self.project[cost_unit].keys():
                    self.project[cost_unit][month]= []

                self.project[cost_unit][month].append(hours)


class Statistics:
    def write(self, data, file_name):
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        for cost_unit in sorted(data.keys()):
            worksheet.write(row, 0, cost_unit)

            for month in sorted(data[cost_unit].keys()):
                col += 1
                costs = data[cost_unit][month]
                worksheet.write(row, col, sum(costs))

            # generate statistics
            start = xl_rowcol_to_cell(row,1)
            stop = xl_rowcol_to_cell(row,col)
            worksheet.write(0, col+1, '=SUM('+start+":"+stop+")")
	    # new cost unit and hence a new row
            row += 1
            col = 1

        workbook.close()


def main():
    reader = Reader()
    reader.read("data.csv")
    print(reader.project)
    stats = Statistics()

    stats.write(reader.project, "test.xslx")


if __name__ == "__main__":
    main()
