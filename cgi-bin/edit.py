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
实现了回复功能；接收传递过来的id,作为replay_to编号
"""
import cgi, sys
form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print("""
<html>
  <head>
    <title>Compose Message</title>
  </head>
  <body>
    <h1>Compose Message</h1>

    <form action='save.py' method='POST'>
    """)

subject = ''
if reply_to is not None:
    print('<input type="hidden" name="reply_to" value="{}"/>'.format(reply_to))
    curs.execute('SELECT subject FROM message WHERE id = %s', (format(reply_to),))
    subject = curs.fetchone()['subject'] #返回查询到的subject的主题
    if not subject.startswith('Re: '):
        subject = 'Re: ' + subject
"""
以html的格式展示回复数据；包括回复主题；回复人；回复内容
提供保存链接
"""
print("""
     <b>Subject:</b><br />
     <input type='text' size='40' name='subject' value='{}' /><br /> <!--br为html的换行元素-->
     <b>Sender:</b><br />
     <input type='text' size='40' name='sender' /><br />
     <b>Message:</b><br />
     <textarea name='text' cols='40' rows='20'></textarea><br />
     <input type='submit' value='Save'/>
     </form>
     <hr />
     <a href='main.py'>Back to the main page</a>'
  </body>
</html>
""".format(subject))