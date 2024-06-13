###
import sys
import os
# Obtém o diretório atual do script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Adiciona o diretório base do projeto ao caminho de busca do Python
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
###
import numpy as np
import json
from sklearn.calibration import LinearSVC
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import Perceptron
# -----------
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from util.parameters import FILE_PATH, CV
from formatation.input_formatation import load_data, separate_features_labels
from src.preprocessing import preprocessing

def test_best_model(grid_search:GridSearchCV, X_test, y_test):
    '''
    Print the best parameters and best score
    '''
    print("Best parameters found: ", grid_search.best_params_)
    print("Best cross-validation score: {:.2f}".format(grid_search.best_score_))

    # Evaluate the best model on the test set
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

def grid_search(X_train, y_train, classifier, param_grid, cv_=5):

    # Realizar a busca em grade
    grid_search = GridSearchCV(estimator=classifier,
                               param_grid=param_grid,
                               scoring='accuracy',
                               cv=cv_, n_jobs=-1, refit=True)
    grid_search.fit(X_train, y_train)

    # Melhor combinação de hiperparâmetros
    best_params = grid_search.best_params_
    # Melhor score
    test_best_model(grid_search, X_train, y_train)
    return best_params


param_grid_LSVC = {
    'penalty': ['l1', 'l2'],
    'loss': ['squared_hinge', 'hinge'],
    'dual': ['auto'],  # 'l1' penalty is not supported with dual=False
    'tol': [1e-4, 1e-3, 1e-2],
    'C': [0.1, 1, 10],
    'multi_class': ['ovr', 'crammer_singer'],
    'fit_intercept': [True, False],
    'intercept_scaling': [0.1, 1.0, 5.0],
    'class_weight': [None, 'balanced'],  # or a dictionary {class_label: weight}
    'verbose': [0],
    'random_state': [None, 42, 100],  # values for reproducibility
    'max_iter': [1000]
}

param_grid_SVC = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
    'degree': [2, 3, 4, 5],
    'gamma': ['scale', 'auto', 0.001, 0.1, 1],
    'coef0': [0.0, 0.1, 0.5, 1],
    'shrinking': [True, False],
    'probability': [True, False],
    'tol': [1e-4, 1e-3, 1e-2],
    'cache_size': [200, 500, 1000],
    'class_weight': [None, 'balanced'],
    'verbose': [False],  # Geralmente mantido False para evitar log excessivo
    'max_iter': [-1],  # -1 para sem limite
    'decision_function_shape': ['ovo', 'ovr'],
    'break_ties': [True, False],
    'random_state': [None, 42, 100]
}

param_grid_GB = {
    'loss': ['log_loss', 'exponential'],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'n_estimators': [100, 300, 500],
    'subsample': [0.6, 0.8, 1.0],
    'criterion': ['friedman_mse', 'squared_error', 'mae'],
    'min_samples_split': [2, 50, 500],
    'min_samples_leaf': [1, 10, 100, 1000],
    'min_weight_fraction_leaf': [0.0, 0.1, 0.2],
    'max_depth': [None],
    'min_impurity_decrease': [0.0, 0.01, 0.05, 0.1],
    'init': [None],  # ou uma instância de estimador, geralmente None
    'random_state': [42, 100, 200],  # valores comuns para garantir replicabilidade
    'verbose': [False],  # Geralmente mantido False para evitar log excessivo
    'max_features': [None, 'sqrt', 'log2', 0.5],
    'max_leaf_nodes': [None, 10, 50, 100],
    'warm_start': [True, False],
    'validation_fraction': [0.1, 0.2, 0.3],
    'n_iter_no_change': [None, 20],
    'tol': [1e-4, 1e-3, 1e-2],
    'ccp_alpha': [0.0, 0.01, 0.1]
}

param_grid_Perceptron = {
    'penalty': ['l2', 'l1', 'elasticnet', None],
    'alpha': [0.0001, 0.001, 0.01],
    'l1_ratio': [0.15, 0.5, 0.75],
    'fit_intercept': [True, False],
    'max_iter': [1000, 2000],
    'tol': [0.001, 0.0001],
    'shuffle': [True, False],
    'eta0': [1.0, 0.1, 0.01],
    'n_jobs': [-1],
    'random_state': [0, 42, 100],
    'early_stopping': [False, True],
    'validation_fraction': [0.1, 0.2],
    'n_iter_no_change': [5, 10],
    'class_weight': [None, 'balanced'],
    'warm_start': [False, True]
}

param_grid = {
    'LinearSVC': param_grid_LSVC,
    'SVC': param_grid_SVC,
    'GradientBoosting': param_grid_GB,
    'Perceptron': param_grid_Perceptron
}


models = {
    'LinearSVC': LinearSVC(),
    'SVC': SVC(),
    'GradientBoosting': GradientBoostingClassifier(),
    'Perceptron': Perceptron()
}

if __name__ == "__main__":
    data = load_data(FILE_PATH)
    X, y = separate_features_labels(data)
    X = preprocessing(X)
    best_params_all = dict()
    for key, model in models.items():
        print(f"Testing {key}")
        try:
            best_params_all[key] = grid_search(X, y, model, param_grid[key], CV)
            json.dump(best_params_all[key], open("studies/best_parameters__"+key+".txt", "w"))
        except Exception as e:
            print(f"Error in {key}")
            print(e)
            best_params_all[key] = e
            json.dump(best_params_all[key], open("studies/best_parameters__"+key+".txt", "w"))
    
    json.dump(best_params_all, open("studies/best_parameters.txt", "w"))
    
