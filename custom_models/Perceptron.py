from sklearn.linear_model import Perceptron as pcn
from util.parameters import NUM_EPOCHS
import numpy as np


PARAMS = {
    "penalty": "elasticnet",
    "alpha": 0.0001,
    "l1_ratio": 0.75,
    "fit_intercept": True,
    "max_iter": 10000,
    "tol": 0.001,
    "shuffle": True,
    "eta0": 1.0,
    "n_jobs": -1,
    "random_state": 200,
    "early_stopping": True,
    "validation_fraction": 0.2,
    "n_iter_no_change": 10,
    "class_weight": None,
    "warm_start": False
}


class Perceptron(pcn):
    def __init__(self, penalty="elasticnet", alpha=0.0001, l1_ratio=0.75,
                 fit_intercept=True, max_iter=10000, tol=0.001, shuffle=True,
                 eta0=1.0, n_jobs=-1, random_state=200, early_stopping=True,
                 validation_fraction=0.2, n_iter_no_change=10, class_weight=None,
                 warm_start=False):
        try: 
            super().__init__(penalty=penalty, alpha=alpha, l1_ratio=l1_ratio,
                             fit_intercept=fit_intercept, max_iter=max_iter, tol=tol,
                             shuffle=shuffle, eta0=eta0, n_jobs=n_jobs, random_state=random_state,
                             early_stopping=early_stopping, validation_fraction=validation_fraction,
                             n_iter_no_change=n_iter_no_change, class_weight=class_weight,
                             warm_start=warm_start)
        except Exception as e:
            print(f"Erro ao instanciar o modelo Perceptron: {e}")
            super().__init__(**PARAMS)
        self.name = "Perceptron"
    
    def fit(self, X, y):
        output = self
        try:
            classes = np.unique(y)
            output = super().fit(X, y)
            for _ in range(NUM_EPOCHS):
                output.partial_fit(X, y, classes=classes)
        except Exception as e:
            print(f"Erro ao treinar o modelo {self.name}: {e}")
        return output
