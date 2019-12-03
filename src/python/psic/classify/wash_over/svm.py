import random

from sklearn import svm
from sklearn.model_selection import cross_val_score

from psic.classify.wash_over.prepare_washover import get_washover_data

X, y = get_washover_data()

SEED = 405
random.seed = SEED

clf = svm.SVC(kernel='linear', C=1, random_state=SEED, verbose=True)
scores = cross_val_score(clf, X, y, cv=10, verbose=True)
print(clf)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
