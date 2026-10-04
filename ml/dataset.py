# ==========================================
# BUGRADAR ML DATASET GENERATOR
# ==========================================

import csv
import os
import random

from ml.features import (
    FEATURE_NAMES
)


# ==========================================
# DATASET PATH
# ==========================================

DATASET_PATH = (
    "data/training_data.csv"
)


# ==========================================
# RANDOM SEED
# ==========================================

RANDOM_SEED = 42


# ==========================================
# DATASET SIZE
# ==========================================

DEFAULT_SAMPLES = 1000


# ==========================================
# GENERATE RANDOM FEATURE VALUES
# ==========================================

def generate_sample():

    functions = random.randint(
        1,
        15
    )

    if_statements = random.randint(
        0,
        20
    )

    for_loops = random.randint(
        0,
        8
    )

    while_loops = random.randint(
        0,
        6
    )

    switch_statements = random.randint(
        0,
        4
    )

    case_statements = random.randint(
        0,
        12
    )

    function_calls = random.randint(
        0,
        30
    )

    variable_declarations = random.randint(
        1,
        40
    )

    max_nesting_depth = random.randint(
        0,
        10
    )

    cyclomatic_complexity = random.randint(
        1,
        25
    )

    syntax_errors = random.randint(
        0,
        3
    )

    classes = random.randint(
        0,
        5
    )

    structs = random.randint(
        0,
        4
    )

    return_statements = random.randint(
        0,
        15
    )

    break_statements = random.randint(
        0,
        8
    )

    continue_statements = random.randint(
        0,
        5
    )

    operator_count = random.randint(
        1,
        60
    )

    include_count = random.randint(
        0,
        10
    )


    return {

        "functions": functions,

        "if_statements": if_statements,

        "for_loops": for_loops,

        "while_loops": while_loops,

        "switch_statements": switch_statements,

        "case_statements": case_statements,

        "function_calls": function_calls,

        "variable_declarations": (
            variable_declarations
        ),

        "max_nesting_depth": (
            max_nesting_depth
        ),

        "cyclomatic_complexity": (
            cyclomatic_complexity
        ),

        "syntax_errors": syntax_errors,

        "classes": classes,

        "structs": structs,

        "return_statements": (
            return_statements
        ),

        "break_statements": (
            break_statements
        ),

        "continue_statements": (
            continue_statements
        ),

        "operator_count": (
            operator_count
        ),

        "include_count": include_count
    }


# ==========================================
# CALCULATE SYNTHETIC RISK
# ==========================================

def calculate_risk_score(
    sample
):

    score = 0


    score += (
        sample[
            "cyclomatic_complexity"
        ] * 2.5
    )


    score += (
        sample[
            "max_nesting_depth"
        ] * 5
    )


    score += (
        sample[
            "if_statements"
        ] * 1.5
    )


    score += (
        sample[
            "for_loops"
        ] * 2
    )


    score += (
        sample[
            "while_loops"
        ] * 2.5
    )


    score += (
        sample[
            "function_calls"
        ] * 0.8
    )


    score += (
        sample[
            "variable_declarations"
        ] * 0.3
    )


    score += (
        sample[
            "syntax_errors"
        ] * 15
    )


    score += (
        sample[
            "operator_count"
        ] * 0.2
    )


    score += (
        sample[
            "case_statements"
        ] * 1
    )


    return score


# ==========================================
# CONVERT SCORE TO LABEL
# ==========================================

def calculate_label(
    score
):

    if score < 50:

        return "LOW"


    if score < 100:

        return "MEDIUM"


    return "HIGH"


# ==========================================
# CREATE DATASET
# ==========================================

def create_dataset(
    output_path=DATASET_PATH,
    samples=DEFAULT_SAMPLES
):

    random.seed(
        RANDOM_SEED
    )


    output_directory = os.path.dirname(
        output_path
    )


    if output_directory:

        os.makedirs(
            output_directory,
            exist_ok=True
        )


    fieldnames = (
        FEATURE_NAMES
        +
        ["risk_label"]
    )


    rows = []


    for _ in range(
        samples
    ):

        sample = generate_sample()

        score = calculate_risk_score(
            sample
        )

        label = calculate_label(
            score
        )

        sample["risk_label"] = label

        rows.append(
            sample
        )


    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


    return output_path


# ==========================================
# MAIN
# ==========================================

def main():

    output = create_dataset()


    print()

    print(
        "========================================"
    )

    print(
        "       BUGRADAR DATASET GENERATOR"
    )

    print(
        "========================================"
    )

    print()

    print(
        "BugRadar bootstrap dataset created."
    )

    print(
        "File:",
        output
    )

    print(
        "Samples:",
        DEFAULT_SAMPLES
    )

    print()

    print(
        "========================================"
    )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()