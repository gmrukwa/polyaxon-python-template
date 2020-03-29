import argparse
import pickle
import os
import numpy as np
from polyaxon_helper import experiment
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from my_project.data import load_data


def model(X, y, n_estimators, max_features, min_samples_leaf):
    classifier = RandomForestClassifier(n_estimators=n_estimators,
                                        max_features=max_features,
                                        min_samples_leaf=min_samples_leaf)
    return cross_val_score(classifier, X, y, cv=5), classifier


parser = argparse.ArgumentParser()
parser.add_argument('--n_estimators', type=int, default=3)
parser.add_argument('--max_features', type=int, default=3)
parser.add_argument('--min_samples_leaf', type=int, default=80)
args = parser.parse_args()

# Polyaxon

experiment.log_params(n_estimators=args.n_estimators,
                      max_features=args.max_features,
                      min_samples_leaf=args.min_samples_leaf)

(X, y) = load_data()

# Polyaxon

experiment.log_data_ref(data=X, data_name='dataset_X')
experiment.log_data_ref(data=y, data_name='dataset_y')

accuracies, classifier = model(X=X,
                               y=y,
                               n_estimators=args.n_estimators,
                               max_features=args.max_features,
                               min_samples_leaf=args.min_samples_leaf)

accuracy_mean, accuracy_std = (np.mean(accuracies), np.std(accuracies))

# Polyaxon

experiment.log_metrics(accuracy_mean=accuracy_mean,
                       accuracy_std=accuracy_std)

outpath = os.path.join(experiment.get_outputs_path(), 'model.pkl')
with(open(outpath, 'wb')) as outfile:
    pickle.dump(classifier, outfile)