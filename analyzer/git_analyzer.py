import os
import subprocess

from analyzer.ast_parser import analyze_code

from analyzer.complexity import (
    generate_complexity_report
)

from analyzer.risk_engine import (
    generate_risk_report
)


# ==========================================
# GIT COMMAND EXECUTION
# ==========================================

def run_git_command(
    arguments
):

    result = subprocess.run(

        [
            "git",
            *arguments
        ],

        capture_output=True,

        text=True,

        encoding="utf-8",

        errors="replace"
    )


    if result.returncode != 0:

        raise RuntimeError(
            result.stderr.strip()
        )


    return result.stdout.strip()


# ==========================================
# CHECK GIT REPOSITORY
# ==========================================

def is_git_repository():

    try:

        run_git_command(
            [
                "rev-parse",
                "--is-inside-work-tree"
            ]
        )

        return True

    except RuntimeError:

        return False


# ==========================================
# GET CURRENT BRANCH
# ==========================================

def get_current_branch():

    return run_git_command(
        [
            "branch",
            "--show-current"
        ]
    )


# ==========================================
# GET GIT STATUS
# ==========================================

def get_git_status():

    output = run_git_command(
        [
            "status",
            "--porcelain"
        ]
    )

    if not output:

        return []

    return output.splitlines()


# ==========================================
# PARSE GIT STATUS
# ==========================================

def parse_git_status(
    status_lines
):

    files = []


    for line in status_lines:

        if len(line) < 3:
            continue


        status = line[:2]

        file_path = line[3:]


        # Handle renamed files.
        if " -> " in file_path:

            old_path, new_path = (
                file_path.split(
                    " -> ",
                    1
                )
            )

        else:

            old_path = None

            new_path = file_path


        if status == "??":

            change_type = "untracked"

        elif "A" in status:

            change_type = "added"

        elif "D" in status:

            change_type = "deleted"

        elif "R" in status:

            change_type = "renamed"

        elif "M" in status:

            change_type = "modified"

        else:

            change_type = "changed"


        files.append({

            "status": status,

            "change_type": change_type,

            "path": new_path,

            "old_path": old_path

        })


    return files


# ==========================================
# GET CHANGED FILES
# ==========================================

def get_changed_files():

    status_lines = get_git_status()

    return parse_git_status(
        status_lines
    )


# ==========================================
# GET DIFF
# ==========================================

def get_git_diff():

    return run_git_command(
        [
            "diff",
            "HEAD",
            "--unified=0"
        ]
    )


# ==========================================
# GET DIFF STATISTICS
# ==========================================

def get_diff_statistics():

    output = run_git_command(
        [
            "diff",
            "HEAD",
            "--numstat"
        ]
    )


    statistics = []


    if not output:

        return statistics


    for line in output.splitlines():

        parts = line.split(
            "\t"
        )


        if len(parts) != 3:

            continue


        added = parts[0]

        deleted = parts[1]

        path = parts[2]


        # Binary files appear as "-".
        if added == "-":

            added_lines = 0

        else:

            added_lines = int(
                added
            )


        if deleted == "-":

            deleted_lines = 0

        else:

            deleted_lines = int(
                deleted
            )


        statistics.append({

            "path": path,

            "added": added_lines,

            "deleted": deleted_lines

        })


    return statistics


# ==========================================
# COUNT UNTRACKED FILE LINES
# ==========================================

def count_file_lines(
    file_path
):

    if not os.path.exists(
        file_path
    ):

        return 0


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return len(
                file.readlines()
            )

    except (
        UnicodeDecodeError,
        OSError
    ):

        return 0


# ==========================================
# GET TOTAL DIFF STATISTICS
# ==========================================

def calculate_change_summary(
    changed_files,
    diff_statistics
):

    added_lines = 0

    deleted_lines = 0


    statistics_by_path = {

        item["path"]: item

        for item in diff_statistics
    }


    for file in changed_files:

        path = file["path"]

        change_type = (
            file["change_type"]
        )


        if change_type == "untracked":

            added_lines += (
                count_file_lines(
                    path
                )
            )

            continue


        statistics = (
            statistics_by_path.get(
                path
            )
        )


        if statistics is None:

            continue


        added_lines += (
            statistics["added"]
        )

        deleted_lines += (
            statistics["deleted"]
        )


    return {

        "added_lines": added_lines,

        "deleted_lines": deleted_lines,

        "total_changed_lines": (
            added_lines
            +
            deleted_lines
        ),

        "changed_files": len(
            changed_files
        )
    }


# ==========================================
# CHECK C/C++ FILE
# ==========================================

def is_cpp_file(
    file_path
):

    extension = (
        os.path.splitext(
            file_path
        )[1].lower()
    )


    return extension in [

        ".c",

        ".cc",

        ".cpp",

        ".cxx",

        ".h",

        ".hh",

        ".hpp",

        ".hxx"
    ]


# ==========================================
# READ CURRENT FILE
# ==========================================

def read_current_file(
    file_path
):

    if not os.path.exists(
        file_path
    ):

        return None


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except (
        UnicodeDecodeError,
        OSError
    ):

        return None


# ==========================================
# READ FILE FROM GIT HEAD
# ==========================================

def read_file_from_head(
    file_path
):

    try:

        return run_git_command(
            [
                "show",
                f"HEAD:{file_path}"
            ]
        )

    except RuntimeError:

        return None


# ==========================================
# ANALYZE SOURCE CODE
# ==========================================

def analyze_source(
    code
):

    ast_report = analyze_code(
        code
    )


    complexity_report = (
        generate_complexity_report(
            ast_report
        )
    )


    risk_report = (
        generate_risk_report(
            ast_report
        )
    )


    return {

        "ast": ast_report,

        "complexity": complexity_report,

        "risk": risk_report
    }


# ==========================================
# COMPARE SCORES
# ==========================================

def calculate_change(
    before,
    after
):

    return round(
        after - before,
        2
    )


# ==========================================
# CLASSIFY CHANGE IMPACT
# ==========================================

def classify_change_impact(
    risk_change
):

    if risk_change > 10:

        return "INCREASED"

    if risk_change < -10:

        return "DECREASED"

    return "STABLE"


# ==========================================
# ANALYZE CHANGED FILE
# ==========================================

def analyze_changed_file(
    file_info
):

    path = file_info["path"]

    change_type = (
        file_info["change_type"]
    )


    if not is_cpp_file(
        path
    ):

        return {

            "path": path,

            "change_type": change_type,

            "supported": False
        }


    current_code = (
        read_current_file(
            path
        )
    )


    # ======================================
    # DELETED FILE
    # ======================================

    if change_type == "deleted":

        before_code = (
            read_file_from_head(
                path
            )
        )


        if before_code is None:

            return {

                "path": path,

                "change_type": change_type,

                "supported": True,

                "deleted": True
            }


        before = analyze_source(
            before_code
        )


        return {

            "path": path,

            "change_type": change_type,

            "supported": True,

            "deleted": True,

            "before": before,

            "after": None,

            "complexity_change": (
                -before[
                    "complexity"
                ][
                    "file_complexity_score"
                ]
            ),

            "risk_change": (
                -before[
                    "risk"
                ][
                    "file_risk_score"
                ]
            ),

            "impact": "DELETED"
        }


    # ======================================
    # CURRENT CODE UNAVAILABLE
    # ======================================

    if current_code is None:

        return {

            "path": path,

            "change_type": change_type,

            "supported": True,

            "error": (
                "Unable to read current file."
            )
        }


    after = analyze_source(
        current_code
    )


    # ======================================
    # NEW / UNTRACKED FILE
    # ======================================

    if change_type in [
        "added",
        "untracked"
    ]:

        return {

            "path": path,

            "change_type": change_type,

            "supported": True,

            "before": None,

            "after": after,

            "complexity_change": (
                after[
                    "complexity"
                ][
                    "file_complexity_score"
                ]
            ),

            "risk_change": (
                after[
                    "risk"
                ][
                    "file_risk_score"
                ]
            ),

            "impact": "NEW FILE"
        }


    # ======================================
    # MODIFIED FILE
    # ======================================

    before_code = (
        read_file_from_head(
            path
        )
    )


    if before_code is None:

        return {

            "path": path,

            "change_type": change_type,

            "supported": True,

            "before": None,

            "after": after,

            "complexity_change": (
                after[
                    "complexity"
                ][
                    "file_complexity_score"
                ]
            ),

            "risk_change": (
                after[
                    "risk"
                ][
                    "file_risk_score"
                ]
            ),

            "impact": "NEW BASELINE"
        }


    before = analyze_source(
        before_code
    )


    before_complexity = (
        before[
            "complexity"
        ][
            "file_complexity_score"
        ]
    )


    after_complexity = (
        after[
            "complexity"
        ][
            "file_complexity_score"
        ]
    )


    before_risk = (
        before[
            "risk"
        ][
            "file_risk_score"
        ]
    )


    after_risk = (
        after[
            "risk"
        ][
            "file_risk_score"
        ]
    )


    complexity_change = (
        calculate_change(
            before_complexity,
            after_complexity
        )
    )


    risk_change = (
        calculate_change(
            before_risk,
            after_risk
        )
    )


    return {

        "path": path,

        "change_type": change_type,

        "supported": True,

        "before": before,

        "after": after,

        "complexity_change": (
            complexity_change
        ),

        "risk_change": risk_change,

        "impact": classify_change_impact(
            risk_change
        )
    }


# ==========================================
# COMPLETE GIT ANALYSIS
# ==========================================

def generate_git_report():

    if not is_git_repository():

        raise RuntimeError(
            "Current directory is not "
            "a Git repository."
        )


    changed_files = (
        get_changed_files()
    )


    diff_statistics = (
        get_diff_statistics()
    )


    summary = (
        calculate_change_summary(
            changed_files,
            diff_statistics
        )
    )


    file_results = []


    for file_info in changed_files:

        result = analyze_changed_file(
            file_info
        )

        file_results.append(
            result
        )


    return {

        "branch": get_current_branch(),

        "changed_files": changed_files,

        "summary": summary,

        "files": file_results
    }


# ==========================================
# PRINT GIT REPORT
# ==========================================

def print_git_report(
    report
):

    print()

    print("========================================")
    print("              BUGRADAR")
    print("           GIT ANALYSIS")
    print("========================================")


    print()

    print(
        "Branch:",
        report["branch"]
    )


    # ======================================
    # REPOSITORY STATUS
    # ======================================

    print()

    print("Repository Status")

    print("----------------------------------------")


    summary = report["summary"]


    print(
        "Changed Files:",
        summary["changed_files"]
    )


    print(
        "Added Lines:",
        summary["added_lines"]
    )


    print(
        "Deleted Lines:",
        summary["deleted_lines"]
    )


    print(
        "Total Changed Lines:",
        summary["total_changed_lines"]
    )


    # ======================================
    # CHANGED FILES
    # ======================================

    print()

    print("Changed Files")

    print("----------------------------------------")


    if not report["changed_files"]:

        print(
            "No uncommitted changes detected."
        )

    else:

        for file_info in (
            report["changed_files"]
        ):

            print(

                f"{file_info['change_type'].upper():12}"

                f" {file_info['path']}"

            )


    # ======================================
    # FILE ANALYSIS
    # ======================================

    print()

    print("File Analysis")

    print("----------------------------------------")


    analyzed_files = [

        file

        for file in report["files"]

        if file.get(
            "supported",
            False
        )
    ]


    if not analyzed_files:

        print(
            "No supported C/C++ files "
            "were changed."
        )


    for file in analyzed_files:

        print()

        print(
            "File:",
            file["path"]
        )

        print(
            "Change Type:",
            file["change_type"]
        )


        if file.get(
            "deleted",
            False
        ):

            print(
                "Impact: DELETED"
            )

            continue


        if "error" in file:

            print(
                "Error:",
                file["error"]
            )

            continue


        if file["before"] is not None:

            before_complexity = (
                file[
                    "before"
                ][
                    "complexity"
                ][
                    "file_complexity_score"
                ]
            )


            after_complexity = (
                file[
                    "after"
                ][
                    "complexity"
                ][
                    "file_complexity_score"
                ]
            )


            before_risk = (
                file[
                    "before"
                ][
                    "risk"
                ][
                    "file_risk_score"
                ]
            )


            after_risk = (
                file[
                    "after"
                ][
                    "risk"
                ][
                    "file_risk_score"
                ]
            )


            print()

            print(
                "Before Complexity:",
                before_complexity
            )

            print(
                "After Complexity:",
                after_complexity
            )

            print(
                "Complexity Change:",
                f"{file['complexity_change']:+.2f}"
            )


            print()

            print(
                "Before Risk:",
                before_risk
            )

            print(
                "After Risk:",
                after_risk
            )

            print(
                "Risk Change:",
                f"{file['risk_change']:+.2f}"
            )


        else:

            after_complexity = (
                file[
                    "after"
                ][
                    "complexity"
                ][
                    "file_complexity_score"
                ]
            )


            after_risk = (
                file[
                    "after"
                ][
                    "risk"
                ][
                    "file_risk_score"
                ]
            )


            print()

            print(
                "Current Complexity:",
                after_complexity
            )

            print(
                "Current Risk:",
                after_risk
            )


        print()

        print(
            "Change Impact:",
            file["impact"]
        )


    # ======================================
    # END REPORT
    # ======================================

    print()

    print("========================================")
    print("        END OF GIT ANALYSIS")
    print("========================================")

    print()