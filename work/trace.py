#!/usr/bin/env python

import os
import re
import sys
import argparse

from collections import deque

import logging 

logging.basicConfig(filename='example.log',level=logging.DEBUG)

class Node:
  def __init__(self):    
    self.name = ""
    self.wlanInterface = ""
    self.tapInterface = ""

  def __str__(self):
    return "name:  "+ self.name +" wlan0: "+ self.wlanInterface +" tap0:  " + self.tapInterface;

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

  def __hash__(self):
	return hash(repr(self))

#class PacketTrace:
#  def __init__(self):    
#    self.path = deque()

class PacketTraceParser:
  def __init__(self):    
    self.nodes = {}
    self.tap = {}
    self.wlan = {}
    self.paths = {}

  def readAddressFiles(self, directory):
    for root, subFolders, files in os.walk(directory):
      for file in files:
        if file.endswith('address'):
          try:
            fullpath = os.path.join(root, file)
            addressFile = open(fullpath, "r")
            node = Node()
            node.name = addressFile.readline().rstrip("\n")
            node.wlanInterface = addressFile.readline().rstrip("\n")
            node.tapInterface = addressFile.readline().rstrip("\n")

            logging.debug("add node " + "\n " + str(node))

            # add node to the node hash map
            self.nodes[node.name] = node
            # add node to the tap hash map
            self.tap[node.tapInterface] = node
            # add node to the wlan hash map
            self.wlan[node.wlanInterface] = node
            # close the file
            addressFile.close()
          except KeyError:
			print ""

  def getSequenceNumber(self,string):
    return (re.split("\\D+", string))[1]

  def getAddresses(self,string):
    addresses = string.split(" ")
    # returns an array with two entries (first entry is the source address, second the destination address) 
    return [(addresses[1])[9:], (addresses[0])[9:]]

  def getNodesByWlanInterface(self,string):
    hops = string.rstrip("\n").split(" ")
    try:
      # return an array containing (previous hop, next hop)
      return [self.wlan[hops[0]] , self.wlan[hops[1]]]
    except KeyError:
      print "smart error handling" 
      return []
    
  def getNodesByTapInterface(self, string): 
    hops = string.rstrip("\n").split(" ")
    try:
      # return an array containing (source, destination)
      #return [self.tap[(hops[1])[9:]] , self.tap[(hops[0])[9:]]]
      return [self.tap[hops[1]] , self.tap[hops[0]]]
    except KeyError:
      print "smart error handling ", string
      return []

  def readLogFiles(self,directory):
    for root, subFolders, files in os.walk(directory):
      for file in files:
        if file.endswith('log'):
          fullpath = os.path.join(root, file)
          logFile = open(fullpath, "r")
          try: 
            for line in logFile:
              if line == "Beginning full info dump.\n":
                currentLine = logFile.next();
                if "data" in currentLine:
                  # determine the sequence number of the data packet, the 
                  # return type is a array (where the second entry should contain the number)
                  sequenceNumber = self.getSequenceNumber(currentLine)
                  # todo: check (skip the ethernet line)
                  logFile.next();
                  # at the processing buffer
                  currentLine = logFile.next()
                  # clean up the mess
                  currentLine = re.sub("\\.|p.=|\\t", "", currentLine)

                  try:
                    # get source and destination node 
                    sourceNode, destinationNode = self.getNodesByWlanInterface(currentLine)
                    # create a packet
                    packet = Packet(sourceNode, destinationNode, sequenceNumber)

                    # get the next line
                    currentLine = logFile.next();
                    # current line should now the previous and next hop line
                    currentLine = re.sub("\\.|.h=|\\t", "", currentLine);
                    # get the next and previous node
                    nextNode, previousNode = self.getNodesByTapInterface(currentLine);

                    # check if there is already an entry
                    if packet not in self.paths:
                      # add an empty deque to the yet to setup path list
                      self.paths[packet] = deque();
                    
                    # access the path list
                    path = self.paths[packet]
 
                    # we have to check if the previous and/or next hop are already in the path list
                          
                  except KeyError:
                    # todo: think about a better exception handling
                    print "oops"
              elif "Packet arrived" in line:
                sequenceNumber = self.getSequenceNumber(currentLine)
                # todo: check why we should skip a line
                currentLine = logFile.next();
                # at the processing buffer line
                currentLine = logFile.next();
                # clean up the mess
                currentLine = re.sub("\\.|p.=|\\t", "", currentLine)
                # get source and destination node 
                sourceNode, destinationNode = self.getNodesByWlanInterface(currentLine)
                # create a packet
                packet = Packet(sourceNode, destinationNode, sequenceNumber)

                # get the next and previous node
                # nextNode, previousNode = getNodesByWlanInterface(currentLine);

            logFile.close()
          except StopIteration:
            # todo: think about a smarter exception handling
            print "oops"

def main():
  parser = argparse.ArgumentParser(description='analyze ARA packet traces')
  parser.add_argument('-a', dest='address_files_location', type=str, default="", action='store', help='location of the address files')
  parser.add_argument('-l', dest='log_files_location', type=str, default="", action='store', help='location of the log files')

  results = parser.parse_args()

  log_files = results.log_files_location
  address_files = results.address_files_location

  t = PacketTraceParser()
  t.readAddressFiles(address_files)
  t.readLogFiles(log_files)

if __name__ == "__main__":
  main()

