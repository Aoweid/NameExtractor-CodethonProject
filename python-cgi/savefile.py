#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os
import cgitb; cgitb.enable()
from heavywater_assignment1_useDB import process
form = cgi.FieldStorage()

# 获取文件名
fileitem = form['filename']

# 检测文件是否上传
if fileitem.filename:
	# 设置文件路径
	filename = os.path.basename(fileitem.filename)
	filepath='/tmp/'+filename
	open(filepath, 'wb').write(fileitem.file.read())
	process(filepath)
else:
	# 出错提示
	message = 'No file was uploaded'
	print """\
	Content-Type: text/html\n
	<html>
	<body>
	   <p>%s</p>
	</body>
	</html>
	""" % (message,)

#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 文件下载
# print """Content-Disposition: attachment; filename=\"%s\"\r\n\n"""%(filename);

# 打开文件
# fo = open(filepath, "rb")
# str = fo.read();
# print str
# 关闭文件
# fo.close()

########################################################################
downloadlist=[
	xml_file+'_removed_dictionary_words.json',
	xml_file+'_removed_hocr_noise_words.json'
	]
for name in downloadlist:
    header = [
        "Content-Type: application/octet-stream",
        "Content-Transfer-Encoding: binary",
        "Accept-Ranges: bytes",
        "Accept-Length: %d" % os.stat(urllib.unquote(name)).st_size,
        "Content-Disposition: attachment;filename=\"%s\"" % os.path.basename(urllib.unquote(name)),

        "\r\n"
        ]
    sys.stdout.write("\r\n".join(header))
    data = open(name, 'rb').read()
    sys.stdout.write(data)
    sys.stdout.flush()
    if os.path.isdir('r:\\'):
        metaf = [str(len(data)), urllib.unquote(name), os.path.abspath(urllib.unquote(name))]
        open('r:\\ot.txt', 'wb').write('\r\n'.join(metaf))
	else:
    	print "Content-Type: text/html\n"
    	print "<html><head><title>Error</title></head><body><pre>Not has file name</pre></body></html>"