# ==========================================
# BUGRADAR MACHINE LEARNING MODEL
# ==========================================

import csv
import os

import joblib

from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from sklearn.model_selection import (
    train_test_split
)

from ml.features import (
    FEATURE_NAMES
)


# ==========================================
# PATHS
# ==========================================

DATASET_PATH = (
    "data/training_data.csv"
)

MODEL_PATH = (
    "models/bug_risk_model.joblib"
)


# ==========================================
# LOAD DATASET
# ==========================================

def load_dataset(
    dataset_path=DATASET_PATH
):

    X = []

    y = []


    with open(
        dataset_path,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file
        )


        for row in reader:

            features = []


            for feature_name in (
                FEATURE_NAMES
            ):

                value = float(
                    row[
                        feature_name
                    ]
                )

                features.append(
                    value
                )


            X.append(
                features
            )

            y.append(
                row[
                    "risk_label"
                ]
            )


    return X, y


# ==========================================
# CREATE MODEL
# ==========================================

def create_model():

    return RandomForestClassifier(

        n_estimators=200,

        max_depth=12,

        min_samples_split=4,

        random_state=42,

        class_weight="balanced"
    )


# ==========================================
# CLASS DISTRIBUTION
# ==========================================

def get_class_distribution(
    labels
):

    distribution = {}


    for label in labels:

        distribution[label] = (
            distribution.get(
                label,
                0
            )
            + 1
        )


    return distribution


# ==========================================
# TRAIN MODEL
# ==========================================

def train_model(
    dataset_path=DATASET_PATH,
    model_path=MODEL_PATH
):

    X, y = load_dataset(
        dataset_path
    )


    if len(X) < 20:

        raise ValueError(
            "Training dataset must contain "
            "at least 20 samples."
        )


    if len(X) != len(y):

        raise ValueError(
            "Feature and label counts "
            "do not match."
        )


    class_distribution = (
        get_class_distribution(
            y
        )
    )


    if len(
        class_distribution
    ) < 2:

        raise ValueError(
            "Dataset must contain at "
            "least two risk classes."
        )


    can_stratify = all(

        count >= 2

        for count in (
            class_distribution.values()
        )
    )


    if can_stratify:

        X_train, X_test, y_train, y_test = (
            train_test_split(

                X,

                y,

                test_size=0.20,

                random_state=42,

                stratify=y
            )
        )

    else:

        X_train, X_test, y_train, y_test = (
            train_test_split(

                X,

                y,

                test_size=0.20,

                random_state=42
            )
        )


    model = create_model()


    model.fit(
        X_train,
        y_train
    )


    predictions = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        predictions
    )


    report = classification_report(

        y_test,

        predictions,

        zero_division=0
    )


    model_directory = os.path.dirname(
        model_path
    )


    if model_directory:

        os.makedirs(
            model_directory,
            exist_ok=True
        )


    joblib.dump(
        model,
        model_path
    )


    return {

        "model": model,

        "accuracy": accuracy,

        "classification_report": report,

        "training_samples": len(
            X_train
        ),

        "testing_samples": len(
            X_test
        ),

        "model_path": model_path,

        "classes": list(
            model.classes_
        ),

        "class_distribution": (
            class_distribution
        )
    }


# ==========================================
# LOAD MODEL
# ==========================================

def load_model(
    model_path=MODEL_PATH
):

    if not os.path.exists(
        model_path
    ):

        raise FileNotFoundError(

            "BugRadar ML model not found.\n"

            f"Expected: {model_path}\n\n"

            "Run:\n"

            "python -m ml.dataset\n"

            "python -m ml.model"
        )


    return joblib.load(
        model_path
    )


# ==========================================
# PREDICT RISK FROM FEATURES
# ==========================================

def predict_features(
    features,
    model=None,
    model_path=MODEL_PATH
):

    if model is None:

        model = load_model(
            model_path
        )


    prediction = model.predict(
        [features]
    )[0]


    probabilities = (
        model.predict_proba(
            [features]
        )[0]
    )


    probability_map = {}


    for index, class_name in enumerate(
        model.classes_
    ):

        probability_map[
            class_name
        ] = round(

            float(
                probabilities[index]
            ) * 100,

            2
        )


    confidence = max(
        probabilities
    ) * 100


    return {

        "prediction": prediction,

        "confidence": round(
            float(
                confidence
            ),
            2
        ),

        "probabilities": (
            probability_map
        )
    }


# ==========================================
# PREDICT FROM AST REPORT
# ==========================================

def predict_risk(
    ast_report,
    model=None,
    model_path=MODEL_PATH
):

    from ml.features import (
        extract_features
    )


    features = extract_features(
        ast_report
    )


    return predict_features(

        features,

        model=model,

        model_path=model_path
    )


# ==========================================
# MAIN TRAINING PROGRAM
# ==========================================

def main():

    print()

    print(
        "========================================"
    )

    print(
        "       BUGRADAR ML TRAINING"
    )

    print(
        "========================================"
    )


    result = train_model()


    print()

    print(
        "Class Distribution:"
    )


    for label, count in (
        result[
            "class_distribution"
        ].items()
    ):

        print(
            " ",
            label,
            ":",
            count
        )


    print()

    print(
        "Training Samples:",
        result[
            "training_samples"
        ]
    )


    print(
        "Testing Samples:",
        result[
            "testing_samples"
        ]
    )


    print(
        "Classes:",
        result[
            "classes"
        ]
    )


    print(
        "Accuracy:",
        round(

            result[
                "accuracy"
            ] * 100,

            2

        ),
        "%"
    )


    print()

    print(
        "Classification Report"
    )

    print(
        "----------------------------------------"
    )

    print(
        result[
            "classification_report"
        ]
    )


    print(
        "Model Saved:",
        result[
            "model_path"
        ]
    )


    print()

    print(
        "========================================"
    )

    print(
        "       END OF ML TRAINING"
    )

    print(
        "========================================"
    )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()