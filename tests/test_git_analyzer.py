from analyzer.git_analyzer import (
    parse_git_status,
    calculate_change,
    classify_change_impact,
    is_cpp_file
)


# ==========================================
# GIT STATUS TEST
# ==========================================

def test_parse_git_status():

    status_lines = [

        " M examples/sample.cpp",

        "A  test.cpp",

        "?? new_file.cpp",

        " D old.cpp"
    ]


    result = parse_git_status(
        status_lines
    )


    assert len(result) == 4


    assert (
        result[0]["change_type"]
        == "modified"
    )


    assert (
        result[1]["change_type"]
        == "added"
    )


    assert (
        result[2]["change_type"]
        == "untracked"
    )


    assert (
        result[3]["change_type"]
        == "deleted"
    )


# ==========================================
# CHANGE CALCULATION TEST
# ==========================================

def test_calculate_change():

    assert (
        calculate_change(
            20,
            30
        )
        == 10
    )


    assert (
        calculate_change(
            30,
            20
        )
        == -10
    )


# ==========================================
# CHANGE IMPACT TEST
# ==========================================

def test_classify_change_impact():

    assert (
        classify_change_impact(
            15
        )
        == "INCREASED"
    )


    assert (
        classify_change_impact(
            -15
        )
        == "DECREASED"
    )


    assert (
        classify_change_impact(
            5
        )
        == "STABLE"
    )


# ==========================================
# C++ FILE DETECTION
# ==========================================

def test_is_cpp_file():

    assert is_cpp_file(
        "main.cpp"
    )


    assert is_cpp_file(
        "header.hpp"
    )


    assert is_cpp_file(
        "program.cc"
    )


    assert not is_cpp_file(
        "notes.txt"
    )


    assert not is_cpp_file(
        "image.png"
    )