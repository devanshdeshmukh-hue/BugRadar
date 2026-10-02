# ==========================================
# BUGRADAR RISK ENGINE
# ==========================================


# ==========================================
# RISK WEIGHTS
# ==========================================

RISK_WEIGHTS = {
    "complexity": 0.30,
    "nesting": 0.15,
    "function_size": 0.15,
    "parameters": 0.10,
    "function_calls": 0.10,
    "recursion": 0.05,
    "syntax_errors": 0.10,
    "structural": 0.05
}


# ==========================================
# RISK CLASSIFICATION
# ==========================================

def classify_risk(score):

    if score <= 25:
        return "LOW"

    if score <= 50:
        return "MEDIUM"

    if score <= 75:
        return "HIGH"

    return "CRITICAL"


# ==========================================
# NORMALIZE VALUE
# ==========================================

def normalize_value(
    value,
    threshold
):

    if threshold <= 0:
        return 0

    score = (
        value / threshold
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
# COMPLEXITY RISK
# ==========================================

def calculate_complexity_risk(
    complexity
):

    return normalize_value(
        complexity,
        20
    )


# ==========================================
# NESTING RISK
# ==========================================

def calculate_nesting_risk(
    nesting_depth
):

    return normalize_value(
        nesting_depth,
        6
    )


# ==========================================
# FUNCTION SIZE RISK
# ==========================================

def calculate_function_size_risk(
    lines
):

    return normalize_value(
        lines,
        100
    )


# ==========================================
# PARAMETER RISK
# ==========================================

def calculate_parameter_risk(
    parameters
):

    return normalize_value(
        parameters,
        8
    )


# ==========================================
# FUNCTION CALL RISK
# ==========================================

def calculate_function_call_risk(
    function_calls
):

    return normalize_value(
        function_calls,
        20
    )


# ==========================================
# RECURSION RISK
# ==========================================

def calculate_recursion_risk(
    recursive
):

    if recursive:
        return 100

    return 0


# ==========================================
# SYNTAX ERROR RISK
# ==========================================

def calculate_syntax_error_risk(
    syntax_errors
):

    if syntax_errors <= 0:
        return 0

    if syntax_errors >= 5:
        return 100

    return (
        syntax_errors / 5
    ) * 100


# ==========================================
# STRUCTURAL RISK
# ==========================================

def calculate_structural_risk(
    ast_report
):

    control_flow = ast_report.get(
        "control_flow",
        {}
    )

    operators = ast_report.get(
        "operators",
        {}
    )

    control_flow_count = sum(
        control_flow.values()
    )

    operator_count = sum(
        operators.values()
    )

    control_score = normalize_value(
        control_flow_count,
        20
    )

    operator_score = normalize_value(
        operator_count,
        50
    )

    structural_score = (
        control_score * 0.6
        +
        operator_score * 0.4
    )

    return round(
        structural_score,
        2
    )


# ==========================================
# FUNCTION RISK SCORE
# ==========================================

def calculate_function_risk(
    function
):

    complexity_risk = (
        calculate_complexity_risk(
            function["complexity"]
        )
    )

    nesting_risk = (
        calculate_nesting_risk(
            function["nesting_depth"]
        )
    )

    size_risk = (
        calculate_function_size_risk(
            function["lines"]
        )
    )

    parameter_risk = (
        calculate_parameter_risk(
            function["parameters"]
        )
    )

    call_risk = (
        calculate_function_call_risk(
            function["function_calls"]
        )
    )

    recursion_risk = (
        calculate_recursion_risk(
            function["recursive"]
        )
    )

    score = (
        complexity_risk
        * RISK_WEIGHTS["complexity"]

        +

        nesting_risk
        * RISK_WEIGHTS["nesting"]

        +

        size_risk
        * RISK_WEIGHTS["function_size"]

        +

        parameter_risk
        * RISK_WEIGHTS["parameters"]

        +

        call_risk
        * RISK_WEIGHTS["function_calls"]

        +

        recursion_risk
        * RISK_WEIGHTS["recursion"]
    )

    return round(
        score,
        2
    )


# ==========================================
# FUNCTION RISK EXPLANATIONS
# ==========================================

def generate_function_risk_explanations(
    function
):

    explanations = []

    if function["complexity"] > 10:

        explanations.append(
            "High cyclomatic complexity"
        )

    if function["nesting_depth"] > 4:

        explanations.append(
            "Deep control-flow nesting"
        )

    if function["lines"] > 50:

        explanations.append(
            "Large function size"
        )

    if function["parameters"] > 5:

        explanations.append(
            "Large number of parameters"
        )

    if function["function_calls"] > 10:

        explanations.append(
            "High number of function calls"
        )

    if function["recursive"]:

        explanations.append(
            "Recursive function"
        )

    return explanations


# ==========================================
# ANALYZE FUNCTION RISK
# ==========================================

def analyze_function_risk(
    function
):

    score = calculate_function_risk(
        function
    )

    classification = classify_risk(
        score
    )

    explanations = (
        generate_function_risk_explanations(
            function
        )
    )

    return {

        "name": function["name"],

        "risk_score": score,

        "classification": classification,

        "explanations": explanations,

        "metrics": {

            "complexity": function[
                "complexity"
            ],

            "nesting_depth": function[
                "nesting_depth"
            ],

            "lines": function[
                "lines"
            ],

            "parameters": function[
                "parameters"
            ],

            "function_calls": function[
                "function_calls"
            ],

            "recursive": function[
                "recursive"
            ]
        }
    }


# ==========================================
# ANALYZE ALL FUNCTION RISKS
# ==========================================

def analyze_all_function_risks(
    functions
):

    results = []

    for function in functions:

        result = analyze_function_risk(
            function
        )

        results.append(
            result
        )

    return results


# ==========================================
# FILE RISK SCORE
# ==========================================

def calculate_file_risk_score(
    function_results,
    syntax_errors,
    structural_risk
):

    if function_results:

        total_function_risk = 0

        for function in function_results:

            total_function_risk += (
                function["risk_score"]
            )

        average_function_risk = (
            total_function_risk
            /
            len(function_results)
        )

    else:

        average_function_risk = 0


    syntax_risk = (
        calculate_syntax_error_risk(
            syntax_errors
        )
    )


    final_score = (

        average_function_risk * 0.75

        +

        syntax_risk * 0.10

        +

        structural_risk * 0.15
    )


    return round(
        final_score,
        2
    )


# ==========================================
# RISK SUMMARY
# ==========================================

def generate_risk_summary(
    function_results
):

    summary = {

        "total_functions": len(
            function_results
        ),

        "low": 0,

        "medium": 0,

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
# HIGHEST RISK FUNCTION
# ==========================================

def find_highest_risk_function(
    function_results
):

    if not function_results:
        return None


    highest = function_results[0]


    for function in function_results[1:]:

        if (
            function["risk_score"]
            >
            highest["risk_score"]
        ):

            highest = function


    return highest


# ==========================================
# RISK FACTOR BREAKDOWN
# ==========================================

def generate_risk_factor_breakdown(
    ast_report
):

    syntax_errors = ast_report.get(
        "syntax_errors",
        0
    )


    structural_risk = (
        calculate_structural_risk(
            ast_report
        )
    )


    return {

        "syntax_error_risk": (
            calculate_syntax_error_risk(
                syntax_errors
            )
        ),

        "structural_risk": structural_risk
    }


# ==========================================
# COMPLETE RISK REPORT
# ==========================================

def generate_risk_report(
    ast_report
):

    function_results = (
        analyze_all_function_risks(
            ast_report.get(
                "functions",
                []
            )
        )
    )


    risk_factors = (
        generate_risk_factor_breakdown(
            ast_report
        )
    )


    file_score = (
        calculate_file_risk_score(

            function_results,

            ast_report.get(
                "syntax_errors",
                0
            ),

            risk_factors[
                "structural_risk"
            ]
        )
    )


    file_classification = (
        classify_risk(
            file_score
        )
    )


    summary = (
        generate_risk_summary(
            function_results
        )
    )


    highest_risk_function = (
        find_highest_risk_function(
            function_results
        )
    )


    return {

        "file_risk_score": file_score,

        "file_classification": (
            file_classification
        ),

        "risk_factors": risk_factors,

        "summary": summary,

        "highest_risk_function": (
            highest_risk_function
        ),

        "functions": function_results
    }


# ==========================================
# STANDALONE TEST
# ==========================================

if __name__ == "__main__":

    from analyzer.ast_parser import analyze_code

    from analyzer.code_reader import read_file


    file_path = (
        "examples/sample.cpp"
    )


    code = read_file(
        file_path
    )


    ast_report = analyze_code(
        code
    )


    risk_report = (
        generate_risk_report(
            ast_report
        )
    )


    print()

    print(
        "========================================"
    )

    print(
        "          BUGRADAR RISK REPORT"
    )

    print(
        "========================================"
    )


    print()

    print(
        "File Risk Score:",
        risk_report[
            "file_risk_score"
        ]
    )


    print(
        "File Classification:",
        risk_report[
            "file_classification"
        ]
    )


    print()

    print(
        "Risk Factors"
    )

    print(
        "----------------------------------------"
    )


    for factor, value in (
        risk_report[
            "risk_factors"
        ].items()
    ):

        print(
            factor,
            ":",
            value
        )


    print()

    print(
        "Risk Summary"
    )

    print(
        "----------------------------------------"
    )


    for key, value in (
        risk_report[
            "summary"
        ].items()
    ):

        print(
            key,
            ":",
            value
        )


    print()

    print(
        "Highest Risk Function"
    )

    print(
        "----------------------------------------"
    )


    highest = (
        risk_report[
            "highest_risk_function"
        ]
    )


    if highest is not None:

        print(
            "Function:",
            highest["name"]
        )

        print(
            "Risk Score:",
            highest["risk_score"]
        )

        print(
            "Classification:",
            highest["classification"]
        )

        print(
            "Reasons:"
        )

        for reason in (
            highest["explanations"]
        ):

            print(
                "-",
                reason
            )

    else:

        print(
            "No functions detected."
        )


    print()

    print(
        "Function Risk Analysis"
    )

    print(
        "----------------------------------------"
    )


    for function in (
        risk_report["functions"]
    ):

        print()

        print(
            "Function:",
            function["name"]
        )

        print(
            "Risk Score:",
            function[
                "risk_score"
            ]
        )

        print(
            "Classification:",
            function[
                "classification"
            ]
        )


        if function["explanations"]:

            print(
                "Risk Factors:"
            )

            for explanation in (
                function[
                    "explanations"
                ]
            ):

                print(
                    " -",
                    explanation
                )

        else:

            print(
                "Risk Factors: None"
            )


    print()

    print(
        "========================================"
    )

    print(
        "       END OF BUGRADAR RISK REPORT"
    )

    print(
        "========================================"
    )