# Current date in default format
$ date
Sun Dec  7 16:56:26 IST 2014

# Current date in ISO-8601 format (with seconds)
$ date -Isec
2014-12-07T16:57:21+0200

# Current date in UTC
$ date -u
Sun Dec  7 14:58:36 UTC 2014

# Current date in custom format, see "date --help" for format options
$ date +%Y-%m-%d
2014-12-07

# Current date as epoch
$ date +%s
1417964341

# Date math
$ date --date='-2 days'
Fri Dec  5 16:59:37 IST 2014
$ date --date='2 days ago'
Fri Dec  5 17:00:08 IST 2014

# Combination of math and format
$ date --date='2 days ago' +%Y%m%d
20141205
