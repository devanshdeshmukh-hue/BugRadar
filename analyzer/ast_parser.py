from tree_sitter import Language, Parser
import tree_sitter_cpp

from analyzer.code_reader import read_file

from analyzer.ast_metrics import (
    count_functions,
    count_if_statements,
    count_for_loops,
    count_while_loops,
    count_return_statements,
    calculate_nesting_depth,
    calculate_cyclomatic_complexity,
    analyze_functions,
    count_classes,
    count_structs,
    analyze_classes,
    count_function_calls,
    analyze_function_calls,
    count_variable_declarations,
    analyze_variable_declarations,
    count_syntax_errors,
    generate_analysis_report
)


# ==========================================
# TREE-SITTER C++ LANGUAGE SETUP
# ==========================================

CPP_LANGUAGE = Language(
    tree_sitter_cpp.language()
)

parser = Parser(CPP_LANGUAGE)


# ==========================================
# PARSE C++ CODE
# ==========================================

def parse_code(code):

    tree = parser.parse(
        code.encode("utf-8")
    )

    return tree


# ==========================================
# ANALYZE C++ CODE
# ==========================================

def analyze_code(code):

    tree = parse_code(code)

    root = tree.root_node

    report = generate_analysis_report(
        root
    )

    return report


# ==========================================
# MAIN PROGRAM
# ==========================================

file_path = "examples/sample.cpp"

code = read_file(
    file_path
)

report = analyze_code(
    code
)


# ==========================================
# DISPLAY BUGRADAR REPORT
# ==========================================

print()

print("========================================")
print("          BUGRADAR AST REPORT")
print("========================================")


# ==========================================
# SYNTAX ERRORS
# ==========================================

print()

print(
    "Syntax Errors:",
    report["syntax_errors"]
)


# ==========================================
# GENERAL METRICS
# ==========================================

print()

print("Metrics")

print("----------------------------------------")

for metric, value in report["metrics"].items():

    print(
        metric,
        ":",
        value
    )


# ==========================================
# FUNCTION ANALYSIS
# ==========================================

print()

print("Function Analysis")

print("----------------------------------------")

for function in report["functions"]:

    print()

    print(
        "Function:",
        function["name"]
    )

    print(
        "Start Line:",
        function["start_line"]
    )

    print(
        "End Line:",
        function["end_line"]
    )

    print(
        "Lines:",
        function["lines"]
    )

    print(
        "Parameters:",
        function["parameters"]
    )

    print(
        "Cyclomatic Complexity:",
        function["complexity"]
    )

    print(
        "Nesting Depth:",
        function["nesting_depth"]
    )


# ==========================================
# CLASS / STRUCT ANALYSIS
# ==========================================

print()

print("Class / Struct Analysis")

print("----------------------------------------")

for item in report["classes"]:

    print()

    print(
        "Type:",
        item["type"]
    )

    print(
        "Name:",
        item["name"]
    )

    print(
        "Start Line:",
        item["start_line"]
    )


# ==========================================
# FUNCTION CALL ANALYSIS
# ==========================================

print()

print("Function Calls")

print("----------------------------------------")

for call in report["calls"]:

    print(
        "Called Function:",
        call
    )


# ==========================================
# VARIABLE ANALYSIS
# ==========================================

print()

print("Variable Analysis")

print("----------------------------------------")

for variable in report["variables"]:

    print(
        "Variable:",
        variable
    )


# ==========================================
# END OF REPORT
# ==========================================

print()

print("========================================")
print("       END OF BUGRADAR REPORT")
print("========================================")