# ==========================================
# BUGRADAR ML FEATURE TESTS
# ==========================================

from ml.features import (
    FEATURE_NAMES,
    extract_features,
    extract_feature_dict,
    get_feature_count,
    validate_features
)


# ==========================================
# SAMPLE AST REPORT
# ==========================================

def sample_ast_report():

    return {

        "syntax_errors": 1,

        "metrics": {

            "functions": 3,

            "if_statements": 4,

            "for_loops": 2,

            "while_loops": 1,

            "switch_statements": 1,

            "case_statements": 3,

            "function_calls": 8,

            "variable_declarations": 12,

            "max_nesting_depth": 4,

            "cyclomatic_complexity": 8,

            "classes": 1,

            "structs": 0,

            "return_statements": 5,

            "break_statements": 2,

            "continue_statements": 1
        },

        "operators": {

            "+": 5,

            "=": 8,

            "&&": 2
        },

        "includes": [

            "<iostream>",

            "<vector>"
        ]
    }


# ==========================================
# TEST FEATURE COUNT
# ==========================================

def test_feature_count():

    assert (
        get_feature_count()
        ==
        len(FEATURE_NAMES)
    )


# ==========================================
# TEST FEATURE EXTRACTION
# ==========================================

def test_extract_features():

    report = sample_ast_report()

    features = extract_features(
        report
    )


    assert isinstance(
        features,
        list
    )


    assert len(features) == (
        len(FEATURE_NAMES)
    )


# ==========================================
# TEST FEATURE VALUES
# ==========================================

def test_feature_values():

    report = sample_ast_report()

    features = extract_features(
        report
    )


    assert features[0] == 3

    assert features[1] == 4

    assert features[2] == 2

    assert features[8] == 4

    assert features[9] == 8

    assert features[10] == 1


# ==========================================
# TEST FEATURE DICTIONARY
# ==========================================

def test_feature_dictionary():

    report = sample_ast_report()

    feature_dict = (
        extract_feature_dict(
            report
        )
    )


    assert isinstance(
        feature_dict,
        dict
    )


    assert (
        feature_dict[
            "functions"
        ]
        ==
        3
    )


    assert (
        feature_dict[
            "cyclomatic_complexity"
        ]
        ==
        8
    )


# ==========================================
# TEST VALIDATION
# ==========================================

def test_validate_features():

    report = sample_ast_report()

    features = extract_features(
        report
    )


    assert validate_features(
        features
    )


# ==========================================
# TEST INVALID FEATURES
# ==========================================

def test_invalid_features():

    assert not validate_features(
        []
    )