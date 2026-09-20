
from tree_sitter import Language, Parser
import tree_sitter_cpp

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

from analyzer.code_reader import read_file


CPP_LANGUAGE = Language(tree_sitter_cpp.language())

parser = Parser(CPP_LANGUAGE)


def parse_code(code):
    tree = parser.parse(code.encode("utf-8"))

    return tree


def print_ast(node, level=0):
    indentation = "  " * level

    print(indentation + node.type)

    for child in node.children:
        print_ast(child, level + 1)


file_path = "examples/sample.cpp"

code = read_file(file_path)
tree = parse_code(code)
root = tree.root_node
report = generate_analysis_report(root)

print()
print("================================")
print("       BUGRADAR AST METRICS")
print("================================")

print()

print("Functions:", count_functions(root))
print("If Statements:", count_if_statements(root))
print("For Loops:", count_for_loops(root))
print("While Loops:", count_while_loops(root))
print("Return Statements:", count_return_statements(root))
print("Maximum Nesting Depth:", calculate_nesting_depth(root))
print("Cyclomatic Complexity:", calculate_cyclomatic_complexity(root))
print("Classes:", count_classes(root))
print("Structs:", count_structs(root))
print("Function Calls:", count_function_calls(root))
print("Variable Declarations:", count_variable_declarations(root))
print("Syntax Errors:", count_syntax_errors(root))


functions = analyze_functions(root)
function_calls = analyze_function_calls(root)


print()
print("Function Analysis")
print("--------------------------------")

for function in functions:
    print()
    print("Function:", function["name"])
    print("Start Line:", function["start_line"])
    print("Cyclomatic Complexity:", function["complexity"])
    print("Nesting Depth:", function["nesting_depth"])

classes = analyze_classes(root)

print()
print("Class / Struct Analysis")
print("--------------------------------")

for item in classes:
    print()
    print("Type:", item["type"])
    print("Name:", item["name"])
    print("Start Line:", item["start_line"])

calls = analyze_function_calls(root)

print()
print("Function Calls Analysis")
print("--------------------------------")

for call in calls:
    print("Called Function:", call)

variables = analyze_variable_declarations(root)

print()
print("Variable Analysis")
print("--------------------------------")

for variable in variables:
    print("Variable:", variable)

print()
print("================================")
print("       STRUCTURED REPORT")
print("================================")

print(report)

print()
print("================================")