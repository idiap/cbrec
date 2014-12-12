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

"""Usage:
    generate.py --input=<path> --output=<path> [options]

Options:
    -v, --version                      show program's version number and exit
    -h, --help                         show this help message and exit
    -d, --debug	                       print status and debug messages [default: False]
    -r, --display                      display recommendations per item [default: False]
    -i, --input=<path>                 path to JSON file to be used as input
    -o, --output=<path>                path to JSON file to be used as output
    --extract=<attributes>             comma separated JSON attributes to be used [default: All]
    --preprocess                       whether to preprocess text or not  [default: True]
    --method=<TFIDF|LSI|RP|LDA>        vector space method to represent the items [default: LSI]
    --k=<integer>                      number of topics for LSI, RP and LDA [default: 100]
    --N=<integer>                      number of recommendations [default: 5]
"""
import json
import sys
from docopt import docopt
from data import Data
from vector_space import VectorSpace
from utils import Unbuffered, write

class Generator:
	def __init__(self, options, items=None): 
		self.items = items  					# item hash representations
		self.debug = options['--debug']			# print status and debug messages
		self.display = options['--display']		# display recommendations per item

	def run(self):
		if self.items is None:
			write("[+] Loading items:") if self.debug else ''
			self.items = json.loads(open(options['--input']).read())
		self.data  = Data(self.items, preprocess=options['--preprocess'],
									  debug=self.debug)
		
		write("\n[+] Creating the vector space:") if self.debug else ''
		vsm   = VectorSpace(self.data.texts, method=options['--method'], debug=self.debug) 
		
		write("[+] Generating recommendations".ljust(54,'.')) if self.debug else ''
		rec_items = self.generate_rec(vsm)
		write("[OK]\n") if self.debug else ''
		
		write("[+] Saving to output file".ljust(54,'.')) if options['--debug'] else ''
		json.dump(rec_items, open(options['--output'], 'w'))
		write("[OK]\n")
		print "[x] Finished."
	
	def generate_rec(self, vsm):
			rec_items = []
			for i, item in enumerate(self.items):
				indices, scores = vsm.n_most_similar(i, N=int(options['--N'])) 
				rec = []
				rec_scores = []
				write("\n(id=%s)  %s \n" % (str(item['id']), item['title'])) if self.display else ''
				for j, idx in enumerate(indices):
					sim_item = self.data.items[idx]
					write("%d. %s (%.3f)\n" % (j+1, sim_item['title'], scores[j])) if self.display else ''
					rec.append(sim_item['id'])
					rec_scores.append("%.4f" % scores[j])
				rec_item = item
				rec_item['rec'] = rec
				rec_item['rec_scores'] = rec_scores 
				rec_items.append(rec_item)
			return rec_items


if __name__ == '__main__':
    options = docopt(__doc__, version='CBRec v1.0, NLP Group @ Idiap 2013')
    print options
    gen = Generator(options, items=None)
    gen.run()