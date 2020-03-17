import json
import os
import pprint

import utils
from text_processing_utils import get_spans_and_words

FILE_IGNORE = set(['.DS_Store'])
VALID_FILE_EXTENSIONS = set(['json'])

class InvertedIndex():
	"""Class for an inverted index.
	
	Attributes:
		documents (str): filepaths to all indexed documents
		postings (dict of posting): contains postings. a posting is a dictionary
									from document to line number.

	"""
	def __init__(self, filepath):
		# Get documents
		documents = []
		for dirpath, dirnames, filenames in os.walk(filepath):
			for filename in filenames:
				if filename not in FILE_IGNORE and filename.split('.')[-1] in VALID_FILE_EXTENSIONS:
					documents.append(os.path.join(dirpath, filename))

		# Get postings
		title_postings = {}
		abstract_postings = {}
		body_postings = {}
		for document in documents:
			doc_dict = utils.load_file(document)
			biorxiv_document = IndexableDocument(doc_dict)

			# Index title, abstract, and body
			for postings_i, text in [(title_postings, biorxiv_document.title),
							  		(abstract_postings, biorxiv_document.abstract),
							  		(body_postings, biorxiv_document.body)]:
				for span, word in get_spans_and_words(text):
					if word in postings_i and document in postings_i[word]:
						postings_i[word][document].append(span)
					else:
						postings_i[word] = {document: [span]}

		self.documents = documents
		self.board = {   						# a board contains several postings
			'title_postings': title_postings,
			'abstract_postings': abstract_postings,
			'body_postings': body_postings
		}

		for postings_name, postings_i in self.board.items():
			print("Number of unique vocabulary words in %s: %s" % (postings_name, len(postings_i)))

	def search(self, word):
		result = {}
		for postings_name, postings in self.board.items():
			if word in postings:
				result[postings_name] = postings[word]
			else:
				result[postings_name] = None
		return result


class IndexableDocument():
	def __init__(self, doc_dict):
		self.id = doc_dict['paper_id']
		self.title = doc_dict['metadata']['title']
		self.authors = utils.format_authors(doc_dict['metadata']['authors'])
		self.authors_with_affiliation = utils.format_authors(doc_dict['metadata']['authors'], with_affiliation=True)
		self.abstract = utils.format_body(doc_dict['abstract'])
		self.body = utils.format_body(doc_dict['body_text'])
		self.bib_entries = utils.format_bib(doc_dict['bib_entries'])
		self.original_item = json.loads(json.dumps(doc_dict))

	def __repr__(self):
		return pprint.pformat({
			'id': self.id,
			'title': self.title,
			'authors': self.authors,
			'abstract': self.abstract,
			'body': self.body
		})


if __name__ == "__main__":
	filepath = '/Users/jinpark/data/cord19-dataset/biorxiv_medrxiv/biorxiv_medrxiv-subset'
	inverted_index = InvertedIndex(filepath)
	print("Search 'antibody': %s" % inverted_index.search('antibody'))
