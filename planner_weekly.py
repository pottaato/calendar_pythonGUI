#!/usr/bin/python3
import mariadb
import cgi
import cgitb
import sys
import time
import datetime
import calendar

print("Content-type:text/html\r\n\r\n")
cgitb.enable()
c = cgi.FieldStorage()

try:
    conn=mariadb.connect(
            user="tata",
            password="tata",
            host="localhost",
            port=3306,
            database="planner"
            )

except mariadb.Error as e:
    print("Error: {}".format(e))
    sys.exit()

cur = conn.cursor()

year = c.getvalue("year") if c.getvalue("year") else datetime.datetime.now().strftime("%Y")
month = c.getvalue("month") if c.getvalue("month") else datetime.datetime.now().strftime("%m")
day = c.getvalue("day") if c.getvalue("day") else int(datetime.datetime.now().strftime("%d"))
n = c.getvalue("next")
p = c.getvalue("prev")


date = "{:02d}{}{}".format(int(day),month, year)
sec = int(time.mktime(datetime.datetime.strptime(date,"%d%m%Y").timetuple()))

#convert = time.localtime(sec)
if n == ">>":
    sec = sec+86400*7
    convert = time.localtime(sec)
    year = int(time.strftime("%Y", convert))
    month = int(time.strftime("%m", convert))
    day = int(time.strftime("%d", convert))
elif p == "<<":
    sec = sec-86400*7
    convert = time.localtime(sec)
    year = int(time.strftime("%Y", convert))
    month = int(time.strftime("%m", convert))
    day = int(time.strftime("%d", convert))

name_month = calendar.month_name[int(month)]
next_month = int(month)+1
if next_month == 13:
    next_month = 1
name_next_month = calendar.month_name[next_month]

next_month = 0
next_year = 0
convert = time.localtime(sec)
week = int(time.strftime("%w", convert))
#print(sec, week)
dates = "<td></td>"
l_dates = []
for i in range(sec-86400*week, sec+86400*(7-week), 86400):
    print(i)
    x = time.localtime(i)
    d = time.strftime("%d", x)
    m = time.strftime("%m", x)
    y = time.strftime("%Y", x)
    dates += "<td align=center>{}</td>".format(int(d))
    l_dates.append(d)
    if int(m) != int(month):
        next_month = 1
    if int(y) != int(year):
        next_month = 1
        next_year = 1

print(l_dates)
#print(next_month, next_year)
header = """
<header><div align=center>
<input type=hidden name=year value={}>
<input type=hidden name=month value={}>
<input type=hidden name=day value={}>
<input type=submit name=prev value="<<">""".format(year, month, day)
if next_month == 0 and next_year == 0:
    header += "<label style='font-weight:1000;'>{} of {}</label>".format(name_month, year)
elif next_month == 1 and next_year == 0:
    header += "<label style='font-weight:1000;'>{}-{} of {}</label>".format(name_month, name_next_month, year)
elif next_month == 1 and next_year == 1:
    header += "<label style='font-weight:1000;'>{}-{} of {}-{}</label>".format(name_month, name_next_month, year, int(year)+1)
header += """<input type=submit name=next value=">>"></div></header>"""

#print(year, month, day)
days= """
<tr style='background-color:#5b7db1; height:10px' align=center>
<td></td>
<td><p style='color:white'>SUN</p></td>
<td><p style='color:white'>MON</p></td>
<td><p style='color:white'>TUE</p></td>
<td><p style='color:white'>WED</p></td>
<td><p style='color:white'>THU</p></td>
<td><p style='color:white'>FRI</p></td>
<td><p style='color:white'>SAT</p></td>
</tr>"""

print("""
<html><body><table style='width:100%; height:50%;'>
<form action='/cgi-bin/planner_weekly.py' method=GET>
""")

print(header)
#print(next_month)
print(days)
print(dates)
#print("<table>")
#print(month, year)
for i in l_dates:
    dt = "{:02d}{:02d}{}".format(int(i), int(month), year)
    sec = int(time.mktime(datetime.datetime.strptime(dt, "%d%m%Y").timetuple()))
    convert= time.localtime(sec)
    week = int(time.strftime("%w", convert))
    for j in range(24):
        print("<tr><td>{:02d}</td>".format(j), end="")
        print("j={}".format(j))
        print(i,week)
        for k in range(7):
            print("<td>")
    cur.execute("SELECT * FROM schedule2 WHERE year={} AND month={} AND date={}".format(year, month, i))
    for m in cur.fetchall():
        if j == int(m[4]) and k == week:
                    print("<td><p align=center>{}</p></td>".format(m[6]), end="")
                else:
                    print("<td><p align=center>---</p></td>", end="")
            print("k={}".format(k))


#day = -1
#for i in range(24):
#    print("<tr><td>{:02d}</td>".format(i), end="")
#    for j in range(7):
#        print("<td><p>____________</p></td>", end="")
#        day += 1
#        print(day)
#    print("<tr>")


print("</table></body></html>")
