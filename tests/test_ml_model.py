# ==========================================
# BUGRADAR ML MODEL TESTS
# ==========================================

from ml.model import (
    create_model,
    get_class_distribution,
    predict_features
)


# ==========================================
# TEST MODEL CREATION
# ==========================================

def test_create_model():

    model = create_model()


    assert model is not None


    assert (
        model.n_estimators
        ==
        200
    )


# ==========================================
# TEST CLASS DISTRIBUTION
# ==========================================

def test_class_distribution():

    labels = [

        "LOW",

        "MEDIUM",

        "HIGH",

        "LOW",

        "HIGH",

        "LOW"
    ]


    result = get_class_distribution(
        labels
    )


    assert (
        result["LOW"]
        ==
        3
    )


    assert (
        result["MEDIUM"]
        ==
        1
    )


    assert (
        result["HIGH"]
        ==
        2
    )


# ==========================================
# TEST MODEL PREDICTION
# ==========================================

def test_prediction():

    from sklearn.ensemble import (
        RandomForestClassifier
    )


    X = [

        [1, 1, 0, 0, 0, 0, 2, 3, 1, 2, 0, 0, 0, 1, 0, 0, 5, 1],

        [5, 10, 4, 3, 2, 8, 20, 30, 7, 15, 1, 2, 1, 8, 4, 2, 30, 5],

        [2, 4, 1, 1, 0, 1, 5, 8, 3, 6, 0, 1, 0, 3, 1, 0, 10, 2],

        [8, 15, 5, 4, 3, 10, 25, 40, 9, 20, 2, 3, 2, 10, 5, 3, 40, 8]
    ]


    y = [

        "LOW",

        "HIGH",

        "MEDIUM",

        "HIGH"
    ]


    model = RandomForestClassifier(

        n_estimators=20,

        random_state=42
    )


    model.fit(
        X,
        y
    )


    result = predict_features(

        X[0],

        model=model
    )


    assert (
        "prediction"
        in result
    )


    assert (
        "confidence"
        in result
    )


    assert (
        "probabilities"
        in result
    )


# ==========================================
# TEST PROBABILITIES
# ==========================================

def test_prediction_probabilities():

    from sklearn.ensemble import (
        RandomForestClassifier
    )


    X = [

        [1] * 18,

        [2] * 18,

        [3] * 18,

        [4] * 18,

        [5] * 18,

        [6] * 18
    ]


    y = [

        "LOW",

        "LOW",

        "MEDIUM",

        "MEDIUM",

        "HIGH",

        "HIGH"
    ]


    model = RandomForestClassifier(

        n_estimators=20,

        random_state=42
    )


    model.fit(
        X,
        y
    )


    result = predict_features(

        X[0],

        model=model
    )


    total_probability = sum(
        result[
            "probabilities"
        ].values()
    )


    assert (
        round(
            total_probability,
            2
        )
        ==
        100.00
    )


    assert (
        0
        <=
        result[
            "confidence"
        ]
        <=
        100
    )