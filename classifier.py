# Author: Saverio Catania
# website: ///
import random
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier


class Classifier:
    def get_list_tuples(read_file):
        list_tuples = []
        with open(read_file, "r") as r:
            c = 0
            for line in r:
                tabsep = line.strip().split('\t')
                msg = TextBlob(tabsep[1])
                try:
                    words = msg.words
                except:
                    continue
                for word in words:
                    if word not in stopwords.words() and not word.isdigit():
                        list_tuples.append((word.lower(), tabsep[0]))
                c += 1
                if c == 500:
                    break
        return list_tuples

    def importa(path):
        entire_data = Classifier.get_list_tuples(path)
        return entire_data

    def splitter(entire_data):
        random.seed(1)
        random.shuffle(entire_data)
        train = entire_data[:250]
        test = entire_data[251:500]
        result = []
        result.append(train)
        result.append(test)
        return result

    def trainer(result):
        train = result[0]
        cl = NaiveBayesClassifier(train)
        return cl

    def check_accuracy(cl, result):
        test = result[1]
        accuracy = cl.accuracy(test)
        return accuracy

    def classifica(body, cl):
        return cl.classify(body)
