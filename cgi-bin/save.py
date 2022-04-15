#!/usr/bin/python

print('Content-type: text/html\n')

import cgitb; cgitb.enable()

import pymysql
ip = '127.0.0.1'
db = 'billbord'
user = 'root'
port = 3308
passwrd  = 'PSPS2053'
conn = pymysql.connect(host =ip,db = db,user = user,port = port,passwd=passwrd)
curs = conn.cursor(cursor=pymysql.cursors.DictCursor) #设置返回内容为字典的形式
"""
实现了数据保存
通过cgi传递过来的数据：reply_to,sender,text,subject数据插入数据库；
"""
import cgi, sys
form = cgi.FieldStorage()

sender = form.getvalue('sender')
subject = form.getvalue('subject')
text = form.getvalue('text')
reply_to = form.getvalue('reply_to')

if not (sender and subject and text):
    print('Please supply sender, subject, and text')
    sys.exit()

if reply_to is not None:
    query = ("""INSERT INTO message(reply_to, sender, subject, text) VALUES(%s, %s, %s, %s)""",
             (int(reply_to), sender, subject, text))
else:
    query = ("""INSERT INTO message(sender, subject, text) VALUES(%s, %s, %s)""", (sender, subject, text))

curs.execute(*query)
conn.commit()

print("""
<html>

<head>
  <title>Message Saved</title>
</head>
<body>
  <h1>Message Saved</h1>
  <hr />
  <a href='main.py'>Back to the main page</a>
</body>
</html>s
""")