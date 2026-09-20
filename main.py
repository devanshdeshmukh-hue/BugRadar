from analyzer.code_reader import read_file
from analyzer.metrics import count_lines

file_path = "examples/sample.cpp"

code = read_file(file_path)

total_lines = count_lines(code)

print("================================")
print("           BUGRADAR")
print("================================")

print("File:", file_path)
print("Total Lines:", total_lines)