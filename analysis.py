#!/usr/bin/env python3

import re
import subprocess

class LibAraLogFileParser:
  def __init__(self):
    self.nodes = { "ff:ff:ff:ff:ff:ff" : "broadcast" }
    self.binary = '/usr/local/bin/node'

  def transform(self, filename):
    pattern = '([a-fA-F0-9]{2}[:]?){6}'
    regular_expression = re.compile(pattern)

    with open(filename, "r") as file:
      with open(filename + '_analysis', "w") as output: 
        for line in file:
          match = regular_expression.finditer(line)

          if match:
            for mac in match:
              hostname = self._get_node(line[mac.start() : mac.end()])
              print(hostname)
#              line = line.replace(line[mac.start() : mac.end()], hostname, 1)
      #      print(line[mac.start() : mac.end()])

          output.write(line)

  def _get_node(self, mac):
    if mac not in self.nodes:
      hostname = self._query_mac(mac)

      if hostname == '':
        # the mac address belongs (maybe) to an tap interface
        temp_mac = mac.replace(mac[0:2],"50",1)
        hostname = self._query_mac(temp_mac)

        # check if again no hostname was found
        if hostname == '':
          print("unknown mac address: " + mac)
          # we simply store the mac address as hostname
          hostname = mac
      
      self.nodes[mac] = hostname.strip('\n')
     
    return self.nodes[mac]

  def _query_mac(self, mac):
      pipe = subprocess.Popen([self.binary, 'list', '-m', mac], stdout=subprocess.PIPE,
          stderr=subprocess.PIPE) 
      #return pipe.communicate()[0].strip('\n')
      return pipe.communicate()[0].decode('utf-8')

def main():
  parser = LibAraLogFileParser()
  parser.transform("/home/mfrey/testbed/experiments/log/grid10x10_a0.log")

if __name__ == "__main__":
  main()

