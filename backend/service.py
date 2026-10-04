from pathlib import Path

from analyzer.ast_parser import (
    analyze_code
)

from analyzer.complexity import (
    generate_complexity_report
)

from analyzer.metrics import (
    count_lines,
    count_blank_lines,
    count_comment_lines,
    count_code_lines,
    count_functions,
    count_conditions,
    count_loops
)

from analyzer.risk_engine import (
    generate_risk_report
)


# ==========================================
# SUPPORTED FILE EXTENSIONS
# ==========================================

SUPPORTED_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hh",
    ".hpp",
    ".hxx"
}


# ==========================================
# VALIDATE FILENAME
# ==========================================

def validate_filename(
    filename
):

    path = Path(
        filename
    )

    extension = (
        path.suffix.lower()
    )

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            "Unsupported file type. "
            "BugRadar currently supports "
            "C/C++ source files."
        )


# ==========================================
# BASIC SOURCE METRICS
# ==========================================

def generate_basic_metrics(
    code
):

    return {

        "lines": count_lines(
            code
        ),

        "blank_lines": count_blank_lines(
            code
        ),

        "comment_lines": count_comment_lines(
            code
        ),

        "code_lines": count_code_lines(
            code
        ),

        "functions": count_functions(
            code
        ),

        "conditions": count_conditions(
            code
        ),

        "loops": count_loops(
            code
        )
    }


# ==========================================
# COMPLETE BUGRADAR ANALYSIS
# ==========================================

def analyze_source(
    code,
    filename
):

    validate_filename(
        filename
    )

    # --------------------------------------
    # BASIC METRICS
    # --------------------------------------

    basic_metrics = (
        generate_basic_metrics(
            code
        )
    )

    # --------------------------------------
    # AST ANALYSIS
    # --------------------------------------

    ast_report = analyze_code(
        code
    )

    # --------------------------------------
    # COMPLEXITY ANALYSIS
    # --------------------------------------

    complexity_report = (
        generate_complexity_report(
            ast_report
        )
    )

    # --------------------------------------
    # RISK ANALYSIS
    # --------------------------------------

    risk_report = (
        generate_risk_report(
            ast_report
        )
    )

    # --------------------------------------
    # RETURN COMPLETE RESULT
    # --------------------------------------

    return {

        "success": True,

        "filename": filename,

        "syntax_errors": (
            ast_report[
                "syntax_errors"
            ]
        ),

        "basic_metrics": basic_metrics,

        "ast_metrics": (
            ast_report[
                "metrics"
            ]
        ),

        "complexity": complexity_report,

        "risk": risk_report
    }