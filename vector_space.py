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
#    along with Foobar. If not, see <http://www.gnu.org/licenses/>.

import sys
import json
from data import Data 
from gensim.corpora import Dictionary
from gensim.similarities import MatrixSimilarity
from gensim.models import TfidfModel, LsiModel, RpModel, ldamodel
from utils import Unbuffered, write

class VectorSpace:
	def __init__(self, texts, method='LSI', num_t=100, debug=False):
		self.texts = texts      # item texts
		self.method = method    # vector space method to represent the items
		self.num_t = num_t      # number of topics for LSI, RP and LDA
		self.debug = debug      # print status and debug messages
		self.compute()

	def compute(self):
		vec_texts = [text.split() for text in self.texts]
		write("\n    "+"-> Computing the dictionary".ljust(50,'.')) if self.debug else ''
		dictionary = Dictionary(vec_texts)
		write("[OK]") if self.debug else ''
		write("\n    "+"-> Creating the bag-of-words space".ljust(50,'.')) if self.debug else '' 
		corpus = [dictionary.doc2bow(vec) for vec in vec_texts]
		write("[OK]") if self.debug else ''
		write("\n    "+("-> Creating the %s space" % self.method).ljust(50,'.') ) if self.debug else '' 
		tfidf_space = TfidfModel(corpus)
		tfidf_corpus = tfidf_space[corpus]
		if self.method == 'TFIDF':
			self.space = tfidf_space
			self.index = MatrixSimilarity(tfidf_corpus)
		elif self.method == 'LSI': 
			self.space = LsiModel(tfidf_corpus, id2word=dictionary, num_topics=self.num_t) 
			self.index = MatrixSimilarity(self.space[tfidf_corpus])
		elif self.method == 'RP': 
			self.space = RpModel(tfidf_corpus, id2word=dictionary, num_topics=self.num_t) 
			self.index = MatrixSimilarity(self.space[tfidf_corpus])
		elif self.method == 'LDA':
			self.space = ldamodel.LdaModel(tfidf_corpus, id2word=dictionary, 
														 num_topics=self.num_t)
			self.index = MatrixSimilarity(self.space[tfidf_corpus])
		self.dictionary = dictionary
		write("[OK]\n") if self.debug else ''

	def n_most_similar(self, idx, N=10):
		text = self.texts[idx]
		vec_bow = self.dictionary.doc2bow(text.split())
		vec_space = self.space[vec_bow]
		sims = self.index[vec_space]
	 	sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])[1:N+1]
	 	indices = [ss[0] for ss in sorted_sims]
	 	scores  = [ss[1] for ss in sorted_sims]
		return indices, scores

if __name__== '__main__':
	items = json.loads(open('example.json').read())
	data  = Data(items)
	vsm   = VectorSpace(data.texts)
	example = data.items[0]
	print "Example (id=%d, title=%s):" % (example['id'], example['title'])
	indices, scores = vsm.n_most_similar(example['id'], N=5) 
	for i, idx in enumerate(indices):
		item = data.items[idx]
		print "%d. %s (%.3f)" % (i+1, item['title'], scores[i])