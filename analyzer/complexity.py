# ==========================================
# BUGRADAR COMPLEXITY ENGINE
# ==========================================


# ==========================================
# COMPLEXITY THRESHOLDS
# ==========================================

CYCLOMATIC_THRESHOLDS = {
    "low": 5,
    "moderate": 10,
    "high": 20
}


NESTING_THRESHOLDS = {
    "low": 2,
    "moderate": 4,
    "high": 6
}


FUNCTION_SIZE_THRESHOLDS = {
    "low": 20,
    "moderate": 50,
    "high": 100
}


PARAMETER_THRESHOLDS = {
    "low": 3,
    "moderate": 5,
    "high": 8
}


FUNCTION_CALL_THRESHOLDS = {
    "low": 5,
    "moderate": 10,
    "high": 20
}


# ==========================================
# COMPLEXITY WEIGHTS
# ==========================================

COMPLEXITY_WEIGHTS = {
    "cyclomatic": 0.35,
    "nesting": 0.20,
    "size": 0.20,
    "parameters": 0.10,
    "function_calls": 0.15
}


# ==========================================
# CLASSIFY RAW VALUE
# ==========================================

def classify_value(
    value,
    thresholds
):
    if value <= thresholds["low"]:
        return "LOW"

    if value <= thresholds["moderate"]:
        return "MODERATE"

    if value <= thresholds["high"]:
        return "HIGH"

    return "CRITICAL"


# ==========================================
# CYCLOMATIC COMPLEXITY ANALYSIS
# ==========================================

def analyze_cyclomatic_complexity(
    complexity
):
    classification = classify_value(
        complexity,
        CYCLOMATIC_THRESHOLDS
    )

    return {
        "value": complexity,
        "classification": classification
    }


# ==========================================
# NESTING DEPTH ANALYSIS
# ==========================================

def analyze_nesting_depth(
    nesting_depth
):
    classification = classify_value(
        nesting_depth,
        NESTING_THRESHOLDS
    )

    return {
        "value": nesting_depth,
        "classification": classification
    }


# ==========================================
# FUNCTION SIZE ANALYSIS
# ==========================================

def analyze_function_size(
    lines
):
    classification = classify_value(
        lines,
        FUNCTION_SIZE_THRESHOLDS
    )

    return {
        "value": lines,
        "classification": classification
    }


# ==========================================
# PARAMETER ANALYSIS
# ==========================================

def analyze_parameters(
    parameters
):
    classification = classify_value(
        parameters,
        PARAMETER_THRESHOLDS
    )

    return {
        "value": parameters,
        "classification": classification
    }


# ==========================================
# FUNCTION CALL ANALYSIS
# ==========================================

def analyze_function_call_count(
    function_calls
):
    classification = classify_value(
        function_calls,
        FUNCTION_CALL_THRESHOLDS
    )

    return {
        "value": function_calls,
        "classification": classification
    }


# ==========================================
# NORMALIZE METRIC TO 0-100
# ==========================================

def normalize_metric(
    value,
    thresholds
):
    high = thresholds["high"]

    if high <= 0:
        return 0

    score = (
        value / high
    ) * 100

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    return round(
        score,
        2
    )


# ==========================================
# FUNCTION COMPLEXITY SCORE
# ==========================================

def calculate_function_complexity_score(
    function
):
    cyclomatic_score = normalize_metric(
        function["complexity"],
        CYCLOMATIC_THRESHOLDS
    )

    nesting_score = normalize_metric(
        function["nesting_depth"],
        NESTING_THRESHOLDS
    )

    size_score = normalize_metric(
        function["lines"],
        FUNCTION_SIZE_THRESHOLDS
    )

    parameter_score = normalize_metric(
        function["parameters"],
        PARAMETER_THRESHOLDS
    )

    call_score = normalize_metric(
        function["function_calls"],
        FUNCTION_CALL_THRESHOLDS
    )

    score = (
        cyclomatic_score
        * COMPLEXITY_WEIGHTS["cyclomatic"]
        +
        nesting_score
        * COMPLEXITY_WEIGHTS["nesting"]
        +
        size_score
        * COMPLEXITY_WEIGHTS["size"]
        +
        parameter_score
        * COMPLEXITY_WEIGHTS["parameters"]
        +
        call_score
        * COMPLEXITY_WEIGHTS["function_calls"]
    )

    return round(
        score,
        2
    )


# ==========================================
# FUNCTION SCORE CLASSIFICATION
# ==========================================

def classify_complexity_score(
    score
):
    if score <= 25:
        return "LOW"

    if score <= 50:
        return "MODERATE"

    if score <= 75:
        return "HIGH"

    return "CRITICAL"


# ==========================================
# COMPLETE FUNCTION COMPLEXITY ANALYSIS
# ==========================================

def analyze_function_complexity(
    function
):
    score = calculate_function_complexity_score(
        function
    )

    classification = classify_complexity_score(
        score
    )

    return {
        "name": function["name"],
        "complexity_score": score,
        "classification": classification,

        "cyclomatic_complexity": (
            function["complexity"]
        ),

        "nesting_depth": (
            function["nesting_depth"]
        ),

        "lines": function["lines"],

        "parameters": function["parameters"],

        "function_calls": (
            function["function_calls"]
        ),

        "recursive": function["recursive"]
    }


# ==========================================
# ANALYZE ALL FUNCTIONS
# ==========================================

def analyze_all_functions(
    functions
):
    results = []

    for function in functions:

        result = analyze_function_complexity(
            function
        )

        results.append(
            result
        )

    return results


# ==========================================
# FILE COMPLEXITY SCORE
# ==========================================

def calculate_file_complexity_score(
    function_results
):
    if not function_results:
        return 0

    total_score = 0

    for function in function_results:

        total_score += (
            function["complexity_score"]
        )

    average_score = (
        total_score
        /
        len(function_results)
    )

    return round(
        average_score,
        2
    )


# ==========================================
# FILE COMPLEXITY CLASSIFICATION
# ==========================================

def classify_file_complexity(
    score
):
    return classify_complexity_score(
        score
    )


# ==========================================
# COMPLEXITY SUMMARY
# ==========================================

def generate_complexity_summary(
    function_results
):
    summary = {
        "total_functions": len(
            function_results
        ),

        "low": 0,

        "moderate": 0,

        "high": 0,

        "critical": 0
    }

    for function in function_results:

        classification = (
            function["classification"]
            .lower()
        )

        if classification in summary:

            summary[classification] += 1

    return summary


# ==========================================
# MOST COMPLEX FUNCTION
# ==========================================

def find_most_complex_function(
    function_results
):
    if not function_results:
        return None

    most_complex = function_results[0]

    for function in function_results[1:]:

        if (
            function["complexity_score"]
            >
            most_complex["complexity_score"]
        ):
            most_complex = function

    return most_complex


# ==========================================
# AVERAGE FUNCTION COMPLEXITY
# ==========================================

def calculate_average_function_complexity(
    function_results
):
    if not function_results:
        return 0

    total = 0

    for function in function_results:

        total += (
            function["complexity_score"]
        )

    average = (
        total
        /
        len(function_results)
    )

    return round(
        average,
        2
    )


# ==========================================
# COMPLETE COMPLEXITY REPORT
# ==========================================

def generate_complexity_report(
    ast_report
):
    function_results = analyze_all_functions(
        ast_report["functions"]
    )

    file_score = (
        calculate_file_complexity_score(
            function_results
        )
    )

    file_classification = (
        classify_file_complexity(
            file_score
        )
    )

    summary = (
        generate_complexity_summary(
            function_results
        )
    )

    most_complex_function = (
        find_most_complex_function(
            function_results
        )
    )

    average_function_complexity = (
        calculate_average_function_complexity(
            function_results
        )
    )

    return {

        "file_complexity_score": file_score,

        "file_classification": (
            file_classification
        ),

        "average_function_complexity": (
            average_function_complexity
        ),

        "most_complex_function": (
            most_complex_function
        ),

        "summary": summary,

        "functions": function_results
    }


# ==========================================
# STANDALONE TEST
# ==========================================

if __name__ == "__main__":

    from analyzer.ast_parser import analyze_code
    from analyzer.code_reader import read_file

    file_path = "examples/sample.cpp"

    code = read_file(
        file_path
    )

    ast_report = analyze_code(
        code
    )

    complexity_report = (
        generate_complexity_report(
            ast_report
        )
    )

    print()

    print("========================================")
    print("       BUGRADAR COMPLEXITY REPORT")
    print("========================================")

    print()

    print(
        "File Complexity Score:",
        complexity_report[
            "file_complexity_score"
        ]
    )

    print(
        "File Classification:",
        complexity_report[
            "file_classification"
        ]
    )

    print(
        "Average Function Complexity:",
        complexity_report[
            "average_function_complexity"
        ]
    )

    print()

    print("Complexity Summary")

    print("----------------------------------------")

    for key, value in (
        complexity_report["summary"].items()
    ):

        print(
            key,
            ":",
            value
        )

    print()

    print("Most Complex Function")

    print("----------------------------------------")

    most_complex = (
        complexity_report[
            "most_complex_function"
        ]
    )

    if most_complex is not None:

        print(
            "Function:",
            most_complex["name"]
        )

        print(
            "Score:",
            most_complex["complexity_score"]
        )

        print(
            "Classification:",
            most_complex["classification"]
        )

    else:

        print(
            "No functions detected."
        )

    print()

    print("Function Complexity")

    print("----------------------------------------")

    for function in (
        complexity_report["functions"]
    ):

        print()

        print(
            "Function:",
            function["name"]
        )

        print(
            "Complexity Score:",
            function[
                "complexity_score"
            ]
        )

        print(
            "Classification:",
            function[
                "classification"
            ]
        )

        print(
            "Cyclomatic Complexity:",
            function[
                "cyclomatic_complexity"
            ]
        )

        print(
            "Nesting Depth:",
            function[
                "nesting_depth"
            ]
        )

        print(
            "Lines:",
            function["lines"]
        )

        print(
            "Parameters:",
            function[
                "parameters"
            ]
        )

        print(
            "Function Calls:",
            function[
                "function_calls"
            ]
        )

        print(
            "Recursive:",
            function[
                "recursive"
            ]
        )

    print()

    print("========================================")
    print("     END OF COMPLEXITY REPORT")
    print("========================================")