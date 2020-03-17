import os

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
		postings = {}
		for document in documents:
			with open(document) as f:
				lines_of_words = self._parse_document(f.read())
				for i, words in enumerate(lines_of_words):
					for word in words:
						if word in postings and document in postings[word]:
							postings[word][document].append(i)
						else:
							postings[word] = {document: [i]}

		self.documents = documents
		self.postings = postings

		print("Number of unique vocabulary words: %s" % len(self.postings))

	def _parse_document(self, document_contents):
		"""Parses document contents.

		Args:
			document_contents (str): contents of a document

		Returns:
			parsed_contents (str): list of parsed words
		"""
		document_contents = document_contents.replace('(', ' ')
		document_contents = document_contents.replace(')', ' ')
		document_contents = document_contents.replace(':', ' ')
		
		lines = document_contents.split('\n')
		lines_of_words = [line.split() for line in lines]
		return lines_of_words

	def search(self, word):
		if word in self.postings:
			return self.postings[word]
		return None

filepath = '/Users/jinpark/data/cord19-dataset/biorxiv_medrxiv/biorxiv_medrxiv-subset'
inverted_index = InvertedIndex(filepath)
print("Search 'Terrance': %s" % inverted_index.search('Comparisons'))

