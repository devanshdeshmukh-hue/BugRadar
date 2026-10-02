from analyzer.complexity import (
    classify_value,
    normalize_metric,
    calculate_function_complexity_score,
    classify_complexity_score,
    analyze_function_complexity,
    analyze_all_functions,
    calculate_file_complexity_score,
    generate_complexity_report
)


def test_classify_value_low():

    thresholds = {
        "low": 5,
        "moderate": 10,
        "high": 20
    }

    assert (
        classify_value(
            3,
            thresholds
        )
        == "LOW"
    )


def test_classify_value_moderate():

    thresholds = {
        "low": 5,
        "moderate": 10,
        "high": 20
    }

    assert (
        classify_value(
            8,
            thresholds
        )
        == "MODERATE"
    )


def test_classify_value_high():

    thresholds = {
        "low": 5,
        "moderate": 10,
        "high": 20
    }

    assert (
        classify_value(
            15,
            thresholds
        )
        == "HIGH"
    )


def test_classify_value_critical():

    thresholds = {
        "low": 5,
        "moderate": 10,
        "high": 20
    }

    assert (
        classify_value(
            25,
            thresholds
        )
        == "CRITICAL"
    )


def test_normalize_metric():

    thresholds = {
        "low": 5,
        "moderate": 10,
        "high": 20
    }

    assert (
        normalize_metric(
            10,
            thresholds
        )
        == 50
    )


def test_normalize_metric_caps_at_100():

    thresholds = {
        "low": 5,
        "moderate": 10,
        "high": 20
    }

    assert (
        normalize_metric(
            50,
            thresholds
        )
        == 100
    )


def test_function_complexity_score():

    function = {

        "name": "test",

        "complexity": 5,

        "nesting_depth": 2,

        "lines": 20,

        "parameters": 2,

        "function_calls": 3,

        "recursive": False
    }

    score = (
        calculate_function_complexity_score(
            function
        )
    )

    assert score >= 0

    assert score <= 100


def test_classify_complexity_score():

    assert (
        classify_complexity_score(10)
        == "LOW"
    )

    assert (
        classify_complexity_score(40)
        == "MODERATE"
    )

    assert (
        classify_complexity_score(60)
        == "HIGH"
    )

    assert (
        classify_complexity_score(90)
        == "CRITICAL"
    )


def test_analyze_function_complexity():

    function = {

        "name": "calculate",

        "complexity": 5,

        "nesting_depth": 2,

        "lines": 20,

        "parameters": 2,

        "function_calls": 3,

        "recursive": False
    }

    result = (
        analyze_function_complexity(
            function
        )
    )

    assert result["name"] == "calculate"

    assert "complexity_score" in result

    assert "classification" in result


def test_analyze_all_functions():

    functions = [

        {
            "name": "one",
            "complexity": 2,
            "nesting_depth": 1,
            "lines": 10,
            "parameters": 1,
            "function_calls": 1,
            "recursive": False
        },

        {
            "name": "two",
            "complexity": 10,
            "nesting_depth": 3,
            "lines": 30,
            "parameters": 3,
            "function_calls": 5,
            "recursive": False
        }
    ]

    results = (
        analyze_all_functions(
            functions
        )
    )

    assert len(results) == 2


def test_empty_function_list():

    assert (
        calculate_file_complexity_score([])
        == 0
    )


def test_generate_complexity_report():

    ast_report = {

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
        generate_complexity_report(
            ast_report
        )
    )

    assert (
        "file_complexity_score"
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