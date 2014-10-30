#!/usr/bin/env python2.7

import sys
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class Castalia:
    def __init__(self):
        print("gna")

class CastaliaResultParser:
    def __init__(self):
        self.results = {} 
        self.nodes = [] 

    def _parse_line(self, line):
        # let's split the line by '|'
        data = line.split('|')
        # well, it's actual data and not a header
        if len(data) > 1:
            # let's filter empty elements and newlines from the list
            data = [element for element in data if len(element) > 0 and element != '\n']

            if data[0] != ' ':
                # let's check if we have multiple parameters
                parameters = data.pop(0).strip().split(',')
                # get the keys
                parameters = [parameter.split('=')[1] for parameter in parameters]
                # our future dict key
                key = ','.join(parameters)

                if key not in self.results.keys():
                    self.results[key] = []

                for value in data:
                    self.results[key].append(float(value))


    def read_breakdown_packets(self, filename):
        with open(filename, "r") as filehandle:
            for line in filehandle:
                self._parse_line(line)


    def plot_histogram(self):
        data = {}

        # prepare the data
        for key in self.results.keys():
            payload, rate, node = key.split(',')

            if payload not in data.keys():
                data[payload] = {}      
                   
            if node not in data[payload].keys():
                data[payload][node] = {}

            if rate not in data[payload][node].keys():
                data[payload][node][rate] = []

            data[payload][node][rate] = self.results[key]

        print("Generating bar plots for packet breakdown: ")
        # let's generate plots
        for payload in data.keys():
            for node in data[payload].keys():
                for rate in sorted(data[payload][node],key=int):

                    rates.append(float(rate))
                    failed.append(data[payload][node][rate][0])
                    success.append(data[payload][node][rate][1])

                sys.stdout.write('.')
                title = "Packet Breakdown (#Nodes: " + node + " Payload: " + payload + " Bytes)" 
                self.generate_bar_plot("packets_breakdown_" + payload + "_" + node + ".png", title, rates, [failed, success], "rate", "packets", ['failed','success'])
        print("\n")

    def plot_breakdown_packets(self):
        data = {}

        # prepare the data
        for key in self.results.keys():
            payload, rate, node = key.split(',')

            if payload not in data.keys():
                data[payload] = {}      
                   
            if node not in data[payload].keys():
                data[payload][node] = {}

            if rate not in data[payload][node].keys():
                data[payload][node][rate] = []

            data[payload][node][rate] = self.results[key]

        print("Generating bar plots for packet breakdown: ")
        # let's generate plots
        for payload in data.keys():
            for node in data[payload].keys():
                rates = [] 
                failed = []
                success = []

                for rate in sorted(data[payload][node],key=int):
                    rates.append(float(rate))
                    failed.append(data[payload][node][rate][0])
                    success.append(data[payload][node][rate][1])

                sys.stdout.write('.')
                title = "Packet Breakdown (#Nodes: " + node + " Payload: " + payload + " Bytes)" 
                self.generate_bar_plot("packets_breakdown_" + payload + "_" + node + ".png", title, rates, [failed, success], "rate", "packets", ['failed','success'])
        print("\n")

    def read_multiple_columns(self, filename):
        with open(filename, "r") as filehandle:
            for line in filehandle:
                preamble = line.split('|')

                if len(preamble) > 1:
                    if preamble[0] == ' ':
                       preamble.pop(0)
                       self.nodes = [element.split('=')[-1].strip() for element in preamble]

                self._parse_line(line)


    def plot(self, title, filename, xlabel, ylabel):
        data = {} 
        nr_of_nodes = -1

        for key in self.results.keys():
            payload, rate, node = key.split(',')

            if payload not in data.keys():
                data[payload] = {}      

            if node not in data[payload].keys():
                data[payload][node] = {}

            if rate not in data[payload][node].keys():
                data[payload][node][rate] = []

            data[payload][node][rate] = self.results[key]

        print("Generating line plots for " + title + ": ")
        # let's generate plots
        for payload in data.keys():
            for node in data[payload].keys():
                rates = [] 
                average = []
                minimum = []
                maximum = [] 

                for rate in sorted(data[payload][node],key=int):
                    rates.append(float(rate))
                    average.append(data[payload][node][rate][0])
                    minimum.append(data[payload][node][rate][1])
                    maximum.append(data[payload][node][rate][2])

                sys.stdout.write('.')
                title = "Average Latency (#Nodes: " + node + " Payload: " + payload + " Bytes)" 
                current_filename = filename + "-" + payload + "-" + node + ".png"
                figure, axis = plt.subplots(1)
                axis.plot(rates, average, lw=2, label=title, color='#003366')
                axis.fill_between(rates, [i + j for i, j in zip(average, maximum)], [i - j for i, j in zip(average, minimum)], facecolor='#003366', alpha=0.5)
                axis.set_title(title)
                axis.set_xlabel(xlabel)
                axis.set_ylabel(ylabel)
                axis.grid()
                figure.savefig(current_filename)
                plt.close()
                print("\n")

    def plot_ext(self, title, filename, xlabel, ylabel):
        data = {} 
        nr_of_nodes = -1

        for key in self.results.keys():
            payload, rate = key.split(',')

            if payload not in data.keys():
                data[payload] = {}      

            if rate not in data[payload].keys():
                data[payload][rate] = {}

            data[payload][rate] = self.results[key]
            # store the number of nodes
            nr_of_nodes = len(self.results[key])

        print("Generating line plots for " + title + ": ")
        # let's generate plots
        for payload in data.keys():
            # we create a new plot for each #nodes 
            for current_node in range(nr_of_nodes):
                rates = []  
                reception_rate = []
                sys.stdout.write('.')
                for rate in sorted(data[payload], key=int):
                    rates.append(rate)
                    reception_rate.append(float(data[payload][rate][current_node]))

                # create the title of the figure
                current_title = title + "(#Nodes = " + self.nodes[current_node] + ", Payload = " + payload + ")" 
                current_filename = filename + "-" + payload + "-" + self.nodes[current_node] + ".png"
                # finally let's plot the reception rate 
                self.generate_line_plot(current_filename, current_title, [rates], [reception_rate], xlabel, ylabel, [])


    def generate_line_plot(self, filename, title, xlist, ylist, xlabel, ylabel, labels): 
        figure = plt.figure()
        axis = figure.add_subplot(111)
        markers = ['s','^','v','2','*','3','d']

        for index, value in enumerate(xlist):
            if len(xlist) > 1:
                plt.plot(value, ylist[index], drawstyle="line", lw=2.5, label=labels[index])
            else:
                plt.plot(value, ylist[index], drawstyle="line", lw=2.5, color="#003366")

        plt.title(title)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        plt.grid()
        plt.savefig(filename)

    def generate_line_plot_ext(self, filename, title, xlist, mu, sigma, xlabel, ylabel): 
        figure, axis = plt.subplots(1)
        axis.plot(xlist, mu, lw=2, label=title, color='#003366')
        axis.fill_between(xlist, [i + j for i, j in zip(mu, sigma)], [i - j for i, j in zip(mu, sigma)], facecolor='#003366', alpha=0.5)
        axis.set_title(title)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid()
        figure.savefig(filename)

    
    def generate_bar_plot(self, filename, title, xdata, ydata, xlabel, ylabel, labels): 
        figure, axis = plt.subplots()

        index = np.arange(xdata[-1])
        width = 0.5

        bar_widths = -1

        if bar_widths > 0:
            axis.bar(index, ydata, bar_widths)
        else:
            axis.bar(index, ydata[1], width, color="#990000")
            axis.bar(index+width, ydata[0], width, color="#003366")

        axis.set_ylabel(ylabel)
        axis.set_xlabel(xlabel)

        #axis.set_xticks(index + width)

        axis.set_title(title)
        #axis.legend((ydata[0][0], ydata[1][0]), (labels[0], labels[1]) )
        axis.grid(axis="y")

        plt.savefig(filename)
        plt.close()

    def prepare_line_plot(self, filename, title, xlabel, ylabel, data):
        xlist = [] 
        std = [] 
        mean = [] 

        for key in sorted(data):
            xlist.append(key)
            mean.append(float(np.mean(data[key])))
            std.append(float(np.std(data[key])))

        self.generate_line_plot(filename, title, xlist, mean, std, xlabel, ylabel) 


def main():
    parser = CastaliaResultParser()
    
    parser.read_multiple_columns("application.txt")
    parser.plot_histogram()
    #parser.read_multiple_columns("latency.txt")
    #parser.plot("Average Latency", "average_latency", "rate", "latency")
    parser.nodes = []
    parser.results = {}

    parser.read_multiple_columns("received.txt")
    parser.plot_ext("Received Packets", "received_packets", "rate", "packets")
    parser.results = {}
    
    parser.read_multiple_columns("reception.txt")
    parser.plot_ext("Packet Reception Rate", "packet_reception_rate", "rate", "packet reception rate")
    parser.results = {}

    parser.read_breakdown_packets("breakdown.txt")
    parser.plot_breakdown_packets()

if __name__ == "__main__":
    main()

