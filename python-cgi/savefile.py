#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os,sys, urllib
import cgitb; cgitb.enable()
import xml.etree.ElementTree as ET
import json
import string
from pyExcelerator import *

########################################################################
def is_dictionary_word(word):#Determine if the input word is in the dictionary
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

def is_name(word):#determine if the input word is a name of people by using a self-made name database
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
	#Initiate the name database
	name_DB = open('nameDB.txt', 'r')
	name_list = name_DB.readlines()
	names = [name.strip() for name in name_list if name != '']
	for name in names:
		if word_without_punctuation.lower() == name.lower():
			return True
	return False

def process(xml_file):
	#set up three json files
	json_name=open(xml_file.replace('.xml', '_name.json'), 'w')
	json_removed_dictionary_words=open(xml_file.replace('.xml', '_removed_dictionary_words.json'), 'w')
	json_removed_hocr_noise_words=open(xml_file.replace('.xml', '_removed_hocr_noise_words.json'), 'w')
	name={'names':[]}
	removed_dictionary_words = {'removed_dictionary_words':[]}
	removed_hocr_noise_words = {'removed_hocr_noise_words':[]}
	#parse the xml file
	tree = ET.parse(xml_file)
	root = tree.getroot()
	#get all the text under the node<Value>
	for element in root.getiterator(tag = 'Value'):
		if is_dictionary_word(element.text):
			removed_dictionary_words['removed_dictionary_words'].append(element.text)
		elif is_name(element.text):
			name['names'].append(element.text)
		else:
			removed_hocr_noise_words['removed_hocr_noise_words'].append(element.text)
	#encode and output to three json files
	json_name.write(json.dumps(name))
	json_removed_dictionary_words.write(json.dumps(removed_dictionary_words))
	json_removed_hocr_noise_words.write(json.dumps(removed_hocr_noise_words))
	json_name.close()
	json_removed_dictionary_words.close()
	json_removed_hocr_noise_words.close()
	#set up a xls file to store the information in the three json files 
	w = Workbook()
	ws = w.add_sheet('Information')
	ws.write(0,0,'name')
	i = 1
	for single_name in name['names']:
		ws.write(i, 0, single_name)
		i += 1
	ws.write(0,1,'removed dictionary words')
	i = 1
	for single_dictionary_word in removed_dictionary_words['removed_dictionary_words']:
		ws.write(i, 1, single_dictionary_word)
		i += 1
	ws.write(0,3,'removed hocr noise words')
	i = 1
	for single_noise_word in removed_hocr_noise_words['removed_hocr_noise_words']:
		ws.write(i, 2, single_noise_word)
		i += 1
	w.save(xml_file.replace('.xml', '_information.xls'))
########################################################################

form = cgi.FieldStorage()

# Get the filename
fileitem = form['filename']

# Detect if the file has been uploaded successfully
if fileitem.filename:
	# Setup the file path
	filename = os.path.basename(fileitem.filename)
	filepath='/tmp/'+filename
	open(filepath, 'wb').write(fileitem.file.read())
	process(filepath)
else:
	# Error alert
	message = 'No file was uploaded'
	print """\
	Content-Type: text/html\n
	<html>
	<body>
	   <p>%s</p>
	</body>
	</html>
	""" % (message,)


########################################################################
command='cd /tmp;'
command+= 'tar -czf result.tar.gz '+filename.replace('.xml', '_name.json')+' '+ filename.replace('.xml', '_removed_dictionary_words.json')+\
' ' +filename.replace('.xml', '_removed_hocr_noise_words.json')+' '+filename.replace('.xml', '_information.xls')+';'
command+='cd /var/www/cgi-bin'
#tmp = open('/tmp/tmp.txt','w')
#tmp.write(command)
#tmp.close()
a=os.system(command)#To suppress the output
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
