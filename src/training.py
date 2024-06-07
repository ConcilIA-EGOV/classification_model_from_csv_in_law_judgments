from joblib import dump, load
import json
import numpy as np
###
import sys
import os

# Obtém o diretório atual do script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Adiciona o diretório base do projeto ao caminho de busca do Python
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
###
from util.parameters import FILE_PATH, CV, BEST_SCORE_STORAGE
from util.parameters import NUM_EPOCHS, MAIN_MODEL_FILE
from formatation.input_formatation import load_data, separate_features_labels
from src.preprocessing import preprocessing, split_train_test
############################
from sklearn.calibration import LinearSVC
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report


def train_model(model, X_train, y_train):
    """
    Treinar o modelo usando o conjunto de treino.
    Se o modelo já estiver treinado, o treinamento será incrementado.
    """    
    if hasattr(model, "partial_fit"):
        # Se o modelo suporta treinamento incremental, use partial_fit
        model.partial_fit(X_train, y_train, classes=np.unique(y_train))
    else:
        # Caso contrário, use fit normal
        model.fit(X_train, y_train)
        
    return model


def test_model(model, X, y):
    '''
    Testar o modelo usando o conjunto de teste
    '''
    score = classification_report(y, model.predict(X), output_dict=True)
    return score


def save_model(model, score):
    """
    Salvar o modelo treinado em um arquivo e o score em outro
    """
    dict_score = {"best_score": score}
    json.dump(dict_score, open(BEST_SCORE_STORAGE, "w"))
    dump(model, MAIN_MODEL_FILE)
    return


def print_results(cv_score, epoch):
    print(f"Epoch {epoch + 1}/{NUM_EPOCHS}")
    prt_cv = " - ".join([f"{(score)*100:.2f}%" for score in cv_score])
    print(f"Cross Validation Scores: {prt_cv}")
    print(f"Cross Validation Mean: {(cv_score.mean())*100:.2f}%\n")


# Função principal para executar o pipeline
def main():
    # Passo 1: Carregar os dados do CSV
    data = load_data(FILE_PATH)
    if data is None:
        print("Erro ao carregar os dados!")
        return
    
    # Passo 2: Separar features (X) dos labels (Y)
    X, y = separate_features_labels(data)
    
    # Passo 3: Pré-processar os dados
    X = preprocessing(X)

    # Passo 4: Dividir em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    
    # Passo 5: Inicializar o modelo de Classificação
    # model = load(MAIN_MODEL_FILE)
    # model = LinearSVC(dual=True, max_iter=10000, tol=1e-3)
    # model = KNeighborsClassifier()
    # model = SVC()
    model = GradientBoostingClassifier()

    best_acc = json.load(open(BEST_SCORE_STORAGE, "r"))["best_score"]
    for epoch in range(NUM_EPOCHS):
        # Passo 6: Treinar o modelo
        train_model(model, X_train, y_train)
        
        # Passo 7: Testar o modelo usando o conjunto de teste
        score = test_model(model, X_test, y_test)

        # Passo 8: Salvar o melhor modelo
        if score > best_acc:
            best_acc = score
            save_model(model, score)
            print_results(score, epoch)


# Chamando a função principal para treinar o modelo
if __name__ == "__main__":
    main()
