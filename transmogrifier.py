#!/usr/bin/env python3.2

import re
import sys
import argparse
import subprocess

class LibAraLogFileParser:
  def __init__(self):
    self.nodes = { "ff:ff:ff:ff:ff:ff" : "broadcast" }
    self.binary = '/usr/local/bin/node'

  def transform(self, input, output):
    pattern = '([a-fA-F0-9]{2}[:]?){6}'
    regular_expression = re.compile(pattern)

    with open(input, "r") as input_file:
      with open(output, "w") as output_file: 
        for line in input_file:
          match = regular_expression.finditer(line)

          modified_line = line

          if match:
            for mac in match:
              hostname = self._get_node(line[mac.start() : mac.end()])
              # let's replace the mac addresses with the hostnames
              modified_line = modified_line.replace(line[mac.start() : mac.end()], hostname, 1)

          output_file.write(modified_line)

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
        else:
          hostname += '.[tap]'
      else:
        hostname += '.[wifi]'
      
      hostname = hostname.replace('\n', '')
      self.nodes[mac] = hostname
     
    return self.nodes[mac]

  def _query_mac(self, mac):
      pipe = subprocess.Popen([self.binary, 'list', '-m', mac], stdout=subprocess.PIPE,
          stderr=subprocess.PIPE) 
      #return pipe.communicate()[0].strip('\n')
      return pipe.communicate()[0].decode('utf-8')

def main():
  parser = argparse.ArgumentParser(description="transmogrifier - a script for transforming libARA (testbed) logs")
  parser.add_argument('-i', '--input', dest='input', type=str, default='', action='store', help='input file to be transformed')
  parser.add_argument('-o', '--output', dest='output', type=str, default='', action='store', help='output file for transformation')

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  arguments = parser.parse_args()

  log = LibAraLogFileParser()
  log.transform(arguments.input, arguments.output)

if __name__ == "__main__":
  main()

