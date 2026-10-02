import subprocess
import sys


def test_cli_help():

    result = subprocess.run(

        [
            sys.executable,
            "main.py",
            "--help"
        ],

        capture_output=True,

        text=True
    )


    assert result.returncode == 0

    assert "BugRadar" in result.stdout

    assert "analyze" in result.stdout


def test_cli_version():

    result = subprocess.run(

        [
            sys.executable,
            "main.py",
            "--version"
        ],

        capture_output=True,

        text=True
    )


    assert result.returncode == 0

    assert "BugRadar 0.1.0" in result.stdout


def test_cli_analyze():

    result = subprocess.run(

        [
            sys.executable,
            "main.py",
            "analyze",
            "examples/sample.cpp"
        ],

        capture_output=True,

        text=True
    )


    assert result.returncode == 0

    assert "BUGRADAR" in result.stdout

    assert "CODE SUMMARY" in result.stdout

    assert "COMPLEXITY ANALYSIS" in result.stdout

    assert "RISK ANALYSIS" in result.stdout


def test_cli_missing_file():

    result = subprocess.run(

        [
            sys.executable,
            "main.py",
            "analyze",
            "examples/not_found.cpp"
        ],

        capture_output=True,

        text=True
    )


    assert result.returncode != 0

    assert "File not found" in result.stdout


def test_cli_unsupported_file(tmp_path):

    test_file = (
        tmp_path / "test.txt"
    )

    test_file.write_text(
        "This is not C++ code."
    )


    result = subprocess.run(

        [
            sys.executable,
            "main.py",
            "analyze",
            str(test_file)
        ],

        capture_output=True,

        text=True
    )


    assert result.returncode != 0

    assert (
        "Unsupported file type"
        in result.stdout
    )