#!/usr/bin/env python
'''Where where am I? (data from Google calendar)

Get gdata from http://code.google.com/p/gdata-python-client/
'''

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

import gdata.calendar.service as cal_service
from time import localtime, strptime, strftime, mktime, timezone

DAY = 24 * 60 * 60

def caltime_to_local(caltime):
    # 2008-11-07T23:30:00.000+02:00
    t = mktime(strptime(caltime[:16], "%Y-%m-%dT%H:%M"))
    tz_h, tz_m = map(int, caltime[-5:].split(":"))
    cal_tz = (tz_h * 60 * 60) + (tz_m * 60)
    if caltime[-6] == "-":
        cal_tz = -cal_tz

    # See timezone documentation, the sign is reversed
    diff = -timezone - cal_tz 

    return localtime(t + diff)

def iter_meetings():
    client = cal_service.CalendarService()
    client.email = "your-google-user-name"
    client.password = "your-google-password"
    client.source = "Where-is-Miki"
    client.ProgrammaticLogin()

    query = cal_service.CalendarEventQuery("default", "private", "full")
    query.start_min = strftime("%Y-%m-%d")
    tomorrow = localtime(mktime(localtime()) + DAY)
    query.start_max = strftime("%Y-%m-%d", tomorrow)
    feed = client.CalendarQuery(query)
    for event in feed.entry:
        title = event.title.text
        when = event.when[0]
        start = caltime_to_local(when.start_time)
        end = caltime_to_local(when.end_time)

        yield title, start, end

def find_meeting(meetings, now):
    for title, start, end in meetings:
        print title, start, end
        if start <= now <= end:
            return title, end

    return None, None

def meetings_html(meetings):
    if not meetings:
        return "No meetings today"

    trs = []
    tr = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
    for title, start, end in meetings:
        start = strftime("%H:%M", start)
        end = strftime("%H:%M", end)
        trs.append(tr % (title, start, end))

    return "Today's meetings: <table border='1'>" + \
           "<tr><th>Title</th><th>Start</th><th>End</th></tr>" + \
            "\n".join(trs) + \
            "</table>"

HTML = '''
<html>
    <head>
        <title>Where is Miki?</title>
        <style>
            body, td, th {
                font-family: Monospace;
                font-size: 22px;
            }
        </style>
    </head>
    <body>
        <h1>Where is Miki?</h1>
        <p>
            Seems that he is <b>%s</b>.
        </p>
        <p>
            %s
        </p>
    </body>
</html>
'''

if __name__ == "__main__":
    import cgitb; cgitb.enable()
    from operator import itemgetter

    days = ["Mon","Tue","Wed", "Thu", "Fri", "Sat", "Sun"]
    now = localtime()

    day = days[now.tm_wday]
    meetings = sorted(iter_meetings(), key=itemgetter(-1))

    # Yeah, yeah - I get in early
    if (now.tm_hour < 6) or (now.tm_hour > 17):
        where = "at home"
    elif day in ["Sat", "Sun"]:
        where = "at home"
    else:
        title, end = find_meeting(now, meetings)
        if end:
            where = "meeting %s (until %s)" % (title, strftime("%H:%M", end))
        else:
            where = "at work"

    print "Content-Type: text/html\n"
    print HTML % (where, meetings_html(meetings))
