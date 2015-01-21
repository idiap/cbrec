#    Copyright (c) 2014 Idiap Research Institute, http://www.idiap.ch/
#    Written by Nikolaos Pappas <nikolaos.pappas@idiap.ch>,
#
#    This file is part of CBRec.
#
#    CBRec is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3 as
#    published by the Free Software Foundation.
#
#    CBRec is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CBRec. If not, see <http://www.gnu.org/licenses/>.

import sys
import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from utils import Unbuffered, write

class Data:
	def __init__(self, items, attrs=None, preprocess=True, debug=False): 
		self.texts  = []            # item texts
		self.items  = items         # item hash representations
		self.attrs  = attrs         # item attributes to keep
		self.regex  = '\r|\t|\n|--' # symbols to be removed
		self.min_w  = 2             # minimum length of each word
		self.debug  = debug	        # print status and debug messages
		if attrs is None: 
			self.attrs = list(set(items[0].keys()) - set(['id']))
		self.extract_text()
		self.preprocess() if preprocess else ''

	def extract_text(self):
		write("\n    "+"-> Extracting text".ljust(50,'.')) if self.debug else ''
		for idx, item in enumerate(self.items):
			attr_texts = []
			for attr in self.attrs:
				attr_texts.append(item[attr])
			text = " ".join(attr_texts).replace(self.regex,"")
			self.texts.append(text) 
		write("[OK]") if self.debug else ''

	def preprocess(self):
		write("\n    "+"-> Preprocessing text".ljust(50,'.')) if self.debug else ''
		stoplist  = stopwords.words('english')
		wregex = RegexpTokenizer(r'\w+')
		for idx, item in enumerate(self.items):
			words = wregex.tokenize(self.texts[idx].lower()) 
			final_words = []
	   		for iw, word in enumerate(words): 
				if word not in stoplist and len(word) > self.min_w:
					final_words.append(word)
			self.texts[idx] = ' '.join(final_words)
		write("[OK]") if self.debug else ''

if __name__== '__main__':
	items = json.loads(open('example.json').read())
	data  = Data(items)
	example = data.items[0]
	print "Total items: %d" % len(data.texts)
	print "Example (id=%d, title=%s):" % (example['id'], example['title'])
	print data.texts[0]
