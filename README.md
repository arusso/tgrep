_In Febuary 2011, Reddit was looking to [hire some systems
engineers](https://www.reddit.com/r/blog/comments/fjgit/reddit_is_doubling_the_size_of_its_programming/),
and asked applicants to write a tool to search through web log files in a
specific format by date/time. This was my (unsubmitted) attempt to the backend
challenge._

## Project Requirements

1. Quickly search through log files.  Example of log line (newlines added):

```
Feb 10 10:59:49 web03 haproxy[1631]: 10.350.42.161:58625 [10/Feb/2011:10:59:49.089] frontend
pool3/srv28-5020 0/138/0/19/160 200 488 - - ---- 332/332/13/0/0 0/15 {Mozilla/5.0 (Windows; U; 
Windows NT 6.1; en-US; rv:1.9.2.7) Gecko/20100713 Firefox/3.6.7|www.reddit.com|
http://www.reddit.com/r/pics/?count=75&after=t3_fiic6|201.8.487.192|17.86.820.117|}
"POST /api/vote HTTP/1.1"
```

2. By default, it looks at /logs/haproxy.log -- if an argument is specified for
  which file to open, it can be either appended or prepended to the time argument

3. Code must be leglible

## Given Assumptions
* Each line starts with a date time
* Each log contains a single 24-hour period +- a few minutes
* Timestamps are always increasing in order
* You can ignore daylight savings

## My assumptions
* Time is in 24-hour notation (as was shown in the example: "tgrep 23:59-0:03")
