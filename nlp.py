import pandas as pd

df_res = pd.read_excel('akipress_fertig.xlsx')

X = df_res['text_prep']
Y = df_res['topic']
topics = ["Культура", "Аналитика", "Спорт"]

from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, random_state=42)

# Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()),
               ])

nb.fit(X_train, Y_train)
Y_pred = nb.predict(X_test)

print("-======================Naive Bayes Classifier======================-")

print('accuracy %s' % accuracy_score(Y_pred, Y_test))
print(classification_report(Y_test, Y_pred, target_names=topics))

print("-======================Naive Bayes Classifier======================-")

print()
print()
# Linear Support Vector Machine
from sklearn.linear_model import SGDClassifier

sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                ])
sgd.fit(X_train, Y_train)
Y_sgd_pred = sgd.predict(X_test)

print("-===================Linear Support Vector Machine===================-")

print('accuracy %s' % accuracy_score(Y_sgd_pred, Y_test))
print(classification_report(Y_test, Y_sgd_pred, target_names=topics))

print("-===================Linear Support Vector Machine===================-")

print()
print()

# Logistic Regression
from sklearn.linear_model import LogisticRegression

logreg = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                   ])
logreg.fit(X_train, Y_train)
Y_logreg_pred = logreg.predict(X_test)

print("-========================Logistic Regression========================-")

print('accuracy %s' % accuracy_score(Y_logreg_pred, Y_test))
accuracy = accuracy_score(Y_logreg_pred, Y_test)
print(classification_report(Y_test, Y_logreg_pred, target_names=topics))

print("-========================Logistic Regression========================-")

print()
print()
