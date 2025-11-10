from flask import Flask, request, url_for, render_template, redirect, session
#from classifier import Classifier
from jinja2 import Template
import requests
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

#classifier libraries
import random
from textblob import TextBlob
#from nltk.corpus import stopwords
import stop_words
#from nltk import NaiveBayesClassifier
from textblob.classifiers import NaiveBayesClassifier

UPLOAD_FOLDER = 'C:/Users/saverio/Desktop/School/informatica/python/right/uploads/'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return 'This is the homepage'


@app.route('/classifier', methods=['GET','POST'])
def riservata():
    if request.method == 'GET':
        return render_template('classifier.html')
    if request.method == 'POST':
        messaggio = request.form.get('msg')
        #controllo sul file
        if 'browse' not in request.files:
            return "Nessun file"
        file = request.files['browse']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "Nessun file selezionato."
        if file:
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)

            """classifier = Classifier ()
            entire_data = classifier.importa(app.config['UPLOAD_FOLDER'] + filename) #in substitution of importa() method
            result = classifier.splitter(entire_data)
            ai = classifier.trainer(result)
            accuracy = classifier.check_accuracy(ai, result) #accuracy of the dataset needs to be printed
            spham = ai.classify(messaggio) #in substitution of classifica() method"""

            #GET_LIST_TUPLES------------------------------------
            read_file=app.config['UPLOAD_FOLDER'] + filename
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
                        if word not in stop_words.get_stop_words('en') and not word.isdigit():
                            list_tuples.append((word.lower(), tabsep[0]))
                    c += 1
                    if c == 500:
                        break

            #SPLITTER---------------------------------------------
            d = datetime.now()
            random.seed(d.second)
            random.shuffle(list_tuples)
            """ln = len(list_tuples) ->  se dovessimo "splittare" l'intero dataset
            m=int(ln*60/100)
            train = list_tuples[:m]
            test = list_tuples[m+1:ln]"""
            train = list_tuples[:360]
            test = list_tuples[361:600]  #a scopo dimostrativo, brevi tempi di attesa

            """train_example = [
                ('I love this sandwich.', 'pos'),
                ('This is an amazing place!', 'pos'),
                ('I feel very good about these beers.', 'pos'),
                ('This is my best work.', 'pos'),
                ("What an awesome view", 'pos'),
                ('I do not like this restaurant', 'neg'),
                ('I am tired of this stuff.', 'neg'),
                ("I can't deal with this", 'neg'),
                ('He is my sworn enemy!', 'neg'),
                ('My boss is horrible.', 'neg')
            ]"""

            #TRAINER----------------------------------------------
            cl = NaiveBayesClassifier(train)

            #CHECK_ACCURACY---------------------------------------
            accuracy = cl.accuracy(test)
            accuracy = int(accuracy*100)
            print accuracy

            #CLASSIFICATION---------------------------------------
            spham = cl.classify(messaggio)
            print messaggio
            #spham = cl.classify ("Hey buddy! How are you? I'm really thankful for your help. Take care!") #ham
            print spham

            cl.show_informative_features(10)


            return render_template('result.html', sphamm=spham,acc = accuracy)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
