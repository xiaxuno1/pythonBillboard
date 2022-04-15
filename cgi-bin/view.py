#!/usr/bin/python

print('Content-type: text/html\n')

import cgitb; cgitb.enable()
"""
根据传入的ID在数据库查询信息以html方式显示内容此条内容的信息
跳转的链接，跳转到回复编辑的界面
"""
import pymysql
ip = '127.0.0.1'
db = 'billbord'
user = 'root'
port = 3308
passwrd  = 'PSPS2053'
conn = pymysql.connect(host =ip,db = db,user = user,port = port,passwd=passwrd)
curs = conn.cursor(cursor=pymysql.cursors.DictCursor) #设置返回内容为字典的形式

import cgi, sys
form = cgi.FieldStorage()
id = form.getvalue('id') #获取cgi传递的参数

print("""
<html>
  <head>
    <title>View Message</title>
  </head>
  <body>
    <h1>View Message</h1>
    """)

try: id = int(id)
except:
     print('Invalid message ID')
     sys.exit()

curs.execute('SELECT * FROM message WHERE id = %s', (format(id),))
rows = curs.fetchall()

if not rows:
     print('Unknown message ID')
     sys.exit()

row = rows[0]

print("""
     <p><b>Subject:</b> {subject}<br />
     <b>Sender:</b> {sender}<br />
     <pre>{text}</pre>
     </p>
     <hr />
     <a href='main.py'>Back to the main page</a>  <!--返回主页的方式-->
     | <a href="edit.py?reply_to={id}">Reply</a>  <!--跳转到编辑界面的链接-->
  </body>
</html>
""".format(subject=row['subject'],sender=row['sender'],text=row['text'],id=row['id']))