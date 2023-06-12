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
eid = c.getvalue("eid")
sub = c.getvalue("sub")
action = c.getvalue("action")

date = "{:02d}{:02d}{}".format(int(day),int(month), year)
sec = int(time.mktime(datetime.datetime.strptime(date,"%d%m%Y").timetuple()))

#print(date, sec)

if sub == "ADD":
    try:
        cur.execute("INSERT schedule2 (year, month, date, hour, min, content) VALUES(?, ?, ?, ?, ?, ?)",(year, month, day, hour, min, content))
        conn.commit()
        print("added")
        action == None
    except:
        print("add error")
else:
    if sub == "EDIT":
        try:
            cur.execute("UPDATE schedule2 SET hour='{}', min='{}', content='{}' WHERE eid={}".format(hour, min, content, eid))
            conn.commit()
            print("edited")
            action = None
        except:
            print("edit error")

    elif sub == "DEL":
        try:
            cur.execute("DELETE FROM schedule2 WHERE eid={}".format(eid))
            conn.commit()
            print("deleted")
        except:
            print("del error")


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

next_month_flag = 0
next_year_flag = 0
convert = time.localtime(sec)
week = int(time.strftime("%w", convert))
dates = "<td>h</td>"
l_sec = []
l_m = []
l_y = []
#print(year, month, day)
for i in range(sec-86400*week, sec+86400*(7-week), 86400):
    x = time.localtime(i)
    d = time.strftime("%d", x)
    m = time.strftime("%m", x)
    y = time.strftime("%Y", x)
    #print(d, m, y)
    dates += "<td align=center>{}</td>".format(d)
    l_sec.append(i)
    l_m.append(m)
    l_y.append(y)

#print(l_m, l_y)
name_m0 = calendar.month_name[int(l_m[0])]
name_m6 = calendar.month_name[int(l_m[6])]
y0 = int(l_y[0])
y6 = int(l_y[6])

#print(l_sec)
#print(year, month, day)
header = """
<div align=center>
<input type=hidden name=year value={}>
<input type=hidden name=month value={}>
<input type=hidden name=day value={}>
<input type=submit name=prev value="<<">""".format(year, month, day)
if name_m0 == name_m6 and y0 == y6:
    header += "<label style='font-weight:1000;'>{} of {}</label>".format(name_m0, y0)
elif name_m0 != name_m6 and y0 == y6:
    header += "<label style='font-weight:1000;'>{}-{} of {}</label>".format(name_m0, name_m6, y0)
elif name_m0 != name_m6 and y0 != y6:
    header += "<label style='font-weight:1000;'>{}-{} of {}-{}</label>".format(name_m0, name_m6, y0, y6)
header += """<input type=submit name=next value=">>">"""
header += """
<input align=right type=button value="yearly" onclick='yearly();'>
<input align=right type=button value="weekly" onclick='weekly();'></div>"""

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
            function show_edit(eid) {
                location.href='planner_weekly1.py?action=show_edit&eid='+eid;}
            function back() {location.href='planner_weekly1.py'}
            function weekly() {location.href='/cgi-bin/planner_copy2.py'}
            function yearly() {location.href='/cgi-bin/planner_yearly1.py'}
        </script>
        <body><table style='width:100%; height:50%;'>
        <form action='/cgi-bin/planner_weekly1.py' method=GET>
""")
print(header)
print(row_days)
print(dates)

for i in range(24):
    print("<tr><td width='10px'>{:02d}</td>".format(i), end="")
    for j in l_sec:
        j = int(j)
        x = time.localtime(j)
        d = time.strftime("%d", x)
        m = time.strftime("%m", x)
        y = time.strftime("%Y", x)
        #print(d, m, y)
        cur.execute("SELECT COUNT(*) FROM schedule2 WHERE year={} AND month={} AND date={}".format(year, month, d))
        count = cur.fetchone()
        #print(count[0])
        if count[0] > 0:
            print("<td width='100px' ondblclick='show_add({},{},{},{});' style='background-color:#d6e5fa;'>".format(y, m, d, i))
            cur.execute("SELECT * FROM schedule2 WHERE year={} AND month={} AND date={}".format(y, m, d))
            for k in cur.fetchall():
                db_eid = int(k[0])
                db_day = int(k[3])
                db_hour = int(k[4])
                content = k[6]
                ls = []
                for l in content:
                    ls.append(l)
                if len(content) > 5:
                    cont = ls[0]+ls[1]+ls[2]+ls[3]+ls[4]+ls[5]+"..."
                else:
                    cont = content
                #print(year, month, j)
                #print(j, db_day, i, db_hour)
                if int(d) == db_day and i == db_hour:
                    print("<div onclick='show_edit({})' class='div_content' style='padding:0px;'>{}</div>".format(db_eid, cont))
                    print("<div style='padding:1px;'></div>")
                else:
                    print("<div></div>")
        else:
            print("<td width='15%' onclick='show_add({},{},{},{});' style='background-color:#d6e5fa;'<div></div>".format(y, m, d, i))
        print("</td>", end="")
    print("</tr>")
print("</table>")



print("<br><br>")
if action == "show_add":
    #print(year, month, day, hour)
    select_min = "<select name=min><option value={:02d}>{:02d}</option>".format(int(min), int(min))
    for i in range(60):
        select_min += "<option value={:02d}>{:02d}</option>".format(i, i)
    select_min += "</select>"
    print("""
    <input type=hidden name=hour value={}>
    {}/{} - {:02d} h : {} m <br><br>
    <input type=text name=content><br><br>
    <input type=submit name=sub value="ADD">
    <input type=button value="BACK" onclick="back();">
    """.format(hour, month, day, int(hour), select_min))

elif action == "show_edit":
    print("<input type=hidden name=eid value={}>".format(int(eid)))
    #print("SELECT * FROM schedule2 WHERE eid={}".format(int(eid)))
    cur.execute("SELECT * FROM schedule2 WHERE eid='{}'".format(int(eid)))
    for i in cur.fetchall():
        mdb_hour = int(i[4])
        mdb_min = int(i[5])
        mdb_con = i[6]
    print(mdb_hour, mdb_min, mdb_con)
    select_hour = "<select name=hour><option value={:02d}>{:02d}</option>".format(mdb_hour, mdb_hour)
    for i in range(24):
        select_hour += "<option value={:02d}>{:02d}</option>".format(i, i)
    select_hour += "</select>"

    select_min = "<select name=min><option value={:02d}>{:02d}</option>".format(mdb_min, mdb_min)
    for i in range(60):
        select_min += "<option value={:02d}>{:02d}</option>".format(i, i)
    select_min += "</select>"
    
    print("""
    {}/{} - {} h : {} m <br><br>
    <input type=text name=content value='{}'><br><br>
    <input type=submit name=sub value="EDIT">
    <input type=submit name=sub value="DEL">
    <input type=button value="BACK" onclick="back();">
    """.format(month, day, select_hour, select_min, mdb_con))

print("</body></html>")
