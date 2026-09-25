# ==========================================
# BASIC AST NODE COUNTING
# ==========================================

def count_node_type(node, node_type):
    count = 0

    if node.type == node_type:
        count += 1

    for child in node.children:
        count += count_node_type(child, node_type)

    return count


# ==========================================
# BASIC AST METRICS
# ==========================================

def count_functions(root):
    return count_node_type(root, "function_definition")


def count_if_statements(root):
    return count_node_type(root, "if_statement")


def count_for_loops(root):
    return count_node_type(root, "for_statement")


def count_while_loops(root):
    return count_node_type(root, "while_statement")

def count_switch_statements(root):
    return count_node_type(root, "switch_statement")


def count_return_statements(root):
    return count_node_type(root, "return_statement")


# ==========================================
# NESTING DEPTH
# ==========================================

def calculate_nesting_depth(node, current_depth=0):
    max_depth = current_depth

    if node.type in [
        "if_statement",
        "for_statement",
        "while_statement",
        "switch_statement"
    ]:
        current_depth += 1

        if current_depth > max_depth:
            max_depth = current_depth

    for child in node.children:
        child_depth = calculate_nesting_depth(
            child,
            current_depth
        )

        if child_depth > max_depth:
            max_depth = child_depth

    return max_depth


# ==========================================
# CYCLOMATIC COMPLEXITY
# ==========================================

def calculate_cyclomatic_complexity(node):
    complexity = 1

    decision_nodes = [
        "if_statement",
        "for_statement",
        "while_statement",
        "case_statement",
        "conditional_expression",
    ]

    logical_operators = [
        "&&",
        "||"
    ]

    def count_decisions(current_node):
        count = 0

        if current_node.type in decision_nodes:
            count += 1

        if current_node.type in logical_operators:
            count += 1

        for child in current_node.children:
            count += count_decisions(child)

        return count

    complexity += count_decisions(node)

    return complexity

    def count_decisions(current_node):
        count = 0

        if current_node.type in decision_nodes:
            count += 1

        for child in current_node.children:
            count += count_decisions(child)

        return count

    complexity += count_decisions(node)

    return complexity


# ==========================================
# FIND IDENTIFIER
# ==========================================

def find_identifier(node):
    if node is None:
        return None

    if node.type == "identifier":
        return node.text.decode("utf-8")

    for child in node.children:
        result = find_identifier(child)

        if result is not None:
            return result

    return None


# ==========================================
# FUNCTION PARAMETER COUNT
# ==========================================

def count_function_parameters(node):
    declarator = node.child_by_field_name("declarator")

    if declarator is None:
        return 0

    parameter_list = None

    def find_parameter_list(current_node):
        nonlocal parameter_list

        if current_node.type == "parameter_list":
            parameter_list = current_node
            return

        for child in current_node.children:

            if parameter_list is None:
                find_parameter_list(child)

    find_parameter_list(declarator)

    if parameter_list is None:
        return 0

    count = 0

    for child in parameter_list.children:

        if child.type == "parameter_declaration":
            count += 1

    return count


# ==========================================
# FUNCTION ANALYSIS
# ==========================================

def analyze_functions(root):
    functions = []

    def visit(node):

        if node.type == "function_definition":

            declarator = node.child_by_field_name(
                "declarator"
            )

            function_name = find_identifier(
                declarator
            )

            complexity = calculate_cyclomatic_complexity(
                node
            )

            nesting_depth = calculate_nesting_depth(
                node
            )

            parameter_count = count_function_parameters(
                node
            )

            start_line = node.start_point[0] + 1

            end_line = node.end_point[0] + 1

            function_lines = end_line - start_line + 1

            functions.append({
                "name": function_name,
                "start_line": start_line,
                "end_line": end_line,
                "lines": function_lines,
                "parameters": parameter_count,
                "complexity": complexity,
                "nesting_depth": nesting_depth
            })

        for child in node.children:
            visit(child)

    visit(root)

    return functions


# ==========================================
# CLASS / STRUCT DETECTION
# ==========================================

def count_classes(root):
    return count_node_type(
        root,
        "class_specifier"
    )


def count_structs(root):
    return count_node_type(
        root,
        "struct_specifier"
    )


# ==========================================
# CLASS / STRUCT ANALYSIS
# ==========================================

def analyze_classes(root):
    classes = []

    def visit(node):

        if node.type in [
            "class_specifier",
            "struct_specifier"
        ]:

            name_node = node.child_by_field_name(
                "name"
            )

            if name_node is not None:
                name = name_node.text.decode(
                    "utf-8"
                )
            else:
                name = "anonymous"

            start_line = node.start_point[0] + 1

            classes.append({
                "name": name,
                "type": (
                    "class"
                    if node.type == "class_specifier"
                    else "struct"
                ),
                "start_line": start_line
            })

        for child in node.children:
            visit(child)

    visit(root)

    return classes


# ==========================================
# FUNCTION CALL DETECTION
# ==========================================

def count_function_calls(root):
    return count_node_type(
        root,
        "call_expression"
    )


def analyze_function_calls(root):
    calls = []

    def visit(node):

        if node.type == "call_expression":

            function_node = node.child_by_field_name(
                "function"
            )

            if function_node is not None:

                function_name = (
                    function_node.text.decode("utf-8")
                )

                calls.append(function_name)

        for child in node.children:
            visit(child)

    visit(root)

    return calls


# ==========================================
# VARIABLE DECLARATION DETECTION
# ==========================================

def count_variable_declarations(root):
    return count_node_type(
        root,
        "declaration"
    )


def analyze_variable_declarations(root):
    variables = []

    def visit(node):

        if node.type == "declaration":

            for child in node.children:

                if child.type == "init_declarator":

                    name_node = child.child_by_field_name(
                        "declarator"
                    )

                    if name_node is not None:

                        variables.append(
                            name_node.text.decode(
                                "utf-8"
                            )
                        )

                elif child.type == "identifier":

                    variables.append(
                        child.text.decode(
                            "utf-8"
                        )
                    )

        for child in node.children:
            visit(child)

    visit(root)

    return variables


# ==========================================
# SYNTAX ERROR DETECTION
# ==========================================

def count_syntax_errors(root):
    error_count = 0

    def visit(node):

        nonlocal error_count

        if node.type == "ERROR":
            error_count += 1

        if node.is_missing:
            error_count += 1

        for child in node.children:
            visit(child)

    visit(root)

    return error_count


# ==========================================
# COMPLETE STRUCTURED ANALYSIS REPORT
# ==========================================

def generate_analysis_report(root):

    report = {

        "syntax_errors": count_syntax_errors(root),

        "metrics": {

            "functions": count_functions(root),

            "if_statements": count_if_statements(root),

            "for_loops": count_for_loops(root),

            "while_loops": count_while_loops(root),

            "switch_statements": count_switch_statements(root),

            "return_statements": count_return_statements(root),

            "classes": count_classes(root),

            "structs": count_structs(root),

            "function_calls": count_function_calls(root),

            "variable_declarations": (
                count_variable_declarations(root)
            ),

            "max_nesting_depth": (
                calculate_nesting_depth(root)
            ),

            "cyclomatic_complexity": (
                calculate_cyclomatic_complexity(root)
            )
        },

        "functions": analyze_functions(root),

        "classes": analyze_classes(root),

        "calls": analyze_function_calls(root),

        "variables": analyze_variable_declarations(root)
    }

    return report