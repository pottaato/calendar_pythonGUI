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
    print("Error: {}".format(e))
    sys.exit()

cur = conn.cursor()

sub = c.getvalue("sub")
action = c.getvalue("action")
year = c.getvalue("year") if c.getvalue("year") else datetime.datetime.now().strftime("%Y")
month = c.getvalue("month") if c.getvalue("month") else datetime.datetime.now().strftime("%m")
day = c.getvalue("day") if c.getvalue("day") else int(datetime.datetime.now().strftime("%d"))
hour = c.getvalue("hour") if c.getvalue("hour") else int(datetime.datetime.now().strftime("%H"))
min = c.getvalue("min") if c.getvalue("min") else int(datetime.datetime.now().strftime("%M"))
eid = c.getvalue("eid") if c.getvalue("eid") else ""
content = c.getvalue("content") if c.getvalue("content") else ""
calendar_change = c.getvalue("calendar")

n = c.getvalue("next") if c.getvalue("next") else "next"
p = c.getvalue("prev") if c.getvalue("prev") else "prev"

if n != "next":
    month = int(month)+1
    action = None
if p != "prev":
    month = int(month)-1
    action = None
if month == 0:
    year = int(year)-1
    month = 12
if month == 13:
    year = int(year)+1
    month = 1

date = "01{}{}".format(month, year)
sec = int(time.mktime(datetime.datetime.strptime(date, "%d%m%Y").timetuple()))
name_month = calendar.month_name[int(month)]

if sub is not None:
    if sub == "ADD":
        try:
            cur.execute("INSERT schedule2 (year, month, date, hour, min, content) VALUES(?, ?, ?, ?, ?, ?)",(year, month, day, hour, min, content))
            conn.commit()
            print("<p>added</p>")
            action == None
        except:
            print("<p>add error</p>")
    else:
        if sub == "DEL":
            try:
                cur.execute("DELETE FROM schedule2 WHERE eid={}".format(eid))
                conn.commit()
                print("<p>deleted</p>")
                action = None
            except:
                print("<p>del error</p>")

        elif sub == "EDIT":
            try:
                cur.execute("UPDATE schedule2 SET date='{}', hour='{}', min='{}', content='{}' WHERE eid={}".format(day, hour, min, content, eid))
                conn.commit()
                print("<p>edited</p>")
                action = None
            except:
                print("<p>edt error</p>")

header = """
<input type=hidden name=year value={}>
<input type=hidden name=month value={}>
<input type=hidden name=action value={}> 
<div class="center">
<input type=submit value="<<" name=prev>
<label style="font-weight:1000;">{} of {}</label>
<input type=submit value=">>" name=next align=left>
<input type=submit name=calendar_change value="yearly" align=left>
<input type=submit name=calendar_change value="monthly" align=left>
""".format(year, month, action, name_month, year, year, month, day)
#print(year,month,day)
if action == "show_add":
    select_hour = "<select name=hour><option value={:02d}>{:02d}</option>".format(int(hour),int(hour))
    for i in range(24):
        select_hour+="<option value={:02d}>{:02d}</option>".format(i,i)
    select_hour+="</select>"

    select_min = "<select name=min><option value={:02d}>{:02d}</option>".format(int(min),int(min))
    for i in range(60):
        select_min+="<option value={:02d}>{:02d}</option>".format(i,i)
    select_min+="</select>"

    action_html="""
    {} h : {} m <br><br>
    <input type=text name=content><br><br>
    <input type=submit name=sub value="ADD">
    <input type=button value="BACK" onclick="back();">
    <input type=hidden name=day value={}>
    """.format(select_hour, select_min, day)

elif action == "show_edit":
    cur.execute("SELECT * FROM schedule2 WHERE eid={}".format(eid))
    for i in cur.fetchall():
        year = int(i[1])
        month = int(i[2])
        day = int(i[3])
        db_hour = int(i[4])
        db_min = int(i[5])
        db_cont = i[6]
    select_hour = "<select name=hour><option value={:02d}>{:02d}</option>".format(db_hour, db_hour)
    for i in range(24):
        select_hour += "<option value={:02d}>{:02d}</option>".format(i, i)
    select_hour += "</select>"
        
    select_min = "<select name=min><option value={:02d}>{:02d}</option>".format(db_min, db_min)
    for i in range(60):
        select_min += "<option value={:02d}>{:02d}</option>".format(i, i)
    select_min += "</select>"
    action_html="""
    {} h : {} m <br><br>
    <input type=text name=content value="{}"><br><br>
    <input type=submit name=sub value="EDIT">
    <input type=submit name=sub value="DEL">
    <input type=button value="BACK" onclick="back();">
    <input type=hidden name=day value={}>
    <input type=hidden name=eid value={}>
    """.format(select_hour, select_min, db_cont, day, eid)


#print(year, month, day)
def Calendar(year, month, day):
    date = "01{}{}".format(month, year)
    sec = int(time.mktime(datetime.datetime.strptime(date, "%d%m%Y").timetuple()))
    print("""
    <table border=1 style='width:100%; height:50%;'>
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
    #print(convert)
    week = int(time.strftime("%w", convert))
    #print(week)
    cnt = 1
    for i in range((sec-86400*week), (sec+86400*(35-week)), 86400):
        x = time.localtime(i)
        y = int(time.strftime("%Y", x))
        m = int(time.strftime("%m", x))
        d = int(time.strftime("%d", x))
         
        #print(y, year, m, int(month), d, day)
        if cnt%7 == 1:
            print("<tr align=left valign=top>")
        if m == int(month):
            print("<td ondblclick='show_add({},{},{});'".format(y,m,d))
            if y == int(year) and m == int(month) and d == int(day) and action is not None:
                print("style='background-color:#eef9bf;height:100px; width:100px'>")
            else:
                print("style='background-color:#c3e5ae; height:100px; width:100px'>")
            print("{}".format(d))
            cur.execute("SELECT * FROM schedule2 WHERE year={} AND month={} AND date={}".format(y, m, d))
            for i in cur.fetchall():
                print("<br><div onclick='show_edit({});'>{}:{}|{}</div>".format(i[0],i[4],i[5],i[6]))
            print("</td>")
        else:
            print("<td ondblclick='show_add({},{},{});'".format(y,m,d))
            if y == int(year) and m == int(month) and d == int(day) and action is not None:
                print("style='background-color:#eef9bf; height:100px; width:100px'>")
            else:
                print("style='background-color:#97dbae; height:100px; width:100px'>")
            print("{}".format(d))
            cur.execute("SELECT * FROM schedule2 WHERE year={} AND month={} AND date={}".format(y, m, d))
            for i in cur.fetchall():
                print("<br><div onclick='show_edit({});'>{}:{}|{}</div>".format(i[0],i[4],i[5],i[6]))
            print("</td>")
        if cnt%7 == 0:
            print("</tr>")
        
        cnt += 1

    print("</table>")

print("""
        <html>
        <head>
        <style>
        .center{text-align:center;}
        </style></head>

        <script language='javascript'>
            function show_edit(eid) {location.href='planner_copy3.py?action=show_edit&eid='+eid;}
            function show_add(year, month, date) 
                {location.href='planner_copy3.py?action=show_add&year='+year+'&month='+month+'&day='+date;}
            function back() {location.href = 'planner_copy3.py';}
            //function weekly(year, month, day) {location.href = '/cgi-bin/planner_weekly.py?year='+year+'&month='+month'&day='+day;}
        </script>
        <body>
        <form action='/cgi-bin/planner_copy3.py' method='GET'>
        """)

print("<table><tr><td>{}</td></tr>".format(header))
print("<tr><td>")
Calendar(year, month, day)
print("</td>")
if action is not None:
    print("<td valign=top>{}</td>".format(action_html))
print("</tr></table>")
print("</form></body></html>")






