# !/usr/bin/python

print("Content-Type:text/html\n")

import pymysql
import cgitb;cgitb.enable()#调试模块，错误可以打印在网页上

ip = '127.0.0.1'
db = 'billbord'
user = 'root'
port = 3308
passwrd  = 'PSPS2053'
conn = pymysql.connect(host =ip,db = db,user = user,port = port,passwd=passwrd)
curs = conn.cursor(cursor=pymysql.cursors.DictCursor) #设置返回内容为字典的形式

print("""
<html>
  <head>
    <title>The FooBar Bulletin Board</title>
  </head>
  <body>
    <h1>The FooBar Bulletin Board</h1>
    """)

curs.execute('SELECT * FROM message')
# rows = curs.dictfetchall() mymysql不支持dictfetchall(),pymysql是在游标设置的
rows = curs.fetchall()

toplevel = []
children = {}

#根据reply_to判断是否为回复的消息，如果不是回复，则为顶层消息；如果是恢复，确定其层级
for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else:
        children.setdefault(parent_id, []).append(row) #如果键不存在则插入值为默认值的键，就是有就插入没有就创建
        #如果是回复的消息，则添加到children字典中
def format(row):
    """此方法实现了对消息和回复的显示，如果有回复消息，则递归调用显示"""
    print(row['subject']) #打印主题
    try: kids = children[row['id']] #是否有回复消息，如果有，则递归调用回复消息，打印引用消息
    except KeyError: pass
    else:
        print('<blockquote>')
        for kid in kids:
            format(kid)
        print('</blockquote>')

print("""<p>""")

for row in toplevel:
    format(row)

print("""
</p>
</body>
</html>
""")