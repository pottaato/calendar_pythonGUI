#!/usr/bin/python3
import sys
import cgi
import cgitb
import time
import datetime
import calendar

print("Content-type: text/html\r\n\r\n")
cgitb.enable()
c = cgi.FieldStorage()

year = c.getvalue("year") if c.getvalue("year") else int(datetime.datetime.now().strftime("%Y"))
month = c.getvalue("month") if c.getvalue("month") else int(datetime.datetime.now().strftime("%m"))
n = c.getvalue("next")
p = c.getvalue("prev")

if n == ">>":
    year = int(year) + 1
if p == "<<":
    year = int(year) - 1

year = int(year)
month = int(month)
#print(year, month)
header = """
<div align=center>
<input type=hidden name=year value={}>
<input type=hidden name=month value={}>
<input type=submit name=prev value="<<">
<label style='font-weight:1000;'>Year of {}</label>
<input type=submit name=next value=">>">
<input type=button align=right value="monthly" onclick="monthly({},{});">
<input type=button align=right value="weekly" onclick="weekly({},{});">
""".format(year, month, year, year, month, year, month)

table_month = """
<table style='width:100%'; height:50%;'>
"""
count = 0
for i in range(1, 4, 1):
    table_month += "<tr>"
    for j in range(1, 5, 1):
        count += 1
        name_month = calendar.month_name[count]
        if int(month) == count:
            table_month += "<td ondblclick='go_month({},{});' style='background-color:lightblue'><p align=center>{}</p></td>".format(year, month, name_month)
        else:
            table_month += "<td onclick='change_month({});' style='background-color:lightgreen'><p align=center>{}</p></td>".format(int(count), name_month)
    table_month += "</tr>"
table_month += "</table>"

print("""
<html>
<head>
<script language:'javascript'>
    function change_month(month) {
        location.href='planner_yearly1.py?month='+month;}
    function go_month(year, month) {location.href='/cgi-bin/planner_copy2.py?year='+year+'&month='+month;}
    function monthly(year, month) {
        location.href='/cgi-bin/planner_copy2.py?year='+year+'&month='+month;}
    function weekly(year, month) {
        location.href='/cgi-bin/planner_weekly1.py?year='+year+'&month='+month;}
</script>
<body><form action='/cgi-bin/planner_yearly1.py' method='GET'>
""")
print(header)
print(table_month)
print("</form></body></html>")


        
    
