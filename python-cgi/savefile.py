#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

# 获取文件名
fileitem = form['filename']

# 检测文件是否上传
if fileitem.filename:
   # 设置文件路径
   filename = os.path.basename(fileitem.filename)
   filepath='/tmp/'+filename
   open(filepath, 'wb').write(fileitem.file.read())
   message = 'The file "' + filepath + '" was uploaded successfully'
else:
   message = 'No file was uploaded'


# print """\
# Content-Type: text/html\n
# <html>
# <body>
#    <p>%s</p>
# </body>
# </html>
# """ % (message,)

#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 文件下载
print """Content-Disposition: attachment; filename=\"%s\"\r\n\n"""%(filename);

# 打开文件
fo = open(filepath, "rb")
str = fo.read();
print str
# 关闭文件
fo.close()