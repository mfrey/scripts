#!/usr/bin/env python

import os
import re
import sys
import argparse

from collections import deque

class Node:
  def __init__(self):    
    self.name = ""
    self.wlanInterface = ""
    self.tapInterface = ""

  def __str__(self):
    return "name: "+ self.name +" wlan0: "+ self.wlanInterface +" tap0: " + self.tapInterface;

class Packet:
  def __init__(self, source, destination, sequenceNumber):    
    self.source = source
    self.destination = destination
    self.sequenceNumber = sequenceNumber

  def __str__(self):
    return "source: "+ self.source + " destination: "+ self.destination + " sequence number: " + self.sequenceNumber;
  
  def __eq__(self,other):
    if(isinstance(other,Packet)):
      return ((other.sequenceNumber == self.sequenceNumber) and (other.source.name == self.source.name) and (other.destination.name == self.destination.name))
    else:
      return false;

#class PacketTrace:
#  def __init__(self):    
#    self.path = deque()

class PacketTraceParser:
  def __init__(self):    
    self.nodes = {}
    self.tap = {}
    self.wlan = {}
    self.paths = {}

  def readAddressFiles(self,directory):
    for root, subFolders, files in os.walk(directory):
      for file in files:
        if file.endswith('address'):
          print file
          addressFile = open(directory + "/" + file, "r")
          node = Node()
          node.name = addressFile.readline()
          node.wlanInterface = addressFile.readline()
          node.tapInterface = addressFile.readline()
          # add node to the node hash map
          self.nodes[node.name] = node
          # add node to the tap hash map
          self.tap[node.tapInterface] = node
          # add node to the wlan hash map
          self.wlan[node.wlanInterface] = node
          # close the file
          adressFile.close()

  def readLogFiles(self,directory):
    for root, subFolders, files in os.walk(directory):
      for file in files:
        if file.endswith('log'):
          logFile = open(directory + "/" + file, "r")
          try: 
            for line in logFile:
              if line == "Beginning full info dump.\n":
                currentLine = logFile.next();
                if "data" in currentLine:
                  # determine the sequence number of the data packet, the 
                  # return type is a array (where the second entry should contain the number)
                  sequenceNumber = (re.split("\\D+", currentLine))[1];
                  # todo: check (skip the ethernet line)
                  logFile.next();
                  # at the processing buffer
                  currentLine = logFile.next();
                  # clean up the mess
                  currentLine = re.sub("\\.|p.=|\\t", "", currentLine);
                  # get the addresses
                  addresses = currentLine.split(" ");
                  # get the destination address
                  destination = (addresses[0])[9:]
                  # get the source address
                  source = (addresses[1])[9:]
                  try:
                    # get the corresponding source node 
                    sourceNode = self.tap[source];
                    # get the corresponding destination node 
                    destinationNode = self.tap[destination]; 
                    # create a packet
                    packet = Packet(sourceNode, destinationNode, sequenceNumber)

                    # get the next line
                    currentLine = logFile.next();
                    # current line should now the previous and next hop line
                    currentLine = re.sub("\\.|.h=|\\t", "", currentLine);
                    # get the hops
                    hops = currentLine.split(" ");

                    # check if there is already an entry
                    if packet not in self.paths:
                      # add an empty deque to the yet to setup path list
                      self.paths[packet] = deque();
                    
                    # access the path list
                    path = self.paths[packet]
                    # get the next node
                    nextNode = self.wlan[(hops[0])[9:]]
                    # get the previous node
                    previousNode = self.wlan[(hops[1])[9:]]
 
                    # we have to check if the previous and/or next hop are already in the path list
                          
                  except KeyError:
                    # todo: think about a better exception handling
                    print "oops"
              elif "Packet arrived" in line:
                print "todo"
            logFile.close()
          except StopIteration:
            # todo: think about a smarter exception handling
            print "oops"


t = PacketTraceParser()
#t.readAddressFiles("demo")
#t.readLogFiles("test")
t.readLogFiles("test2")

#parser = argparse.ArgumentParser(description='analyze ARA packet traces')
#parser.add_argument('string', metavar='A', type=string, nargs='+', help='the location of the address files')
#parser.add_argument('string', metavar='L', type=string, nargs='+', help='the location of the log files')

