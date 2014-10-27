#!/usr/bin/env python2.7

import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class CastaliaResultParser:
    def __init__(self):
        print("start it")

    def read(self, filename):
        results = {} 
        with open(filename, "r") as filehandle:
            for line in filehandle:
                # delimiter is apperantly a '|'
                data = line.split('|')
                # well, it's actual data and not a header
                if len(data) > 1:
                    # let's filter empty elements and newlines from the list
                    data = [element for element in data if len(element) > 0 and element != '\n']
                    x = data.pop(0).strip()

                    if x.startswith("offset"): 
                        x = float(x.split("=")[1])
                        print x
                        y = [float(element) for element in data]

                        if x not in results.keys():
                            results[x] = y
        # print(results)
        return results

    def read_received_packets(self, filename):
        x_list = [] 
        y_list = []

        with open(filename, "r") as filehandle:
            for line in filehandle:
                # delimiter is apperantly a '|'
                data = line.split('|')
                # well, it's actual data and not a header
                if len(data) > 1:
                    # let's filter empty elements and newlines from the list
                    data = [element for element in data if len(element) > 1 and element != '\n']

                    # get the rates
                    if data[0].strip().startswith("rate"):
                        x_list = [float(rates.split("=")[1]) for rates in data]
                    # get the values
                    else:
                        y_list = [float(packets) for packets in data]

        return (x_list, y_list)

    def read_breakdown_packets(self, filename):
        rates = [] 
        failed = []
        success = []

        with open(filename, "r") as filehandle:
            for line in filehandle:
                # delimiter is apperantly a '|'
                data = line.split('|')
                # well, it's actual data and not a header
                if len(data) > 1:
                    # let's filter empty elements and newlines from the list
                    data = [element for element in data if len(element) > 1 and element != '\n']
                    # get the rates
                    if data[0].strip().startswith("rate"):
                       rates.append(float(data[0].split("=")[1]))
                       failed.append(float(data[1]))
                       success.append(float(data[2]))

        return (rates, failed, success)

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
        figure = plt.figure()
        bar_widths = -1

        if bar_widths > 0:
            plt.bar(xdata, ydata, bar_widths)
        else:
            plt.bar(xdata, ydata[1], color="#990000")
            plt.bar(xdata, ydata[0], color="#003366")

        plt.ylabel(ylabel,va="center",ha="center")
        plt.xlabel(xlabel)
        plt.title(title)
        plt.legend( (ydata[0], ydata[1]), (labels[0], labels[1]) )


        plt.grid(axis="y")
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
    #results = parser.read("latency.txt")
    #parser.prepare_line_plot("latency.png", "Application Level Latency", "offset", "latency [ms]", results)

    results = parser.read_received_packets("packets.txt")
    parser.generate_line_plot("packets_received.png", "Packets Received Per Node", [results[0]], [results[1]], "rate", "packets", ['test'])

    results = parser.read_received_packets("reception_rate.txt")
    parser.generate_line_plot("packets_reception_rate.png", "Packet Reception Rate", [results[0]], [results[1]], "rate", "packet reception rate", ['test'])
    
    results = parser.read_breakdown_packets("breakdown.txt")
    parser.generate_bar_plot("packets_breakdown.png", "Packet Breakdown", results[0], [results[1],results[2]], "rate", "packets", ['test','foo'])

if __name__ == "__main__":
    main()

