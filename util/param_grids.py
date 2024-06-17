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

param_grid_KNN = {
    'n_neighbors': [10, 30, 50],
    'weights': ['uniform', 'distance'],
    'algorithm': ['ball_tree', 'kd_tree', 'brute'],
    'leaf_size': [30, 60, 100],
    'p': [1, 2],  # 1 for Manhattan distance, 2 for Euclidean distance
    'metric': ['minkowski', 'euclidean', 'manhattan', 'chebyshev', 'hamming'],
    'metric_params': [None],
    'n_jobs': [-1]
}

param_grid_SVC = {
    'C': [10, 50, 100],
    'kernel': ['poly', 'rbf', 'sigmoid'],
    'degree': [2, 3, 4, 5],
    'gamma': [0.5, 1, 2],
    'coef0': [0.0, 0.5, 1],
    'shrinking': [True, False],
    'probability': [True, False],
    'tol': [1e-4, 1e-3, 1e-5],
    'cache_size': [100, 200, 300],
    'class_weight': [None, 'balanced'],
    'verbose': [False],  # Geralmente mantido False para evitar log excessivo
    'max_iter': [10],  # -1 para sem limite
    'decision_function_shape': ['ovr'],
    'break_ties': [False],
    'random_state': [None, 42, 100]
}

param_grid_GB = {
    'loss': ['log_loss', 'exponential'],
    'learning_rate': [0.05, 0.1, 0.2],
    'n_estimators': [50, 100, 200],
    'subsample': [0.8, 1.0],
    'criterion': ['friedman_mse', 'squared_error'],
    'min_samples_split': [0.5, 1, 2, 10],
    'min_samples_leaf': [0.5, 1, 10, 50],
    'min_weight_fraction_leaf': [0.0, 0.2, 0.5],
    'max_depth': [1, 5, 10],
    'min_impurity_decrease': [0.0, 0.1, 0.5],
    'init': [None],  # ou uma instância de estimador, geralmente None
    'random_state': [42, 100, 200],  # valores comuns para garantir replicabilidade
    'verbose': [False],  # Geralmente mantido False para evitar log excessivo
    'max_features': [None, 'sqrt', 'log2', 0.5, 2],
    'max_leaf_nodes': [None, 2, 10, 50],
    'warm_start': [True, False],
    'validation_fraction': [0.1, 0.2, 0.3],
    'n_iter_no_change': [None, 20],
    'tol': [1e-4, 1e-3, 1e-5],
    'ccp_alpha': [0.0, 0.05, 0.1]
}

param_grid_Perceptron = {
    'penalty': ['l2', 'l1', 'elasticnet', None],
    'alpha': [0.0001, 0.001, 0.01],
    'l1_ratio': [0.15, 0.5, 0.75],
    'fit_intercept': [True, False],
    'max_iter': [10],
    'tol': [0.001, 0.0001],
    'shuffle': [True, False],
    'eta0': [1.0, 0.5, 2],
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
    'KNN': param_grid_KNN,
    'SVC': param_grid_SVC,
    'GradientBoosting': param_grid_GB,
    'Perceptron': param_grid_Perceptron
}
