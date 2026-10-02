from analyzer.risk_engine import (
    classify_risk,
    normalize_value,
    calculate_complexity_risk,
    calculate_nesting_risk,
    calculate_function_size_risk,
    calculate_parameter_risk,
    calculate_function_call_risk,
    calculate_recursion_risk,
    calculate_syntax_error_risk,
    calculate_structural_risk,
    calculate_function_risk,
    analyze_function_risk,
    generate_risk_report
)


def test_classify_risk():

    assert (
        classify_risk(10)
        == "LOW"
    )

    assert (
        classify_risk(40)
        == "MEDIUM"
    )

    assert (
        classify_risk(60)
        == "HIGH"
    )

    assert (
        classify_risk(90)
        == "CRITICAL"
    )


def test_normalize_value():

    assert (
        normalize_value(
            10,
            20
        )
        == 50
    )


def test_normalize_value_caps():

    assert (
        normalize_value(
            50,
            20
        )
        == 100
    )


def test_complexity_risk():

    assert (
        calculate_complexity_risk(
            10
        )
        == 50
    )


def test_nesting_risk():

    assert (
        calculate_nesting_risk(
            3
        )
        == 50
    )


def test_function_size_risk():

    assert (
        calculate_function_size_risk(
            50
        )
        == 50
    )


def test_parameter_risk():

    assert (
        calculate_parameter_risk(
            4
        )
        == 50
    )


def test_function_call_risk():

    assert (
        calculate_function_call_risk(
            10
        )
        == 50
    )


def test_recursive_risk():

    assert (
        calculate_recursion_risk(
            True
        )
        == 100
    )

    assert (
        calculate_recursion_risk(
            False
        )
        == 0
    )


def test_syntax_error_risk():

    assert (
        calculate_syntax_error_risk(
            0
        )
        == 0
    )

    assert (
        calculate_syntax_error_risk(
            5
        )
        == 100
    )


def test_structural_risk():

    ast_report = {

        "control_flow": {
            "if": 2,
            "for": 1,
            "while": 1,
            "switch": 0,
            "case": 0,
            "return": 2,
            "break": 0,
            "continue": 0
        },

        "operators": {
            "+": 2,
            "=": 3
        }
    }

    score = (
        calculate_structural_risk(
            ast_report
        )
    )

    assert score >= 0

    assert score <= 100


def test_function_risk():

    function = {

        "complexity": 5,

        "nesting_depth": 2,

        "lines": 20,

        "parameters": 2,

        "function_calls": 3,

        "recursive": False
    }

    score = (
        calculate_function_risk(
            function
        )
    )

    assert score >= 0

    assert score <= 100


def test_analyze_function_risk():

    function = {

        "name": "test",

        "complexity": 5,

        "nesting_depth": 2,

        "lines": 20,

        "parameters": 2,

        "function_calls": 3,

        "recursive": False
    }

    result = (
        analyze_function_risk(
            function
        )
    )

    assert result["name"] == "test"

    assert "risk_score" in result

    assert "classification" in result

    assert "explanations" in result


def test_generate_risk_report():

    ast_report = {

        "syntax_errors": 0,

        "control_flow": {
            "if": 1,
            "for": 1,
            "while": 0,
            "switch": 0,
            "case": 0,
            "return": 1,
            "break": 0,
            "continue": 0
        },

        "operators": {
            "+": 1,
            "=": 1
        },

        "functions": [

            {
                "name": "main",

                "complexity": 2,

                "nesting_depth": 1,

                "lines": 10,

                "parameters": 0,

                "function_calls": 1,

                "recursive": False
            }
        ]
    }

    report = (
        generate_risk_report(
            ast_report
        )
    )

    assert (
        "file_risk_score"
        in report
    )

    assert (
        "file_classification"
        in report
    )

    assert (
        "functions"
        in report
    )