# ==========================================
# BUGRADAR ML FEATURE EXTRACTION
# ==========================================


# ==========================================
# FEATURE NAMES
# ==========================================

FEATURE_NAMES = [

    "functions",

    "if_statements",

    "for_loops",

    "while_loops",

    "switch_statements",

    "case_statements",

    "function_calls",

    "variable_declarations",

    "max_nesting_depth",

    "cyclomatic_complexity",

    "syntax_errors",

    "classes",

    "structs",

    "return_statements",

    "break_statements",

    "continue_statements",

    "operator_count",

    "include_count"
]


# ==========================================
# SAFE INTEGER CONVERSION
# ==========================================

def safe_int(value):

    try:

        return int(value)

    except (
        TypeError,
        ValueError
    ):

        return 0


# ==========================================
# EXTRACT FEATURES
# ==========================================

def extract_features(
    ast_report
):

    metrics = ast_report.get(
        "metrics",
        {}
    )

    operators = ast_report.get(
        "operators",
        {}
    )

    includes = ast_report.get(
        "includes",
        []
    )

    features = [

        safe_int(
            metrics.get(
                "functions",
                0
            )
        ),

        safe_int(
            metrics.get(
                "if_statements",
                0
            )
        ),

        safe_int(
            metrics.get(
                "for_loops",
                0
            )
        ),

        safe_int(
            metrics.get(
                "while_loops",
                0
            )
        ),

        safe_int(
            metrics.get(
                "switch_statements",
                0
            )
        ),

        safe_int(
            metrics.get(
                "case_statements",
                0
            )
        ),

        safe_int(
            metrics.get(
                "function_calls",
                0
            )
        ),

        safe_int(
            metrics.get(
                "variable_declarations",
                0
            )
        ),

        safe_int(
            metrics.get(
                "max_nesting_depth",
                0
            )
        ),

        safe_int(
            metrics.get(
                "cyclomatic_complexity",
                0
            )
        ),

        safe_int(
            ast_report.get(
                "syntax_errors",
                0
            )
        ),

        safe_int(
            metrics.get(
                "classes",
                0
            )
        ),

        safe_int(
            metrics.get(
                "structs",
                0
            )
        ),

        safe_int(
            metrics.get(
                "return_statements",
                0
            )
        ),

        safe_int(
            metrics.get(
                "break_statements",
                0
            )
        ),

        safe_int(
            metrics.get(
                "continue_statements",
                0
            )
        ),

        sum(
            operators.values()
        ),

        len(
            includes
        )
    ]


    return features


# ==========================================
# FEATURE DICTIONARY
# ==========================================

def extract_feature_dict(
    ast_report
):

    values = extract_features(
        ast_report
    )

    return dict(
        zip(
            FEATURE_NAMES,
            values
        )
    )


# ==========================================
# FEATURE COUNT
# ==========================================

def get_feature_count():

    return len(
        FEATURE_NAMES
    )


# ==========================================
# VALIDATE FEATURES
# ==========================================

def validate_features(
    features
):

    if not isinstance(
        features,
        list
    ):

        return False


    if len(features) != len(
        FEATURE_NAMES
    ):

        return False


    for value in features:

        if not isinstance(
            value,
            (int, float)
        ):

            return False


    return True