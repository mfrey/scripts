#!/usr/bin/env python

import os
import sys
import argparse

class Node:
  def __init__(self):    
    self.name = "";
    self.wlanInterface = ""
    self.tapInterface = ""


class PacketTraceParser:
  def __init__(self):    
    self.nodes = {}

  def readAddressFiles(self,directory):
    for root, subFolders, files in os.walk(directory):
      for file in files:
        addressFile = open(directory + "/" + file, "r")
        if addressFile.endswith('address')
          node = Node()
          node.name = addressFile.readline()
          node.wlanInterface = addressFile.readline()
          node.tapInterface = addressFile.readline()
          # add node to the hash map
          self.nodes[node.name] = node

  def readLogFiles(self,directory):
    for root, subFolders, files in os.walk(directory):
      for file in files:
        logFile = open(directory + "/" + file, "r")
        if logFile.endswith('log')



t = PacketTraceParser()
t.readAddressFiles("test")

#parser = argparse.ArgumentParser(description='analyze ARA packet traces')
#parser.add_argument('string', metavar='A', type=string, nargs='+', help='the location of the address files')
#parser.add_argument('string', metavar='L', type=string, nargs='+', help='the location of the log files')

