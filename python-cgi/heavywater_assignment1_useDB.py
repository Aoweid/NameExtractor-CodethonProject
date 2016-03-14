import xml.etree.ElementTree as ET
import json
import string

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
