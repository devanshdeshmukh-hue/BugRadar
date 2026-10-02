from analyzer.metrics import (
    count_lines,
    count_blank_lines,
    count_comment_lines,
    count_code_lines,
    count_functions,
    count_conditions,
    count_loops
)


def test_count_lines():

    code = """int main()
{
    return 0;
}
"""

    assert count_lines(code) == 4


def test_count_blank_lines():

    code = """int main()

{
    return 0;
}
"""

    assert count_blank_lines(code) == 1


def test_count_comment_lines():

    code = """// comment
int main()
{
    // another comment
    return 0;
}
"""

    assert count_comment_lines(code) == 2


def test_count_code_lines():

    code = """// comment

int main()
{
    return 0;
}
"""

    assert count_code_lines(code) == 4


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

    assert count_functions(code) == 2


def test_count_conditions():

    code = """
if (x > 10)
{
    x++;
}
else if (x > 5)
{
    x--;
}
"""

    assert count_conditions(code) == 2


def test_count_loops():

    code = """
for (int i = 0; i < 10; i++)
{
    cout << i;
}

while (x < 10)
{
    x++;
}
"""

    assert count_loops(code) == 2