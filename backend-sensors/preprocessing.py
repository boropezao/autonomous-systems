from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import numpy as np

scaler = StandardScaler()
scaler.mean_ = [
    69.86369863,
    10516.82808219,
    1515.46369863,
    1162.62671233,
    1057.42945205,
    472.98013699,
]
scaler.scale_ = [
    22.02013207,
    9977.84610545,
    525.30039356,
    386.4553223,
    438.55505717,
    213.73160808,
]
scaler.var_ = [
    4.84886216e02,
    9.95574129e07,
    2.75940503e05,
    1.49347716e05,
    1.92330538e05,
    4.56812003e04,
]


target = StandardScaler()
target.mean_ = [180921.19589041]
target.scale_ = [79415.29188607]
target.var_ = [6.30678859e09]

discrete_scaler = MinMaxScaler()
discrete_scaler.min_ = [-0.11111111, 0.0, -0.16666667, 0.0]
discrete_scaler.scale_ = [0.11111111, 0.25, 0.08333333, 0.33333333]

time_scaler = MinMaxScaler()
time_scaler.min_ = [-13.56521739, -32.5, -17.27272727]
time_scaler.scale_ = [0.00724638, 0.01666667, 0.00909091]

discrete_selected = ["overallQual", "garageCars", "totRmsAbvGrd", "fullBath"]
continuos_selected = [
    "lotFrontage",
    "lotArea",
    "grLivArea",
    "stFlrSF",
    "totalBsmtSF",
    "garageArea",
]
time_selected = ["yearBuilt", "yearRemodAdd", "garageYrBlt"]

ordinal_selected = ["bsmtQual", "exterQual", "kitchenQual", "fireplaceQu"]
nominal_selected = ["neighborhood", "msSubClass", "garageType", "garageFinish"]


def preprocess_input(data):

    continuos = []
    discrete = []
    time = []
    ordinal = []
    nominal = []

    # Transform discrete features
    for feature in discrete_selected:
        value = float(data.get(feature))
        discrete.append(value)

    if discrete:
        discrete = np.array(discrete).reshape(1, -1)
        discrete = discrete_scaler.transform(discrete).flatten()

    # Transform continuous features
    for feature in continuos_selected:
        value = float(data.get(feature))
        continuos.append(value)

    if continuos:
        continuos = np.array(continuos).reshape(1, -1)
        continuos = scaler.transform(continuos).flatten()

    # Transform time features
    for feature in time_selected:
        value = float(data.get(feature))
        time.append(value)

    if time:
        time = np.array(time).reshape(1, -1)
        time = time_scaler.transform(time).flatten()

    # Collect ordinal and nominal features
    for feature in ordinal_selected:
        ordinal.append(int(data.get(feature)))

    for feature in nominal_selected:
        nominal.append(int(data.get(feature)))

    # Concatenate all processed features
    input_data = np.concatenate((continuos, discrete, time, ordinal, nominal))
    input_data = input_data.reshape(1, -1)  # Reshape to

    return input_data


def inverse_result(prediction_result):
    return target.inverse_transform(prediction_result)
