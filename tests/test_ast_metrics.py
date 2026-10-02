from analyzer.ast_parser import parse_code

from analyzer.ast_metrics import (
    count_functions,
    count_if_statements,
    count_for_loops,
    count_while_loops,
    calculate_nesting_depth,
    calculate_cyclomatic_complexity,
    count_classes,
    count_structs,
    count_function_calls,
    count_syntax_errors
)


def get_root(code):

    tree = parse_code(
        code
    )

    return tree.root_node


def test_count_functions():

    code = """
int add(int a, int b)
{
    return a + b;
}

int main()
{
    return 0;
}
"""

    root = get_root(code)

    assert count_functions(root) == 2


def test_count_if_statements():

    code = """
int main()
{
    if (x > 10)
    {
        return 1;
    }

    if (x > 5)
    {
        return 2;
    }

    return 0;
}
"""

    root = get_root(code)

    assert count_if_statements(root) == 2


def test_count_for_loops():

    code = """
int main()
{
    for (int i = 0; i < 10; i++)
    {
        cout << i;
    }

    return 0;
}
"""

    root = get_root(code)

    assert count_for_loops(root) == 1


def test_count_while_loops():

    code = """
int main()
{
    while (x < 10)
    {
        x++;
    }

    return 0;
}
"""

    root = get_root(code)

    assert count_while_loops(root) == 1


def test_nesting_depth():

    code = """
int main()
{
    if (x > 0)
    {
        for (int i = 0; i < 10; i++)
        {
            while (x < 100)
            {
                x++;
            }
        }
    }

    return 0;
}
"""

    root = get_root(code)

    depth = calculate_nesting_depth(
        root
    )

    assert depth == 3


def test_cyclomatic_complexity():

    code = """
int main()
{
    if (x > 0)
    {
        return 1;
    }

    if (y > 0)
    {
        return 2;
    }

    return 0;
}
"""

    root = get_root(code)

    complexity = (
        calculate_cyclomatic_complexity(
            root
        )
    )

    assert complexity == 3


def test_count_classes():

    code = """
class Student
{
public:
    int age;
};
"""

    root = get_root(code)

    assert count_classes(root) == 1


def test_count_structs():

    code = """
struct Student
{
    int age;
};
"""

    root = get_root(code)

    assert count_structs(root) == 1


def test_count_function_calls():

    code = """
int main()
{
    foo();
    bar();

    return 0;
}
"""

    root = get_root(code)

    assert count_function_calls(root) == 2


def test_valid_code_has_no_syntax_errors():

    code = """
int main()
{
    return 0;
}
"""

    root = get_root(code)

    assert count_syntax_errors(root) == 0