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

from sklearn.externals import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier

from sklearn.pipeline import make_pipeline

import warnings
import datetime


classifier = MultinomialNB()
count_vectorizer = CountVectorizer()


def setup():
    warnings.filterwarnings("ignore")

    # load data
    path_to_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_data", "shuffled-full-set-hashed.csv")
    data = open(path_to_data_file, "r")

    rows = []
    labels = []

    # iterate through the file line by line
    # and store info
    for line in data:
        title = line.split(",")[0]
        words = line.split(",")[1]

        # append current document to rows
        rows.append({'words': words, 'class': title})
        labels.append(title)

    # create DataFrame
    data_frame = DataFrame(rows, index=labels)

    # fit the classifier to the term-document matrix
    counts = count_vectorizer.fit_transform(data_frame['words'].values)
    targets = data_frame['class'].values
    classifier.fit(counts, targets)


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
