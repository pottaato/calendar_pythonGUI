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
hour = c.getvalue("hour") if c.getvalue("hour") else int(datetime.datetime.now().strftime("%H"))
min = c.getvalue("min") if c.getvalue("min") else int(datetime.datetime.now().strftime("%M"))
n = c.getvalue("next")
p = c.getvalue("prev")
content = c.getvalue("content")
sub = c.getvalue("sub")
action = c.getvalue("action")

date = "{:02d}{}{}".format(int(day),month, year)
sec = int(time.mktime(datetime.datetime.strptime(date,"%d%m%Y").timetuple()))

if sub == "ADD":
    try:
        cur.execute("INSERT schedule2 (year, month, date, hour, min, content) VALUES(?, ?, ?, ?, ?, ?)",(year, month, day, hour, min, content))
        conn.commit()
        print("added")
        action == None
    except:
        print("add error")

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

#print(year, month, day)
name_month = calendar.month_name[int(month)]
next_month = int(month)+1
if next_month == 13:
    next_month = 1
name_next_month = calendar.month_name[next_month]

next_month = 0
next_year = 0
convert = time.localtime(sec)
week = int(time.strftime("%w", convert))
dates = "<td>h</td>"
l_dates = []
for i in range(sec-86400*week, sec+86400*(7-week), 86400):
    #print(i)
    x = time.localtime(i)
    d = time.strftime("%d", x)
    m = time.strftime("%m", x)
    y = time.strftime("%Y", x)
    dates += "<td align=center>{}</td>".format(d)
    l_dates.append(d)
    if int(m) != int(month):
        next_month = 1
    if int(y) != int(year):
        next_month = 1
        next_year = 1

#print(year, month, day)
#print(next_month, next_year)
header = """
<div align=center>
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
header += """<input type=submit name=next value=">>"></div>"""

#print(year, month, day)
row_days= """
<tr style='background-color:#5b7db1; height:10px' align=center>
<td style='background-color:white'></td>
<td><p style='color:white'>SUN</p></td>
<td><p style='color:white'>MON</p></td>
<td><p style='color:white'>TUE</p></td>
<td><p style='color:white'>WED</p></td>
<td><p style='color:white'>THU</p></td>
<td><p style='color:white'>FRI</p></td>
<td><p style='color:white'>SAT</p></td>
</tr>"""

print("""
        <html>
        <head><style>
        .div_content {
            background-color: lightblue;
            text-align: center;
        }
        </style></head>
        <script language='javascript'>
            function show_add(year, month, date, hour) {
                location.href='planner_weekly1.py?action=show_add&year='+year+'&month='+month+'&day='+date+'&hour='+hour;}
            function back() {location.href='planner_weekly1.py'}
        </script>
        <body><table style='width:100%; height:50%;'>
        <form action='/cgi-bin/planner_weekly1.py' method=GET>
""")
print(header)
print(row_days)
print(dates)

for i in range(24):
    print("<tr><td>{:02d}</td>".format(i), end="")
    for j in l_dates:
        cur.execute("SELECT COUNT(*) FROM schedule2 WHERE year={} AND month={} AND date={}".format(year, month, j))
        count = cur.fetchone()
        #print(count[0])
        if count[0] > 0:
            print("<td width='15%' onclick='show_add({},{},{},{});' style='background-color:#d6e5fa;'>".format(year, month, j, i))
            cur.execute("SELECT * FROM schedule2 WHERE year={} AND month={} AND date={}".format(year, month, j))
            for k in cur.fetchall():
                db_day = int(k[3])
                db_hour = int(k[4])
                content = k[6]
                #print(year, month, j)
                #print(j, db_day, i, db_hour)
                if int(j) == db_day and i == db_hour:
                    #print("ok")
                    print("<div class='div_content' style='padding=0px;'>{}</div>".format(content))
                    print("<div style='padding=1px;'></div>")
                else:
                    print("<div></div>")
        else:
            print("<td width='15%' onclick='show_add({},{},{},{});' style='background-color:#d6e5fa;'<div></div>".format(year, month, j, i))
        print("</td>", end="")
    print("</tr>")
print("</table>")

select_min = "<select name=min><option value={:02d}>{:02d}</option>".format(int(min), int(min))
for i in range(60):
    select_min += "<option value={:02d}>{:02d}</option>".format(i, i)
select_min += "</select>"


print("<br><br>")
if action == "show_add":
    #print(year, month, day, hour)
    print("""
    <input type=hidden name=hour value={}>
    {} d / {:02d} h : {} m <br><br>
    <input type=text name=content><br><br>
    <input type=submit name=sub value="ADD">
    <input type=button value="BACK" onclick="back();">
    """.format(hour, day, int(hour), select_min))

print("</body></html>")
