#!/usr/bin/env python
import re

# 2007-04-01 11:20
find_time = re.compile(
   "(?P<year>\d{4})"  # 4 digit year
   "-"
   "(?P<month>\d{2})"  # 2 digit month
   "-"
   "(?P<day>\d{2})"  # 2 digit day
   "\s+"        # white space(s)
   "(?P<hour>\d{2})"  # 2 digit hour
   ":"
   "(?P<minute>\d{2})"  # 2 digit minute
   ).search

match = find_time("The exact time is 2007-04-01  11:20.")
assert match, "can't find time"
print "MONTH: %s" % match.group("month")
