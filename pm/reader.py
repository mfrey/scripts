#!/usr/bin/env python3

import csv

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

            if month not in self.project.keys():
                self.project[month] = {}


            if "Gesamt" not in cost_unit:
                 if cost_unit not in self.project[month].keys():
                     self.project[month][cost_unit] = []

                 self.project[month][cost_unit].append(hours)
                            

def main():
    reader = Reader()
    reader.read("data.csv")
    print(reader.project)


if __name__ == "__main__":
    main()
