import xml.etree.ElementTree as ET
import json
import string
import urllib, urllib2, httplib
import HTMLParser
import bs4
from bs4 import BeautifulSoup

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

def is_name(key):
	'''Use facebook website to search the input key, if there are same results
	 returned, the key will be take as name and return True, if not, the key
	 is not a name and return False'''
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
	# Use Facebook website to search
	search_url_header = "https://www.facebook.com/search/people/?q=key"
	url=search_url_header.replace('key',key.replace(' ','+'))
	# In the disguise of Firefox, send the searching demand
	headers={
	'User-Agent' : "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0"
	}
	req = urllib2.Request(url)
	fetchback= urllib2.urlopen(req)
	htmlpage=fetchback.read()
	# Use BeautifulSoup to analysis
	soup=BeautifulSoup(htmlpage,"html5lib")
	html_parser = HTMLParser.HTMLParser()
	comment= html_parser.unescape(soup.code.string) # Useful information at the node <code>
	target=BeautifulSoup(comment,"html5lib")
	result=target.find_all("div",class_="_5d-5") # Names saved in the node <div class="_5d-5">
	match=0
	for name in result:
		relname=name.string[:name.string.find('(')]
		if relname.lower().find(key.lower()) != -1:
			match+=1;
	if match>0:
		return True
	else:
		return False

def main():
	xml_file='ocr-sample5.xml'
	json_name=open(xml_file+'_name.json', 'w')
	json_removed_dictionary_words=open(xml_file+'_removed_dictionary_words.json','w')
	json_removed_hocr_noise_words=open(xml_file+'_removed_hocr_noise_words.json', 'w')
	name={'names':[]}
	removed_dictionary_words = {'removed_dictionary_words':[]}
	removed_hocr_noise_words = {'removed_hocr_noise_words':[]}
	tree = ET.ElementTree(file = xml_file)
	root = tree.getroot()
	for element in tree.iter(tag='Value'):
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

if __name__ == '__main__':
	main()
