#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os,sys, urllib
import cgitb; cgitb.enable()
import xml.etree.ElementTree as ET
import json
import string

########################################################################
def is_dictionary_word(word):
	word_without_punctuation = word.encode('utf-8').translate(None, string.punctuation+'·')
	if word_without_punctuation == '':
		return False
	dictionary = open('dictionary.txt','r')
	dictionary_words_list1 = dictionary.readlines()
	dictionary_words = [word.strip() for word in dictionary_words_list1]
	for words in dictionary_words:
		if word_without_punctuation.lower() == words.lower():
			return True
	return False

def is_name(word):
	word_without_punctuation = word.encode('utf-8').translate(None, string.punctuation+'·')
	if word_without_punctuation == '':
		return False
	if not 'A'<= word_without_punctuation[0] <= 'Z':
		return False
	for i in range(1, len(word_without_punctuation)):
		if not "a" <= word_without_punctuation[i] <= "z":
			return False
		else:
			continue
	name_DB = open('nameDB.txt', 'r')
	name_list = name_DB.readlines()
	names = [name.strip() for name in name_list if name != '']
	for name in names:
		if word_without_punctuation.lower() == name.lower():
			return True
	return False

def process(xml_file):
	# xml_file = raw_input('Please enter the name of the xml file.')
	# xml_file='ocr-sample2.xml'
	json_name=open(xml_file+'_name.json', 'w')
	json_removed_dictionary_words=open(xml_file+'_removed_dictionary_words.json','w')
	json_removed_hocr_noise_words=open(xml_file+'_removed_hocr_noise_words.json', 'w')
	name={'names':[]}
	removed_dictionary_words = {'removed_dictionary_words':[]}
	removed_hocr_noise_words = {'removed_hocr_noise_words':[]}
	tree = ET.parse(xml_file)
	root = tree.getroot()
	for element in root.findall('Value'):
		if is_dictionary_word(element.text):
			removed_dictionary_words['removed_dictionary_words'].append(element.text)
		elif is_name(element.text):
			name['names'].append(element.text)
		else:
			removed_hocr_noise_words['removed_hocr_noise_words'].append(element.text)
	json_name.write(json.dumps(name))
	json_removed_dictionary_words.write(json.dumps(removed_dictionary_words))
	json_removed_hocr_noise_words.write(json.dumps(removed_hocr_noise_words))
	json_name.close()
	json_removed_dictionary_words.close()
	json_removed_hocr_noise_words.close()
########################################################################

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
command='cd /tmp;'
command+= "tar -zcvf result.tar.gz '"+filename+"_name.json' '"+ filename+"_removed_dictionary_words.json' '" +filename+"_removed_hocr_noise_words.json';"
command+='cd /var/www/cgi-bin'
a=os.system(command)#不要删除变量a, 这是为了抑制输出, 因为这些输出会被当做应答
name='/tmp/result.tar.gz'

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
