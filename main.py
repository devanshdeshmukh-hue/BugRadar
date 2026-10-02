import argparse
import os
import sys

from analyzer.code_reader import read_file

from analyzer.ast_parser import (
    analyze_code
)

from analyzer.complexity import (
    generate_complexity_report
)

from analyzer.risk_engine import (
    generate_risk_report
)


# ==========================================
# BUGRADAR VERSION
# ==========================================

VERSION = "0.1.0"


# ==========================================
# PRINT HEADER
# ==========================================

def print_header():

    print()

    print("========================================")
    print("              BUGRADAR")
    print("       CODE RISK ANALYZER")
    print("========================================")


# ==========================================
# PRINT SECTION
# ==========================================

def print_section(title):

    print()

    print("----------------------------------------")

    print(
        title
    )

    print("----------------------------------------")


# ==========================================
# VALIDATE FILE
# ==========================================

def validate_file(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )


    if not os.path.isfile(file_path):

        raise ValueError(
            f"Path is not a file: {file_path}"
        )


    extension = (
        os.path.splitext(file_path)[1]
        .lower()
    )


    if extension not in [
        ".cpp",
        ".cc",
        ".cxx",
        ".h",
        ".hpp"
    ]:

        raise ValueError(
            "Unsupported file type. "
            "BugRadar currently supports "
            "C/C++ files."
        )


# ==========================================
# PRINT CODE SUMMARY
# ==========================================

def print_code_summary(
    ast_report
):

    metrics = (
        ast_report["metrics"]
    )


    print_section(
        "CODE SUMMARY"
    )


    print(
        "Functions              :",
        metrics["functions"]
    )


    print(
        "Conditions             :",
        metrics["if_statements"]
    )


    print(
        "For Loops              :",
        metrics["for_loops"]
    )


    print(
        "While Loops            :",
        metrics["while_loops"]
    )


    print(
        "Switch Statements      :",
        metrics["switch_statements"]
    )


    print(
        "Variables              :",
        metrics["variable_declarations"]
    )


    print(
        "Function Calls         :",
        metrics["function_calls"]
    )


    print(
        "Classes                :",
        metrics["classes"]
    )


    print(
        "Structs                :",
        metrics["structs"]
    )


    print(
        "Maximum Nesting Depth  :",
        metrics["max_nesting_depth"]
    )


    print(
        "Cyclomatic Complexity  :",
        metrics["cyclomatic_complexity"]
    )


    print(
        "Syntax Errors          :",
        ast_report["syntax_errors"]
    )


# ==========================================
# PRINT COMPLEXITY REPORT
# ==========================================

def print_complexity_report(
    complexity_report
):

    print_section(
        "COMPLEXITY ANALYSIS"
    )


    print(
        "File Complexity Score  :",
        complexity_report[
            "file_complexity_score"
        ]
    )


    print(
        "Classification         :",
        complexity_report[
            "file_classification"
        ]
    )


    print(
        "Average Function Score :",
        complexity_report[
            "average_function_complexity"
        ]
    )


    most_complex = (
        complexity_report[
            "most_complex_function"
        ]
    )


    if most_complex is not None:

        print()

        print(
            "Most Complex Function  :",
            most_complex["name"]
        )

        print(
            "Function Score         :",
            most_complex[
                "complexity_score"
            ]
        )

        print(
            "Function Classification :",
            most_complex[
                "classification"
            ]
        )


# ==========================================
# PRINT RISK REPORT
# ==========================================

def print_risk_report(
    risk_report
):

    print_section(
        "RISK ANALYSIS"
    )


    print(
        "File Risk Score        :",
        risk_report[
            "file_risk_score"
        ]
    )


    print(
        "Risk Classification    :",
        risk_report[
            "file_classification"
        ]
    )


    highest = (
        risk_report[
            "highest_risk_function"
        ]
    )


    if highest is not None:

        print()

        print(
            "Highest Risk Function  :",
            highest["name"]
        )

        print(
            "Risk Score             :",
            highest["risk_score"]
        )

        print(
            "Classification         :",
            highest["classification"]
        )


        if highest["explanations"]:

            print()

            print(
                "Risk Factors:"
            )


            for reason in (
                highest["explanations"]
            ):

                print(
                    "  -",
                    reason
                )


        else:

            print()

            print(
                "Risk Factors           : None"
            )


# ==========================================
# PRINT FUNCTION RISKS
# ==========================================

def print_function_risks(
    risk_report
):

    print_section(
        "FUNCTION RISK ANALYSIS"
    )


    functions = (
        risk_report["functions"]
    )


    if not functions:

        print(
            "No functions detected."
        )

        return


    for function in functions:

        print()

        print(
            "Function:",
            function["name"]
        )

        print(
            "Risk Score:",
            function["risk_score"]
        )

        print(
            "Classification:",
            function["classification"]
        )


        if function["explanations"]:

            print(
                "Risk Factors:"
            )


            for explanation in (
                function["explanations"]
            ):

                print(
                    "  -",
                    explanation
                )

        else:

            print(
                "Risk Factors: None"
            )


# ==========================================
# PRINT FINAL SUMMARY
# ==========================================

def print_final_summary(
    risk_report
):

    print_section(
        "FINAL SUMMARY"
    )


    print(
        "BugRadar Risk Score:",
        risk_report[
            "file_risk_score"
        ]
    )


    print(
        "BugRadar Classification:",
        risk_report[
            "file_classification"
        ]
    )


# ==========================================
# ANALYZE FILE
# ==========================================

def analyze_file(
    file_path
):

    validate_file(
        file_path
    )


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


    risk_report = (
        generate_risk_report(
            ast_report
        )
    )


    print_header()


    print()

    print(
        "File:",
        file_path
    )


    print_code_summary(
        ast_report
    )


    print_complexity_report(
        complexity_report
    )


    print_risk_report(
        risk_report
    )


    print_function_risks(
        risk_report
    )


    print_final_summary(
        risk_report
    )


    print()

    print("========================================")
    print("          END OF BUGRADAR")
    print("========================================")

    print()


# ==========================================
# CREATE ARGUMENT PARSER
# ==========================================

def create_parser():

    parser = argparse.ArgumentParser(

        prog="BugRadar",

        description=(
            "BugRadar - C/C++ source-code "
            "complexity and risk analyzer."
        )
    )


    parser.add_argument(
        "--version",
        action="version",
        version=f"BugRadar {VERSION}"
    )


    subparsers = (
        parser.add_subparsers(
            dest="command"
        )
    )


    # ======================================
    # ANALYZE COMMAND
    # ======================================

    analyze_parser = (
        subparsers.add_parser(
            "analyze",
            help="Analyze a C/C++ source file."
        )
    )


    analyze_parser.add_argument(

        "file",

        help=(
            "Path to the C/C++ source file."
        )
    )


    return parser


# ==========================================
# MAIN CLI FUNCTION
# ==========================================

def main():

    parser = create_parser()

    args = parser.parse_args()


    if args.command == "analyze":

        try:

            analyze_file(
                args.file
            )

        except (
            FileNotFoundError,
            ValueError
        ) as error:

            print()

            print(
                "Error:",
                error
            )

            print()

            sys.exit(1)


        except Exception as error:

            print()

            print(
                "Unexpected error:",
                error
            )

            print()

            sys.exit(1)


    else:

        parser.print_help()


# ==========================================
# PYTHON ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()