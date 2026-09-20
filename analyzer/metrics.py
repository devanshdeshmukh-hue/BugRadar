def count_lines(code):
    lines = code.splitlines()

    return len(lines)


def count_blank_lines(code):
    lines = code.splitlines()

    blank_lines = 0

    for line in lines:
        if line.strip() == "":
            blank_lines += 1

    return blank_lines


def count_comment_lines(code):
    lines = code.splitlines()

    comment_lines = 0

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("//"):
            comment_lines += 1

    return comment_lines


def count_code_lines(code):
    total_lines = count_lines(code)
    blank_lines = count_blank_lines(code)
    comment_lines = count_comment_lines(code)

    return total_lines - blank_lines - comment_lines

def count_functions(code):
    lines = code.splitlines()

    function_count = 0

    for line in lines:
        stripped_line = line.strip()

        if "(" in stripped_line and ")" in stripped_line:
            if not stripped_line.startswith(("if", "else if", "for", "while", "switch")):
                function_count += 1

    return function_count

def count_conditions(code):
    lines = code.splitlines()

    condition_count = 0

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("if ") or stripped_line.startswith("if("):
            condition_count += 1

        elif stripped_line.startswith("else if ") or stripped_line.startswith("else if("):
            condition_count += 1

    return condition_count

def count_loops(code):
    lines = code.splitlines()

    loop_count = 0

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("for ") or stripped_line.startswith("for("):
            loop_count += 1

        elif stripped_line.startswith("while ") or stripped_line.startswith("while("):
            loop_count += 1

    return loop_count