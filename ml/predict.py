# ==========================================
# BUGRADAR ML PREDICTION
# ==========================================

import argparse

from analyzer.ast_parser import (
    analyze_code
)

from analyzer.code_reader import (
    read_file
)

from ml.model import (
    load_model,
    predict_risk
)


# ==========================================
# PREDICT FILE
# ==========================================

def predict_file(
    file_path,
    model_path="models/bug_risk_model.joblib"
):

    code = read_file(
        file_path
    )


    ast_report = analyze_code(
        code
    )


    model = load_model(
        model_path
    )


    prediction = predict_risk(

        ast_report,

        model=model
    )


    return prediction


# ==========================================
# DISPLAY PREDICTION
# ==========================================

def display_prediction(
    file_path,
    prediction
):

    print()

    print(
        "========================================"
    )

    print(
        "       BUGRADAR ML PREDICTION"
    )

    print(
        "========================================"
    )

    print()

    print(
        "File:",
        file_path
    )

    print(
        "Predicted Risk:",
        prediction[
            "prediction"
        ]
    )

    print(
        "Confidence:",
        prediction[
            "confidence"
        ],
        "%"
    )

    print()

    print(
        "Risk Probabilities"
    )

    print(
        "----------------------------------------"
    )


    for risk_level, probability in (
        prediction[
            "probabilities"
        ].items()
    ):

        print(

            f"{risk_level:<10} : "
            f"{probability}%"

        )


    print()

    print(
        "========================================"
    )


# ==========================================
# MAIN
# ==========================================

def main():

    parser = argparse.ArgumentParser(

        description=(
            "BugRadar ML risk prediction"
        )
    )


    parser.add_argument(

        "file",

        nargs="?",

        default="examples/sample.cpp",

        help=(
            "C/C++ source file to analyze"
        )
    )


    parser.add_argument(

        "--model",

        default=(
            "models/bug_risk_model.joblib"
        ),

        help=(
            "Path to trained BugRadar model"
        )
    )


    args = parser.parse_args()


    prediction = predict_file(

        args.file,

        args.model
    )


    display_prediction(

        args.file,

        prediction
    )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()