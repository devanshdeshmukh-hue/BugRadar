from analyzer.code_reader import read_file


def test_read_file(tmp_path):

    test_file = tmp_path / "test.cpp"

    test_file.write_text(
        "int main() { return 0; }"
    )

    content = read_file(
        str(test_file)
    )

    assert content == (
        "int main() { return 0; }"
    )