#!/usr/bin/python3

import time
import datetime
import cgi
import cgitb
import sqlite3
import re
import calendar

print("Content-type:text/html\n\n")
print("<meta http-equiv='Content-Type' content='text/html'; charset='utf-8'>")

form = cgi.FieldStorage()

now_year = form.getvalue('year') if form.getvalue('year') else datetime.datetime.now().strftime('%Y')
now_month = form.getvalue('month') if form.getvalue('month') else datetime.datetime.now().strftime('%m')
now_day = form.getvalue('day') if form.getvalue('day') else datetime.datetime.now().strftime('%d')
now_hour = form.getvalue('hour') if form.getvalue('hour') else datetime.datetime.now().strftime('%H')
now_minute = form.getvalue('minute') if form.getvalue('minute') else datetime.datetime.now().strftime('%M')
now_content = form.getvalue('content') if form.getvalue('content') else ''
now_content = re.sub(r'^\s+|\s+$', '', now_content)
renew = form.getvalue('renew') if form.getvalue('renew') else ''
run_action = form.getvalue('action') if form.getvalue('action') else ''
run_revise = form.getvalue('revise') if form.getvalue('revise') else ''

if run_action == '<<':
	date = "15/" + now_month + "/" + now_year
	second = int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))
	x = time.localtime(second-86400*30)
	now_year = time.strftime("%Y", x)
	now_month = time.strftime("%m", x)
	run_revise = ''

elif run_action == '>>':
	date = "15/" + now_month + "/" + now_year
	second = int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))
	x = time.localtime(second+86400*30)
	now_year = time.strftime("%Y", x)
	now_month = time.strftime("%m", x)
	run_revise = ''

elif run_action == 'ADD':
	if len(now_content) != 0:
		conn = sqlite3.connect('calendar.db')
		c = conn.cursor()
		date = now_year + '-' + now_month + '-' + now_day
		c.execute("INSERT INTO calendar (date, hour, minute, content, time) VALUES (?, ?, ?, ?, ?)", (date, now_hour, now_minute, now_content, int(time.time())))
		conn.commit()
		conn.close()

else:
	if run_action == 'DEL':
		conn = sqlite3.connect('calendar.db')
		c = conn.cursor()
		c.execute("DELETE FROM calendar WHERE id =" + run_revise)
		conn.commit()
		conn.close()
		run_revise = ''

	if run_action == 'EDIT':
		if len(now_content) != 0:
			conn = sqlite3.connect('calendar.db')
			c = conn.cursor()
			c.execute("UPDATE calendar SET hour = ?,  minute = ?, content = ? WHERE id = ?", (now_hour, now_minute, now_content, run_revise))
			conn.commit()
			conn.close()

	if len(run_revise) != 0:
		conn = sqlite3.connect('calendar.db')
		c = conn.cursor()
		for row in c.execute("SELECT date, hour, minute, content FROM calendar WHERE id='" + run_revise + "'"):
			now_year = (row[0].split("-"))[0]
			now_month = (row[0].split("-"))[1]
			now_day = (row[0].split("-"))[2]
			now_hour = row[1]
			now_minute = row[2]
			now_content = row[3]
		conn.close()

#now_year = datetime.datetime.now().strftime('%Y')
#now_month = datetime.datetime.now().strftime('%m')
#now_day = datetime.datetime.now().strftime('%d')

date = "01/" + now_month + "/" + now_year
second = int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))
#print(second)

select_year = '<select name=year class=select onChange="xmlhttpPost();">'
#select_year = '<select name=year class=select>'
for i in range(1990,2051):
	ed = 'selected' if int(i) == int(now_year) else ''
	select_year += ('<option value={year} {ed}>{year}</option>'.format(year=i,ed=ed))
select_year += '</select>'

select_month = '<select name=month class=select onChange="xmlhttpPost();">'
#select_month = '<select name=month class=select>'
for i in range(1,13):
	ed = 'selected' if int(i) == int(now_month) else ''
	i = '0' + str(i) if len(str(i)) == 1 else i
	select_month += ('<option value={month} {ed}>{month}</option>'.format(month=i,ed=ed))
select_month += '</select>'

select_day = '<select name=day class=select>'
for i in range(second, (second+86400*32), 86400):
	x = time.localtime(i)
	month = time.strftime("%m", x)
	i = time.strftime("%d", x)
	if int(month) != int(now_month):
		break
	ed = 'selected' if int(i) == int(now_day) else ''
	select_day += ('<option value={day} {ed}>{day}</option>'.format(day=i,ed=ed))
select_day += '</select>'

select_hour = '<select name=hour class=select>'
for i in range(0,24):
	ed = 'selected' if int(i) == int(now_hour) else ''
	i = '0' + str(i) if len(str(i)) == 1 else i
	select_hour += ('<option value={hour} {ed}>{hour}</option>'.format(hour=i,ed=ed))
select_hour += '</select>'

select_minute = '<select name=minute class=select>'
for i in range(0,60):
	ed = 'selected' if int(i) == int(now_minute) else ''
	i = '0' + str(i) if len(str(i)) == 1 else i
	select_minute += ('<option value={minute} {ed}>{minute}</option>'.format(minute=i,ed=ed))
select_minute += '</select>'

def Calendar():

	if len(run_revise) != 0:
		revise_html = ("""
	{hour}：{minute}
	<input type=text name=content value='{content}' size=30>
	<input type=submit name=action value="EDIT">
	<input type=submit name=action value="DEL">
	<input type=button value="RETURN" onClick="back();">
	<input type=hidden name=revise value={revise}>
	""".format(hour=select_hour,minute=select_minute,content=now_content,revise=run_revise))

	else:
		revise_html = ("""
	{hour}：{minute}
	<input type=text name=content size=30>
	<input type=submit name=action value="ADD">
	""".format(hour=select_hour,minute=select_minute))

	print("""
		<table>
		<tr>
			<td>
			<table width=100% border=0>
			<tr>
				<td align=left>{year}&nbsp;/&nbsp;{month}&nbsp;/&nbsp;{day}，{revise}</td>
				<td align=right>
					<input type=submit name=action value="<<">
					<input type=submit name=action value=">>">
				</td>
			</tr>
			</table>
			</td>
		</tr>
		<tr>
			<td>
			<table border=1>
			<tr class=title>
				<td align="center">SUN</td>
				<td align="center">MON</td>
				<td align="center">TUE</td>
				<td align="center">WED</td>
				<td align="center">THU</td>
				<td align="center">FRI</td>
				<td align="center">SAT</td>
			</tr>
	""".format(year=select_year,month=select_month,day=select_day,revise=revise_html))

	x = time.localtime(second)
	week = int(time.strftime("%w", x))
	#print(week)

	conn = sqlite3.connect('calendar.db')
	c = conn.cursor()

	count = 1
	for i in range((second-86400*week), (second+86400*(35-week)), 86400):
		if (count % 7) == 1:
			print('<tr>')

		x = time.localtime(i)
		year = time.strftime("%Y", x)
		month = time.strftime("%m", x)
		day = time.strftime("%d", x)
		td_color = 'even' if int(month) == int(now_month) else 'odd'
		print('<td class=' +  td_color + '>' + day + '<br>')
		date = year + '-' + month + '-' + day
		for row in c.execute("SELECT id, hour, minute, content FROM calendar WHERE date='" + date + "' ORDER BY hour ASC, minute ASC"):
			print("<div style='background-color: #1F51C6; padding: 0px' onClick='revise({});'><font class=content>{}：{}&nbsp;{}</font></div>".format(row[0],row[1],row[2],row[3]))
			print('<div style="padding: 1px"</div>')

		print('</td>')
		if (count % 7) == 0:
			print('</tr>')

		count += 1

	conn.close()
	print("""
			</table>
			</td>
		</tr>
		</table>
	""")

print("""
<html>
<meta http-equiv='Content-Type' content='text/html'; charset='utf-8'>
	<style>
		.title {
			padding: 2px 2px 2px 2px;
			background-color: #77A5A5;
			font-size: 16pt;
			color: #1e5799;
			font-weight: bold;
			font-family: sans-serif;
		}

		.odd {
			padding: 2px 2px 2px 2px;
			background-color: #E9E9F3;
			font-size: 12pt;
			color: #333333;
			font-family: sans-serif;
			height: 100px;
			width: 150px;
			text-align: left;
			vertical-align: text-top;
		}

		.even {
			padding: 2px 2px 2px 2px;
			background-color: #FFBF00;
			font-size: 12pt;
			color: #333333;
			font-family: sans-serif;
			height: 100px;
			width: 150px;
			text-align: left;
			vertical-align: text-top;
		}

		.select {
			font: bolder 12pt sans-serif;
			padding: 1px 1px 1px 1px;
			border: solid 1px #808080;
			background-color: #F8FFFF;
		}

		.content {
			font-size: 10pt;
			color: #EEEEEE;
			font-weight: bold;
			font-family: sans-serif;
		}
	</style>

    <script language='javascript'>
		function revise(id) {
			location.href = 'calendar.cgi?revise=' + id;
		}

		function back() {
			location.href = 'calendar.cgi';
		}
    </script>
	<body>
	<form action="calendar.cgi" method="post">
	""")

Calendar()

print("""
	</form>
	</body>
</html>""")

