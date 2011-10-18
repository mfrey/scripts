#!/usr/bin/env ruby1.8

require "gnuplot"

class Coordinate
  attr_accessor :x, :y, :z, :name

  def initialize(x, y, z, name)
    @x = x
    @y = y
    @z = z
  end
end

class Placement
  attr_accessor :coordinates

  def initialize(filename)
    begin 
      file = File.new(filename, "r")
      
      @coordinates = Array.new

      while(line = file.gets)
        split = line.split(" ")
        
        if split.size == 4
          @coordinates.push(Coordinate.new(split[1], split[2], split[3], split[4]))
        end
      end

      file.close
    rescue => error    
      puts "Exception: #{error}"
      error
    end
  end

end

placement = Placement.new("placementfile.plm")
#placement.coordinates.each { |x| puts x.x.to_s + " " + x.y.to_s + " " + x.z.to_s } 

Gnuplot.open do |gp|
  Gnuplot::Plot.new(gp) do |plot|
  
    plot.title  "Placement"
    plot.ylabel "y"
    plot.xlabel "x"
    plot.set    "border linewidth 1.5"
    plot.set    "pointsize 1.5"
    plot.set    "style line 1 lc rgb '#0060ad' pt 7"

    x = Array.new
    y = Array.new
    z = Array.new

    placement.coordinates.each { |coordinate| 
      x.push(coordinate.x.to_f) 
      y.push(coordinate.y.to_f) 
      z.push(coordinate.z.to_f) 
    } 

    plot.data << Gnuplot::DataSet.new( [x, y, z] ) do |ds|
      ds.with = "p ls 1"
    end
  end
end


