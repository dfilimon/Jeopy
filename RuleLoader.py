"""
Nasty module that valides .jeop files.
Don't poke around the code too much. You might break it and there are too many ifs to
count.
"""
from __future__ import print_function
import sys, tempfile
import re
import htmllib
import json
from zipfile import *
from PyQt4.QtGui import QMessageBox

def status(type_, message = None, obj = None):
	if type_ == 'jeop':
		print('Loading failed: game file',  message)
		if obj != None:
			print(obj)
	elif type_ == 'json':
		print('Parsing failed:', message)
		print(obj)
	elif type_ == 'file':
		print('File not found in archive:', message, 'referenced by:', obj)
	else:
		print('Validation succeeded')

def validateFile(game, fileName):
	if is_zipfile(fileName) == False: # file not a zip archive
		status('jeop', 'is not a zip archive')
		return False


	z = ZipFile(str(fileName), 'r')

	if z.testzip() != None: # corrupted file
		status('jeop', 'is corrupted')
		return False
	if 'rules.json' not in z.namelist(): # no game description
		status('jeop', 'does not contain a valid game description')
		return False

	try:
		game.rules = json.load(z.open('rules.json'))
	except ( AttributeError, ValueError ) as error:
		status('jeop', 'does not contain a valid JSON rule file', error)
		return False

	# print(game.rules)

	if validateRules(game, z) == False: # rule file not logical
		status('jeop', 'does not describe a valid game')
		return False
	else:
		if game.type == 'html' and not validateResources(z):
			return False
		game.resources = {}
		for resourceName in z.namelist():
			if resourceName != 'rules.json':
				game.resources[resourceName] = z.read(resourceName)
		#resources = [z.read(x) for x in z.namelist() if x != 'rules.json']

	game.tempPath = tempfile.mkdtemp()
	z.extractall(game.tempPath)
	z.close()

	status('success')
	return True


def isList(obj):
	return ( type(obj).__name__ == 'list' )


def isDict(obj):
	return ( type(obj).__name__ == 'dict' )

def isStr(obj):
	return ( type(obj).__name__ == 'unicode' or type(obj).__name__ == 'str' )

def isInt(obj):
	return ( type(obj).__name__ == 'int' )

def validateRules(game, z):
	rules = game.rules
	resources = z.namelist()

	if not isDict(rules):
		status('json', 'not a dictionary:', rules)
		return False

	if 'type' not in rules or rules['type'] not in ['html', 'image']:
		status('json', 'no type specified [html/image]', rules)
		return False

	type_ = rules['type']
	if type_ == 'html':
		if 'template' not in rules:
			status('json', 'no default template', rules)
			return False
		elif not isStr(rules['template']):
			status('json', 'not a string:', rules['template'])
			return False
		elif rules['template'] not in resources:
			status('file', rules['template'], rules)
			return False
		else:
			game.template = ''.join([line for line in z.open(rules['template']).readlines()])

	if 'size' in rules:
		if isDict(rules['size']):
			if 'width' not in rules['size'] or 'height' not in rules['size']:
				status('json', 'invalid size specifications:', rules['size'])
				return False
			if not isInt(rules['size']['width']):
				status('json', 'invalid width:', rules['size']['width'])
				return False
			if not isInt(rules['size']['height']):
				status('json', 'invalid height:', rules['size']['height'])
				return False
			game.width = rules['size']['width']
			game.height = rules['size']['height']
		else:
			status('jsone', 'not a dictionary:', rules['size'])
	else:
		game.width = 800
		game.height = 600


	if 'rounds' not in rules:
		status('json', 'no rounds', rules)
		return False
	elif not isList(rules['rounds']):
		status('json', 'not a list:', rules['rounds'])
		return False
	else:
		numRounds = len(rules['rounds'])
		numQuestions = [ [] for _ in range(numRounds) ]
		numCategories = [ 0 for _ in range(numRounds) ]

		for i in range(numRounds):
			round_ = rules['rounds'][i]

			if not isDict(round_):
				status('json', 'not a dictionary:', round_)
				return False

			if 'buttonFontSize' in round_ and not isInt(round_['buttonFontSize']):
				status('json', 'not an int:', round_['buttonFontSize'])

			if 'labelFontSize' in round_ and not isInt(round_['labelFontSize']):
				status('json', 'not an int:', round_['labelFontSize'])

			if 'categories' not in round_:
				status('json', 'no categories, round:', round_)
				return False
			elif not isList(round_['categories']):
				status('json', 'not a list:', round_['categories'])
				return False

			if 'title' in round_ and not isStr(round_['title']):
				status('json', 'not a string:', round_['title'])
				return False

			numCategories[i] = len(round_['categories'])
			numQuestions[i] = [ 0 for _ in range(numCategories[i]) ]

			for j in range(numCategories[i]):
				category = round_['categories'][j]
				if not isDict(category):
					status('json', 'not a dictionary:', category)
					return False

				if 'title' not in category:
					status('json', 'no title, category:', category)
					return False
				elif not isStr('title'):
					status('json', 'not a string:', category['title'])

				if 'questions' not in category:
					status('json', 'no title/questions, category:', category)
					return False
				elif not isList(category['questions']):
					status('json', 'not a list:', category['questions'])

				numQuestions[i][j] = len(category['questions'])
				#print(numQuestions[i][j])

				for question in category['questions']:
					if 'statement' not in question:
						status('json', 'no statement, question:', question)
						return False
					elif not isStr(question['statement']):
						status('json', 'not a string:', question['statement'])
						return False

					if 'answer' not in question:
						status('json', 'no answer, question:', question)
						return False
					elif not isStr(question['answer']):
						status('json', 'not a string:', question['answer'])
						return False

					if 'value' not in question:
						status('json', 'no value, question:', question)
						return False
					elif not isInt(question['value']):
						status('json', 'not an integer:', question['value'])
						return False
					try:
						value = int(question['value'])
					except TypeError:
						status('json', 'value not convertible to int, question:', question['value'])
						return False

					if type_ == 'html' and 'template' in question:
						if not isStr(question['template']):
							status('json', 'not a string:', question['template'])
							return False
						elif question['template'] not in resources:
							status('file', question['template'], question)
							return False
					elif type_ == 'image':
						if question['statement'] not in resources:
							status('file', question['statement'], question)
							return False
						if question['answer'] not in resources:
							status('file', question['answer'], question)
							return False

	game.type = type_
	game.numRounds = numRounds
	game.numCategories = numCategories
	game.numQuestions = numQuestions

	return True

import HTMLParser
class ResourceValidator(HTMLParser.HTMLParser):
	def __init__(self, zip_):
		#super(ResourceValidator, self).__init__()

		self.fileList = zip_.namelist()
		htmlPattern = re.compile('\.html$', re.IGNORECASE)
		self.htmlFileList = [resourceName
for resourceName in self.fileList
if htmlPattern.search(resourceName) != None]
		HTMLParser.HTMLParser.__init__(self)
		self.valid = True
		for htmlFile in self.htmlFileList:
			self.currentHtmlFile = htmlFile
			try:
				self.feed(zip_.open(htmlFile).read())
			except HTMLParser.HTMLParseError:
				self.valid = False
				return

	def handle_starttag(self, tag, attributeList):
		#print(tag, attributeList)
		#if not self.valid:
		#	return
		for attr in attributeList:
			if (tag == 'img' and attr[0] == 'src' or tag == 'link' and attr[0] == 'href') and (attr[1] not in self.fileList):
				self.valid = False
				status('file', attr[1], self.currentHtmlFile)
				return

def validateResources(zip_):
	validator = ResourceValidator(zip_)
	return validator.valid


def main():
	if len(sys.argv) != 2:
		print('Usage: ./RuleLoader.py <filename>')
	class Game:
		pass
	game = Game()
	if validateFile(game, sys.argv[1]) == True:
		print(sys.argv[1], 'is a valid .jeop file.')
		print(game.numQuestions)
		print(game.numCategories)
if __name__ == '__main__':
	main()
