from analyzer.metrics import (
    count_lines,
    count_blank_lines,
    count_comment_lines,
    count_code_lines,
    count_functions,
    count_conditions,
    count_loops
)
from analyzer.code_reader import read_file

from analyzer.metrics import (
    count_lines,
    count_blank_lines,
    count_comment_lines,
    count_code_lines,
    count_conditions,
    count_loops
)


file_path = "examples/sample.cpp"

code = read_file(file_path)

total_lines = count_lines(code)
blank_lines = count_blank_lines(code)
comment_lines = count_comment_lines(code)
code_lines = count_code_lines(code)
functions = count_functions(code)
conditions = count_conditions(code)
loops = count_loops(code)


print("================================")
print("           BUGRADAR")
print("================================")

print()

print("File:", file_path)

print()
print("Code Metrics")
print("--------------------------------")

print("Total Lines:", total_lines)
print("Blank Lines:", blank_lines)
print("Comment Lines:", comment_lines)
print("Code Lines:", code_lines)
print("Functions:", functions)
print("Conditions:", conditions)
print("Loops:", loops)

print()
print("================================")