from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import json

import os, sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


import warnings
import datetime


# Help with Scikit stuff from http://zacstewart.com/2015/04/28/document-classification-with-scikit-learn.html


classifier = MultinomialNB()
count_vectorizer = CountVectorizer()


def setup():
    warnings.filterwarnings("ignore")

    # open data file
    path_to_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_data", "shuffled-full-set-hashed.csv")
    data = open(path_to_data_file, "r")

    # initialize arrays for loading data
    rows = []
    labels = []

    # iterate through the file line by line
    # to build the dataframe
    for line in data:
        title = line.split(",")[0]
        words = line.split(",")[1]

        # append current document to rows
        rows.append({'words': words, 'class': title})
        labels.append(title)

    print("building dataframe")
    sys.stdout.flush()
    # create DataFrame
    data_frame = DataFrame(rows, index=labels)
    # shuffle dataset
    #data_frame = data_frame.reindex(np.random.permutation(data_frame.index))

    print("dataframe built, extracting features")
    sys.stdout.flush()

    # extract features
    counts = count_vectorizer.fit_transform(data_frame['words'].values)
    targets = data_frame['class'].values

    print("extracted features, training classifier")
    sys.stdout.flush()

    # train classifier
    classifier.fit(counts, targets)

    print("ready")
    sys.stdout.flush()


def index(request):
    return render(request, 'home.html', {})


@api_view(["POST"])
@permission_classes((AllowAny, ))
def get_prediction(request):
    words = request.data['words']

    # predict document type
    test_count = count_vectorizer.transform([words])
    prediction = classifier.predict(test_count)

    return HttpResponse("This is a " + str(prediction))



setup()
