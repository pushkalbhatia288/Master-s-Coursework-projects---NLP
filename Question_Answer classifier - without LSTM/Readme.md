APPROACH:
The problem statement asks us to do a classification task, where a list of sentences is given. The sentences are to be classified into Questions/No Questions (Binary classification).
How I dealt with this is to think of this as a Question detection task. By saying so, I mean that with the use of heuristics and Machine Learning, I try to find if a given sentence has some features that tells me if it is a question or not.
I used Machine learning too because only heuristic based learning makes the model very stiff.

DATA: 
1. For this problem I was provided only with the testing unlabeled data. Since the evaluation is to be done on this et, I did not take any of these sentences for the classification task (Training). 
2. Therefore, I decided to create my own data. I had many datasets available for Q/A datasets, but I needed particularly questions and proper sentences which are not questions (Q/A datasets usually had incomplete sentences for the ones that were not questions, since they were random answers). 
3. So, I took a set of questions(1000) from http://cogcomp.org/Data/QA/QC/train_1000.label, which had 1000 questions of different types. Then I searched for a list of sentences which gave me data for sentences that were not questions. 
4. I did little preprocessing, just to get these as simple questions and not questions. I also created a labels file for the same. This gave me the training data I needed (20:80 for test:train).

FEATURE ENGINEERING:
On research I found out that there are some heuristics that help us understand that a sentence is a question. (Particular formats, presence of certain words etc) I have included these heuristics as features for my classification model (I have used svm for this task).
Some of them that i have used are as follows:
1. Presence of a wh word.
These are words such as what, where, when, how, who whose presence makes a strong feature for a question. however, that is not always true, and therefore we needed more features.
2. Presence of a wh word with the next word being "VERB".
For this I used Spacy POS tagging, using the in-built model "en_core_web_sm". With this I tagged each word of the sentence and checked for the same.
3. Presence of a wh word and the third word being a "VERB"
Again I tried to do the same thing as above and provided it as a feature.
**Note: I did not do trigrams/bigrams for the whole sentence since I did not need the other trigrams in the sentence. Instead I just checked for the token, and the corresponding word on the required index (2nd or 3rd). Spacy does it for us, so it gets easy.
4. Presence of Verb at the start of the sentence like is, are etc. and the third word's POS tag.
Again, this is another important feature for certain types of questions.
5. Presence of a question mark.
Though I know that a lot of text did not have questions, but I used this as an important feature. Also, to make sure I had enough cases in my training set which did not have question marks.

TRIED BUT NOT INCLUDED:
I tried a lot of time to generate a feature by parsing the sentence and generating it's tree. Then I though to add that as another feature. But it was complicated and I couldn't run it. The complications were related to install Stanford parser, downloading its jar which was unsuccessful.
What would this feature have done?
This feature would have further provided us correct results for some cases that we are still missing. that is so because questions have a certain format which can be detected by the tree structure. Also stanford parser provided us with certain tags (SBARQ and SQ) that tells us that the sentance is a question.


After training with my own created data and finding accuracy on my test data, I predicted/classified the results for the data that is given to me.

FILES INCLUDED: 
data_to_train: self created trainning data
data_lables: self created labels for training data
test_inputs: Actual file to be tested (evaluated)
output_results: file with predicted labels for actual data(test_inputs)
Question_classiciation.py: Python file with code
preprocess.py: small code for little preprocessing and creating data
