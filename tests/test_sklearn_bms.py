import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from autora_bms.skl.bms import BMSRegressor

warnings.filterwarnings("ignore")


def generate_noisy_constant_data(
    const: float = 0.5, epsilon: float = 0.01, num: int = 1000, seed: int = 42
):
    X = np.expand_dims(np.linspace(start=0, stop=1, num=num), 1)
    y = np.random.default_rng(seed).normal(loc=const, scale=epsilon, size=num)
    return X, y, const, epsilon


def test_constant_model():
    X, y, const, epsilon = generate_noisy_constant_data()
    for x in X:
        print(x)
        if x[0] == 0.0:
            x[0] = 0.001
    print(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    estimator = BMSRegressor(epochs=30)
    assert estimator is not None
    estimator.fit(X_train, y_train)
    # print(X_train)
    # print(estimator.model_)
    # print(estimator.predict(X_test))


def test_weber_model():
    raw_data = pd.read_csv("../example/experiment_0_data.csv")

    X, y = raw_data[["S1", "S2"]], raw_data["difference_detected"]
    estimator = BMSRegressor(epochs=30)
    estimator.fit(X, y)
    # print(X_train)
    # print(estimator.model_)
    # print(estimator.predict(X_test))


if __name__ == "__main__":
    test_weber_model()
