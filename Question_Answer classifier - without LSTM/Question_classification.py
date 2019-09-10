import pandas as pd
import spacy
import nltk
from sklearn import svm
from nltk import pos_tag
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random
#from stanford_parser.parser import Parser  


class Question_classification:
	def __init__(self):
		self.data_file = open("data_to_train.txt", "r")
		self.labels_file = open("data_labels.txt", "r")
		self.labels = []
		for label in self.labels_file:
			self.labels.append(int(label))
		self.wh_words = {"what": 1, "where": 1, "who": 1, "which": 1, "when": 1, "how" : 1, "is" : 1, "are" : 1}
		self.verb_starters = {"is": 1, "are": 1, "can": 1, "would": 1, "could": 1, "can": 1, "will": 1}
		self.nlp = spacy.load('en_core_web_sm')


	def extract_features(self):
		self.feature_list = []
		for sentence in self.data_file:
			feature = []
			wh_start_word = 0
			wh_word = 0
			wh_with_word = 0
			question_mark = 0
			verb_start_with_pron = 0
			trigram_feature = 0
			doc = self.nlp(unicode(str(sentence).strip(), "utf-8"))
			for index, token in enumerate(doc):
				# Check wh word bigram
				if index == 0 and token.text.lower() in self.wh_words:
					wh_start_word = 1
				# Check wh word
				if token.text.lower() in self.wh_words:
					wh_word = 1
				# Check verb and pronoun bigram
				if index == 0 and doc[index].text.lower() in self.verb_starters and doc[index + 1].pos == "PRON":
					verb_start_with_pron = 1
				if index != len(doc)-1 and doc[index].text.lower() in self.wh_words and doc[index + 1].pos == "VERB":
					wh_with_word = 1
				# Check Question mark
				if (index == len(doc) - 1 and token.text == "?") or (index == len(doc) - 1 and token.text[-1] == "?"):
					question_mark = 1
				# Check current word and third word
				if index == 0 and len(doc) >= 3 and doc[index].text.lower() in self.verb_starters and doc[index + 2].pos == "VERB":
					trigram_feature = 1
			feature.append(wh_start_word)
			feature.append(wh_word)
			feature.append(wh_with_word)
			feature.append(verb_start_with_pron)
			feature.append(question_mark)
			feature.append(trigram_feature)
			#print len(feature)
			self.feature_list.append(feature)

		print len(self.feature_list)
		print len(self.labels)

	def test_accuracy(self, X, y):
		X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.20)
		self.clf = svm.SVC(gamma='auto')
		self.clf.fit(X_train, y_train)
		predicted = self.clf.predict(X_test)
		print "Test Accuracy after training: ", accuracy_score(y_test, predicted)


	def training(self):
		shuffle_data = list(zip(self.feature_list, self.labels))
		random.shuffle(shuffle_data)
		X, y = zip(*shuffle_data)
		self.test_accuracy(X, y)


	def predict_question(self):
		test_inputs = open("test_inputs.txt", "r")
		output_results = open("output_results.txt", "w+")
		for line in test_inputs:
			feature_list = []
			feature = []
			wh_start_word = 0
			wh_word = 0
			wh_with_word = 0
			question_mark = 0
			verb_start_with_pron = 0
			trigram_feature = 0
			doc = self.nlp(unicode(str(line).strip(), "utf-8"))
			for index, token in enumerate(doc):
				if index == 0 and token.text.lower() in self.wh_words:
					wh_start_word = 1
				if token.text.lower() in self.wh_words:
					wh_word = 1
				if index == 0 and doc[index].text.lower() in self.verb_starters and doc[index + 1].pos == "PRON":
					verb_start_with_pron = 1
				if index != len(doc) - 1 and doc[index].text.lower() in self.wh_words and doc[index + 1].pos == "VERB":
					wh_with_word = 1
				if (index == len(doc) - 1 and token.text == "?") or (index == len(doc) - 1 and token.text[-1] == "?"):
					question_mark = 1
				if index == 0 and len(doc) >= 3 and doc[index].text.lower() in self.verb_starters and doc[index+2].pos == "VERB":
					trigram_feature = 1
			feature.extend([wh_start_word, wh_word, wh_with_word, verb_start_with_pron, question_mark, trigram_feature])
			feature_list.append(feature)
			output_results.write(str(self.clf.predict(feature_list)[0]) + "\n")

	# def syntactic_parse(self):
	# 	pattern = """NP: {<DT>?<JJ>*<NN>} VBD: {<VBD>} IN: {<IN>}"""
	# 	NPChunker = nltk.RegexpParser(pattern)
	# 	result = NPChunker.parse(pos_tag("Hello How are you doing"))
	# 	print result

def main():
    question_classification = Question_classification()
    question_classification.extract_features()
    question_classification.training()
    question_classification.predict_question()
    #question_classification.syntactic_parse()

    list_of_wrong_output = ["Am i the best", "Am i the best?"]

main()
