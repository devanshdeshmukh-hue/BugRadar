from analyzer.ast_parser import (
    parse_code,
    analyze_code
)


def test_parse_code():

    code = """
int main()
{
    return 0;
}
"""

    tree = parse_code(
        code
    )

    assert tree is not None

    assert tree.root_node is not None


def test_analyze_code():

    code = """
int main()
{
    return 0;
}
"""

    report = analyze_code(
        code
    )

    assert report is not None

    assert "syntax_errors" in report

    assert "metrics" in report

    assert "functions" in report


def test_analyze_code_detects_function():

    code = """
int add(int a, int b)
{
    return a + b;
}
"""

    report = analyze_code(
        code
    )

    assert report["metrics"]["functions"] == 1

    assert (
        report["functions"][0]["name"]
        == "add"
    )