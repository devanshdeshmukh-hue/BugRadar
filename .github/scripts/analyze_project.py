from pathlib import Path
import os
import sys


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ==========================================
# BUGRADAR IMPORTS
# ==========================================

from analyzer.code_reader import read_file

from analyzer.ast_parser import analyze_code

from analyzer.complexity import (
    generate_complexity_report
)

from analyzer.risk_engine import (
    generate_risk_report
)


# ==========================================
# SUPPORTED SOURCE FILES
# ==========================================

SOURCE_EXTENSIONS = {
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
# EXCLUDED DIRECTORIES
# ==========================================

EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache"
}


# ==========================================
# FIND SOURCE FILES
# ==========================================

def find_source_files():

    files = []

    for path in PROJECT_ROOT.rglob("*"):

        if not path.is_file():
            continue

        if any(
            part in EXCLUDED_DIRECTORIES
            for part in path.parts
        ):
            continue

        if path.suffix.lower() in SOURCE_EXTENSIONS:

            files.append(path)

    return sorted(files)


# ==========================================
# ANALYZE SINGLE FILE
# ==========================================

def analyze_file(file_path):

    code = read_file(
        str(file_path)
    )

    ast_report = analyze_code(
        code
    )

    complexity_report = (
        generate_complexity_report(
            ast_report
        )
    )

    risk_report = (
        generate_risk_report(
            ast_report
        )
    )

    return {
        "ast": ast_report,
        "complexity": complexity_report,
        "risk": risk_report
    }


# ==========================================
# PRINT FILE REPORT
# ==========================================

def print_file_report(
    file_path,
    report
):

    relative_path = file_path.relative_to(
        PROJECT_ROOT
    )

    complexity = report[
        "complexity"
    ]

    risk = report[
        "risk"
    ]

    print()

    print(
        "========================================"
    )

    print(
        "BUGRADAR FILE ANALYSIS"
    )

    print(
        "========================================"
    )

    print()

    print(
        "File:",
        relative_path
    )

    print(
        "Complexity Score:",
        complexity[
            "file_complexity_score"
        ]
    )

    print(
        "Complexity Classification:",
        complexity[
            "file_classification"
        ]
    )

    print(
        "Risk Score:",
        risk[
            "file_risk_score"
        ]
    )

    print(
        "Risk Classification:",
        risk[
            "file_classification"
        ]
    )

    print()

    print(
        "Functions:",
        len(
            report[
                "ast"
            ][
                "functions"
            ]
        )
    )

    print(
        "Syntax Errors:",
        report[
            "ast"
        ][
            "syntax_errors"
        ]
    )

    highest_risk = (
        risk[
            "highest_risk_function"
        ]
    )

    if highest_risk is not None:

        print()

        print(
            "Highest Risk Function:",
            highest_risk[
                "name"
            ]
        )

        print(
            "Function Risk Score:",
            highest_risk[
                "risk_score"
            ]
        )

        print(
            "Function Classification:",
            highest_risk[
                "classification"
            ]
        )

        if highest_risk[
            "explanations"
        ]:

            print(
                "Risk Factors:"
            )

            for explanation in (
                highest_risk[
                    "explanations"
                ]
            ):

                print(
                    " -",
                    explanation
                )

    print()

    print(
        "========================================"
    )


# ==========================================
# WRITE GITHUB STEP SUMMARY
# ==========================================

def write_github_summary(
    results
):

    # --------------------------------------
    # GITHUB_STEP_SUMMARY exists only
    # inside GitHub Actions.
    # --------------------------------------

    summary_path = os.environ.get(
        "GITHUB_STEP_SUMMARY"
    )

    # --------------------------------------
    # When running locally, the variable
    # does not exist.
    #
    # Therefore, simply skip this step.
    # --------------------------------------

    if not summary_path:

        print()
        print(
            "GitHub Actions summary skipped "
            "(running locally)."
        )

        return

    # --------------------------------------
    # Convert the actual GitHub path
    # into a Path object.
    # --------------------------------------

    summary_file = Path(
        summary_path
    )

    lines = []

    lines.append(
        "# 🛡️ BugRadar Analysis"
    )

    lines.append("")

    lines.append(
        "| File | Complexity | Risk | Classification |"
    )

    lines.append(
        "|---|---:|---:|---|"
    )

    for item in results:

        path = item[
            "path"
        ]

        complexity = item[
            "report"
        ][
            "complexity"
        ]

        risk = item[
            "report"
        ][
            "risk"
        ]

        lines.append(
            "| "
            + str(path)
            + " | "
            + str(
                complexity[
                    "file_complexity_score"
                ]
            )
            + " | "
            + str(
                risk[
                    "file_risk_score"
                ]
            )
            + " | "
            + risk[
                "file_classification"
            ]
            + " |"
        )

    lines.append("")

    lines.append(
        "BugRadar analysis completed successfully."
    )

    # --------------------------------------
    # Append report to GitHub summary.
    # --------------------------------------

    with summary_file.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(lines)
        )


# ==========================================
# MAIN
# ==========================================

def main():

    print()

    print(
        "========================================"
    )

    print(
        "          BUGRADAR CI ANALYSIS"
    )

    print(
        "========================================"
    )

    source_files = find_source_files()

    if not source_files:

        print()

        print(
            "No supported C/C++ source files found."
        )

        print()

        return 0

    results = []

    for file_path in source_files:

        try:

            report = analyze_file(
                file_path
            )

            results.append(
                {
                    "path": file_path.relative_to(
                        PROJECT_ROOT
                    ),
                    "report": report
                }
            )

            print_file_report(
                file_path,
                report
            )

        except Exception as error:

            print()

            print(
                "ERROR analyzing:",
                file_path
            )

            print(
                "Reason:",
                error
            )

            return 1

    # --------------------------------------
    # Write GitHub summary.
    #
    # Locally this safely does nothing.
    # --------------------------------------

    write_github_summary(
        results
    )

    print()

    print(
        "========================================"
    )

    print(
        "       BUGRADAR CI ANALYSIS PASSED"
    )

    print(
        "========================================"
    )

    return 0


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    raise SystemExit(
        main()
    )