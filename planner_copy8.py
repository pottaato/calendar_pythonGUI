#!/usr/bin/python3
import mariadb
import sys
import cgi
import cgitb
import time
import datetime
import calendar
import re

print("Content-type: text/html\r\n\r\n")
cgitb.enable()
c = cgi.FieldStorage()

try:
    conn=mariadb.connect(
            user="tata",
            password="tata",
            host="localhost",
            port=3306,
            database="planner")
except mariadb.Error as e:
    print("Error: {e}")
    sys.exit()

cur = conn.cursor()

sub = c.getvalue("sub")
alter = c.getvalue("alter")
print(alter)
year = c.getvalue("year") if c.getvalue("year") else datetime.datetime.now().strftime("%Y")
month = c.getvalue("month") if c.getvalue("month") else datetime.datetime.now().strftime("%m")
day = c.getvalue("date") if c.getvalue("date") else datetime.datetime.now().strftime("%d")
hour = c.getvalue("hour") if c.getvalue("hour") else datetime.datetime.now().strftime("%H")
min = c.getvalue("min") if c.getvalue("min") else datetime.datetime.now().strftime("%M")
txt = c.getvalue("txt") if c.getvalue("txt") else ""
content = c.getvalue("content") if c.getvalue("content") else ""

view_date = c.getvalue("view_date")
view_hour = c.getvalue("view_hour")
view_min = c.getvalue("view_min")

n = c.getvalue("next") if c.getvalue("next") else "next"
if n != "next":
    month = int(month) + 1
p = c.getvalue("prev") if c.getvalue("prev") else "prev"
if p != "prev":
    month = int(month) - 1

if month == 0:
    year = int(year) - 1
    month = 12
elif month == 13:
    year = int(year) + 1
    month = 1

name_month = calendar.month_name[int(month)]

date = "1/{}/{}".format(month, year)
sec = int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))
convert = time.localtime(sec)
week = int(time.strftime("%w", convert))

if sub is not None:
    if sub == "ADD":
        try:
            cur.execute("INSERT schedule2 (year, month, date, hour, min, content) VALUES(?, ?, ?, ?, ?, ?)", (year, month, day, hour, min, content))
            conn.commit()
            print("<p align=center style='color:#0b4d8'><b>Added to planner</b></p>")
        except:
            print("<p align=center style='color:#c74b50'><b>Error occured</b></p>")
    else:
        if sub == "DEL":
            try:
                cur.execute("DELETE FROM schedule2 WHERE eid={}".format(alter))
                conn.commit()
                print("<p align=center style='color:#0b4d8'><b>Removed from planner</b></p>")
                alter = None
            except:
                print("<p align=center style='color:#c74b50'><b>Error occured</b></p>")

select_day = "<select name=date><option value={}>{}</option>".format(day, day)
for i in range(sec, (sec+86400*32), 86400):
    x = time.localtime(i)
    d = int(time.strftime("%d",x))
    m = int(time.strftime("%m",x))
    if m != int(month): break
    select_day += ("<option value={}>{:02d}</option>".format(d, d))
select_day += "</select>"

select_hour = "<select name=hour><option value={}>{}</option>".format(hour, hour)
for i in range(24):
    select_hour += "<option value={}>{:02d}</option>".format(i, i)
select_hour += "</select>"

select_min = "<select name=min><option value={}>{}</option>".format(min, min)
for i in range(60):
    select_min += "<option value={}>{:02d}</option>".format(i, i)
select_min += "</select>"

header = """
<input type=hidden value="{}" name=year>
<input type=hidden value="{}" name=month>
<div class="center">
<input type=submit value="Previous Month" name="prev" align="left">
<label style="font-weight:1000;">{} {}</label>
<input type=submit value="Next Month" name="next" align="right">
<br><br>
""".format(year, month, name_month, year)

if alter is None:
    alter_html = ("""
        {} / {} h : {} m
        <input type=text name=content>
        <input type=submit name=sub value="ADD">
        """.format(select_day, select_hour, select_min))
else:
    cur.execute("SELECT * FROM schedule2 WHERE eid={}".format(alter))
    for i in (cur.fetchall()):
        choosen_date = i[3]
        choosen_hour = i[4]
        choosen_min = i[5]
        choosen_content = i[6]
    alter_html = ("""
        {} / {} h : {} m
        <input type=text name=content value="{}">
        <input type=submit name=sub value="EDIT">
        <input type=submit name=sub value="DEL">
        <input type=button value="BACK" onClick="back();">
        <input type=hidden name=alter value={}>
        <input type=hidden name=view_date value={}>
        <input type=hidden name=view_hour value={}>
        <input type=hidden name=view_min value={}>
        """.format(select_day, select_hour, select_min, choosen_content, alter, choosen_date, choosen_hour, choosen_min))

def calendar():
    
    print("""
    <table style='width:100%; height:50%;'>
    <tr style='background-color:#5b7db1; height:20px' align=center>
    <td><p style='color:white'>SUN</p></td>
    <td><p style='color:white'>MON</p></td>
    <td><p style='color:white'>TUE</p></td>
    <td><p style='color:white'>WED</p></td>
    <td><p style='color:white'>THU</p></td>
    <td><p style='color:white'>FRI</p></td>
    <td><p style='color:white'>SAT</p></td>
    """)
    
    convert = time.localtime(sec)
    week = int(time.strftime("%w", convert))
    cnt = 1
    for i in range((sec-86400*week), (sec+86400*(35-week)), 86400):
        x = time.localtime(i)
        y = int(time.strftime("%Y", x))
        m = int(time.strftime("%m", x))
        d = int(time.strftime("%d", x))
        
        db = "SELECT * FROM schedule2 WHERE year={} AND month={} AND date={}".format(y, m, d)
        cur.execute(db)
        if cnt%7 == 1:
            print("<tr align='left' valign='top'>")

        if m == int(month):
            print("<td style='background-color:#c3e5ae; height:100px; width:50px'>{}".format(d))
            for i in (cur.fetchall()):
                print("<br><div onClick='alter({});'>{}:{}|{}</div>".format(i[0],i[4],i[5],i[6]))
            print("</td>")
        else:
            print("<td style='background-color:#97dbae; height:100px; width:50px'>{}".format(d))
            for i in (cur.fetchall()):
                print("<br><div onClick='alter({});'>{}:{}|{}</div>".format(i[0],i[4],i[5],i[6]))
            print("</td>")
        
        if cnt%7 == 0:
            print("</tr>")

        cnt += 1
    
    print("</table><br>")

print("""
        <html>
        <head>
        <style>
        table, th, td {border: 1px solid black;}
        .center{text-align:center;}
        </style></head>
        
        <script language='javascript'>
            function alter(eid) {location.href = 'planner_copy8.py?alter=' + eid;}
            function back() {location.href = 'planner_copy8.py';}
        </script>
        <body>
        <form action='/cgi-bin/planner_copy8.py' method='GET'>""")

print(header)
print(alter_html)
calendar()

print("""
        </form></body>
        </html>""")





