#!/usr/bin/env python

from sql import SQLInterface
import time

dailysql = "select c.CustomerName, strftime(\"%H:%M:%S\", julianday(h.stoptime)-julianday(h.starttime)+0.5) time_worked, description FROM Hours h, Customers C WHERE h.CustomerId = c.CustomerId AND starttime > date('now','-1 day') AND starttime < date('now','+1 day')"

print "[Eaglehour] Daily report generated %s"  % ( time.strftime( "%Y:%m:%d %H:%M:%S", time.localtime() ) )
print

sql = SQLInterface()
sql.cursor.execute(dailysql)
answer = sql.cursor.fetchall()
for row in answer:
	print "%32s %10s %.32s" % (row[0].splitlines()[0], row[1], row[2])
