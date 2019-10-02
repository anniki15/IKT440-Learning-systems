import os
import re
from pathlib import Path


### GLOBALS
newsgroup_folder = '20_newsgroups/'
category_folderS = os.listdir(newsgroup_folder)
vocabulary = set()
total_document_count = 0
prediction_testing_documents = list()
###

class Category:
    def __init__(self, name):
         self.name = name
         self.unique_words = set()
         self.unique_words_count = dict()
         self.word_probabilities = dict()
         self.documents_count = 0
         self.category_prob = 0

    def increment_document_count(self):
        self.documents_count += 1

    def increment_word_count(self, word):
        self.unique_words_count[word] += 1

    def add_word(self, word):
        self.unique_words.add(word)
        self.unique_words_count[word] = 1

    def has_word(self, word):
        return word in self.unique_words

    def set_category_probability(self, total_document_count):
        self.category_prob = self.documents_count / total_document_count

    # def set_word_probabilities(self):
    #     self.word_probabilities = dicself.

    # def set_prob(self, ):

categories = dict()

#Cleaning the file. Removing everything above Lines:, and symbols and punctuation
#Improvment ideas:
#   Remove all lines that start with <word><:>
#remove first 20lines?
def clean_document(file):

    head, sep, tail = file.partition('Lines:')
    tail_lower = tail.lower()

    t = ''
    for line in tail_lower.splitlines():
        s = (re.sub(r'([^\s\w]|_)+', u' ', line.replace('\n', ' ').replace('\t', ' ')))
        t += s + ' '

    return t


for category_folder in category_folderS:

    category_documentS = os.listdir(newsgroup_folder + category_folder)

    two_thirds_of_documents = len(category_documentS) // 3 * 2 + 1

    categories[category_folder] = Category(category_folder)

    #iterate the first 2/3 of the documents per category
    for doc_name in category_documentS[:two_thirds_of_documents]:
        total_document_count += 1

        absolute_document_path = Path(newsgroup_folder) / category_folder / doc_name

        with open(absolute_document_path) as f:
            f = f.read()

            f = clean_document(f) # Remove headers, split on 'lines:'

            categories[category_folder].increment_document_count()

            for word in f.split():

                vocabulary.add(word) #add word to vocabulary. set data type ensures distinct words

                #add to category dict, or increment count
                if categories[category_folder].has_word(word):
                    categories[category_folder].increment_word_count(word)
                else:
                    categories[category_folder].add_word(word)
    for doc_name in category_documentS[two_thirds_of_documents:]:
        pass

print(vocabulary)
print(categories)


for c in categories.values():
    c.set_category_probability(total_document_count)
    # categories[category_path] = Category(category_path)
    # print(vocabulary)
    # print(categories)


    # with open(e) as f:
    #     data = f.read()
    #     # data2 = data.split()
    #     print(data)


