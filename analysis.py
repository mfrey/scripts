#!/usr/bin/env python3

import re

class LibAraLogFileParser:
  def __init__(self):
    print("hello world")
    self.nodes = {}

  def read(self, filename):
    pattern = '([a-fA-F0-9]{2}[:]?){6}'
    regular_expression = re.compile(pattern)

    with open(filename, "r") as file:
      for line in file:
        match = regular_expression.finditer(line)

        if match:
          for mac in match:
            print(line[mac.start() : mac.end()])

def main():
  parser = LibAraLogFileParser()
  parser.read("/home/mfrey/testbed/experiments/log/grid10x10_a0.log")

if __name__ == "__main__":
  main()

