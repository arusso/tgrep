#!/usr/bin/python2.6

#=#=#=#=#=#=#
# @author: Aaron Russo (aaron.n.russo@gmail.com)
# @date:   20-Feb-2011
# @purpose: To quickly parse log files, printing out relevant lines based on 
#           search input
# @notes:  written for submission to reddit.com job challenge
#=#=#=#=#=#=#


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
# IMPORT VALUES
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
import sys
import os
import re
import os.path
import io

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
# CONSTANT VALUES
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
_TIME_TYPE_SPECIFIC=1
_TIME_TYPE_RANGE=2    # a range can be specified like
                      # 10:24 or 10:24:01-10:24:59
_TIME_TYPE_ERROR=-1

_PATTERN_24HOURS='([0-1]?[0-9]|[2][0-3])'
_PATTERN_60MINS='([0-5][0-9])'
_PATTERN_60SECS='([0-5][0-9])' 
_PATTERN_FULLTIME=_PATTERN_24HOURS+":"+_PATTERN_60MINS+":"+_PATTERN_60SECS

_FIRST_ENTRY = 0
_LAST_ENTRY = 1

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
# DEFAULT VALUES
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
_input_file='/logs/haproxy.log'
_file_len=0
_debug=0

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
# main() function - primary entry point for application
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def main():
  global _input_file,_file_len
  _search_type=-1

  ######## Parse Arguments
  if len(sys.argv) < 2 or len(sys.argv) > 3:  # arg counts
    usage()
    exit()

  for arg in sys.argv[1:3]:
    debug( "parsing: '"+arg+"'",0)
    results=getTimeType(arg)  # (time type, (hour,min,sec[,hour,min,sec]))

    if results[0]!=_TIME_TYPE_ERROR:
      _search_type=results[0]
      _search_params=results[1]
    else:
      debug("checking validity of filename",1)
      # is this the input file?
      if os.path.isfile(arg):  # yes!
        _input_file=arg
        debug("logfile: "+_input_file)
      else:                    # no!
        print "bad input: '"+arg+"'"      
        exit()

  ######## Begin Searching Through File
    f = open(_input_file,mode='rt')
  try:
    _file_len = f.seek(0,2).tell()  # get max size
  except:
    print "Unexpected error:", sys.exc_info()[0]

  

def getEntries(type,time):
  if time==_TIME_TYPE_SPECIFIC:
    e_start = findTime(f,buildTime(time[0],time[1],time[2],_FIRST))
    e_end   = findTime(f,buildTime(time[0],time[1],time[2],_LAST))
  elif time==TIME_TYPE_RANGE:
    e_start = findTime(f,buildTime(time[0],time[1],time[2],_FIRST))
    e_end   = findTime(f,buildTime(time[3],time[4],time[5],_LAST))

# returns the beginning of the line that we find the entry, not the entry location
# fol = first or last
def findTime(file,time,fol = _FIRST_ENTRY):
  mid = _file_len/2
  debug("char midpoint: "+str(mid))    

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
# getTimeType(input) - determines what type of search type the user wants
#   and returns the search type as well as the parameters for the search
#   in a consistent manner (ie. expands implicit time ranges)
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def getTimeType(input):
  debug("determining time type...")
  pattern_specific=_PATTERN_FULLTIME+"$"
  result = re.match(pattern_specific,input)
  if result != None:  # we found a result
    return (_TIME_TYPE_SPECIFIC,result.groups(0))
  else:
    debug("not specific time type!",1)

  # let's look for an explicit time range
  pattern_range_explicit=_PATTERN_FULLTIME+"-"+_PATTERN_FULLTIME+"$"
  result = re.match(pattern_range_explicit,input)
  if result != None:
    return (_TIME_TYPE_RANGE,result.groups(0))
  else:
    debug("not range explicit time type!",1)

  # let's look for the implicit time range
  pattern_range_implicit=_PATTERN_24HOURS+":"+_PATTERN_60MINS+"$"
  result = re.match(pattern_range_implicit,input)
  if result != None:
    # let's expand the range before returning it
    result_tpl = (result.groups(0)[0],result.groups(0)[1],'00',result.groups(0)[0],result.groups(0)[1],'59')
    return (_TIME_TYPE_RANGE,result_tpl)
  else:
    debug("not range implicit time type!",1)
  
  return (_TIME_TYPE_ERROR,result)

# quick function to build time string
def buildTime(hour,minute,second):
  return hour+":"+minute+":"+second

# quick function to build range string
def buildTimeRange(s_hour,s_min,s_sec,f_hour,f_min,f_sec):
  return buildTime(s_hour,s_min,s_sec)+"-"+buildTime(f_hour,f_min,f_sec)


def usage():
  print "usage: "+sys.argv[0]+" <time|time range> [logfile]" 





def debug(msg,lvl=0):
  global _debug
  if _debug:
    print " "*lvl+"dbg: "+msg


if __name__ == '__main__':
  main()
