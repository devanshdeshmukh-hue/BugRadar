from pathlib import Path
import json
import os
import subprocess
import sys
from urllib import request
from urllib.error import HTTPError, URLError


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ==========================================
# BUGRADAR IMPORTS
# ==========================================

from analyzer.code_reader import read_file

from analyzer.ast_parser import analyze_code

from analyzer.complexity import (
    generate_complexity_report
)

from analyzer.risk_engine import (
    generate_risk_report
)


# ==========================================
# SUPPORTED FILE TYPES
# ==========================================

SOURCE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hh",
    ".hpp",
    ".hxx"
}


# ==========================================
# READ GITHUB EVENT
# ==========================================

def load_github_event():

    event_path = os.environ.get(
        "GITHUB_EVENT_PATH"
    )

    if not event_path:

        return {}

    path = Path(
        event_path
    )

    if not path.exists():

        return {}

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# GET PR INFORMATION
# ==========================================

def get_pull_request_info(
    event
):

    pull_request = event.get(
        "pull_request",
        {}
    )

    return {
        "number": pull_request.get(
            "number"
        ),

        "title": pull_request.get(
            "title",
            ""
        ),

        "base_sha": pull_request.get(
            "base",
            {}
        ).get(
            "sha"
        ),

        "head_sha": pull_request.get(
            "head",
            {}
        ).get(
            "sha"
        )
    }


# ==========================================
# GET CHANGED FILES USING GIT
# ==========================================

def get_changed_files(
    base_sha,
    head_sha
):

    if not base_sha:

        raise ValueError(
            "Base commit SHA was not found."
        )

    if not head_sha:

        raise ValueError(
            "Head commit SHA was not found."
        )

    command = [
        "git",
        "diff",
        "--name-only",
        base_sha,
        head_sha
    ]

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            "Unable to determine changed files:\n"
            + result.stderr
        )

    files = []

    for line in result.stdout.splitlines():

        line = line.strip()

        if line:

            files.append(
                Path(line)
            )

    return files


# ==========================================
# FILTER C/C++ FILES
# ==========================================

def filter_source_files(
    files
):

    source_files = []

    for file_path in files:

        if (
            file_path.suffix.lower()
            in SOURCE_EXTENSIONS
        ):

            source_files.append(
                file_path
            )

    return source_files


# ==========================================
# ANALYZE FILE
# ==========================================

def analyze_file(
    relative_path
):

    absolute_path = (
        PROJECT_ROOT
        /
        relative_path
    )

    if not absolute_path.exists():

        return None

    code = read_file(
        str(absolute_path)
    )

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
        "path": str(
            relative_path
        ).replace(
            "\\",
            "/"
        ),

        "ast": ast_report,

        "complexity": complexity_report,

        "risk": risk_report
    }


# ==========================================
# ANALYZE CHANGED FILES
# ==========================================

def analyze_changed_files(
    source_files
):

    results = []

    for file_path in source_files:

        try:

            report = analyze_file(
                file_path
            )

            if report is not None:

                results.append(
                    report
                )

        except Exception as error:

            results.append(
                {
                    "path": str(
                        file_path
                    ).replace(
                        "\\",
                        "/"
                    ),

                    "error": str(
                        error
                    )
                }
            )

    return results


# ==========================================
# RISK EMOJI
# ==========================================

def risk_indicator(
    classification
):

    classification = (
        classification.upper()
    )

    if classification == "LOW":

        return "🟢"

    if classification == "MEDIUM":

        return "🟡"

    if classification == "HIGH":

        return "🟠"

    if classification == "CRITICAL":

        return "🔴"

    return "⚪"


# ==========================================
# BUILD PR REPORT
# ==========================================

def build_pr_report(
    pr_info,
    changed_files,
    results
):

    lines = []

    lines.append(
        "## 🛡️ BugRadar Pull Request Analysis"
    )

    lines.append("")

    lines.append(
        "BugRadar analyzed the C/C++ files "
        "changed in this pull request."
    )

    lines.append("")

    lines.append(
        "**Pull Request:** "
        + str(
            pr_info.get(
                "number",
                "Unknown"
            )
        )
    )

    lines.append("")

    lines.append(
        "**Changed C/C++ files:** "
        + str(
            len(changed_files)
        )
    )

    lines.append("")

    if not results:

        lines.append(
            "### ✅ No analyzable C/C++ files"
        )

        lines.append("")

        lines.append(
            "No changed C/C++ source files "
            "were available for BugRadar analysis."
        )

        lines.append("")

        lines.append(
            "---"
        )

        lines.append(
            "*BugRadar automated analysis* 🤖"
        )

        return "\n".join(
            lines
        )

    lines.append(
        "### 📊 File Risk Summary"
    )

    lines.append("")

    lines.append(
        "| File | Complexity | Risk | Classification |"
    )

    lines.append(
        "|---|---:|---:|---|"
    )

    for result in results:

        if "error" in result:

            lines.append(
                "| "
                + result["path"]
                + " | ❌ | ❌ | Analysis Error |"
            )

            continue

        complexity = result[
            "complexity"
        ]

        risk = result[
            "risk"
        ]

        complexity_score = (
            complexity[
                "file_complexity_score"
            ]
        )

        risk_score = (
            risk[
                "file_risk_score"
            ]
        )

        classification = (
            risk[
                "file_classification"
            ]
        )

        indicator = risk_indicator(
            classification
        )

        lines.append(
            "| "
            + result["path"]
            + " | "
            + str(
                complexity_score
            )
            + " | "
            + str(
                risk_score
            )
            + " | "
            + indicator
            + " "
            + classification
            + " |"
        )

    lines.append("")

    # ======================================
    # HIGHEST RISK FUNCTION
    # ======================================

    highest_function = None

    highest_file = None

    for result in results:

        if "error" in result:

            continue

        function = (
            result[
                "risk"
            ][
                "highest_risk_function"
            ]
        )

        if function is None:

            continue

        if (
            highest_function is None
            or
            function["risk_score"]
            >
            highest_function["risk_score"]
        ):

            highest_function = function

            highest_file = result[
                "path"
            ]

    if highest_function is not None:

        lines.append(
            "### 🚨 Highest Risk Function"
        )

        lines.append("")

        lines.append(
            "**Function:** `"
            + str(
                highest_function[
                    "name"
                ]
            )
            + "`"
        )

        lines.append("")

        lines.append(
            "**File:** `"
            + str(
                highest_file
            )
            + "`"
        )

        lines.append("")

        lines.append(
            "**Risk Score:** "
            + str(
                highest_function[
                    "risk_score"
                ]
            )
        )

        lines.append("")

        lines.append(
            "**Classification:** "
            + str(
                highest_function[
                    "classification"
                ]
            )
        )

        explanations = (
            highest_function[
                "explanations"
            ]
        )

        if explanations:

            lines.append("")

            lines.append(
                "**Risk Factors:**"
            )

            for explanation in explanations:

                lines.append(
                    "- "
                    + explanation
                )

    # ======================================
    # ANALYSIS STATISTICS
    # ======================================

    lines.append("")

    lines.append(
        "### 📈 Analysis Statistics"
    )

    lines.append("")

    total_functions = 0

    total_syntax_errors = 0

    for result in results:

        if "error" in result:

            continue

        total_functions += len(
            result[
                "ast"
            ][
                "functions"
            ]
        )

        total_syntax_errors += (
            result[
                "ast"
            ][
                "syntax_errors"
            ]
        )

    lines.append(
        "- **Files analyzed:** "
        + str(
            len(results)
        )
    )

    lines.append(
        "- **Functions analyzed:** "
        + str(
            total_functions
        )
    )

    lines.append(
        "- **Syntax errors:** "
        + str(
            total_syntax_errors
        )
    )

    lines.append("")

    lines.append(
        "---"
    )

    lines.append(
        "*BugRadar automated analysis* 🤖"
    )

    return "\n".join(
        lines
    )


# ==========================================
# POST COMMENT TO GITHUB PR
# ==========================================

def post_pr_comment(
    body
):

    token = os.environ.get(
        "GITHUB_TOKEN"
    )

    repository = os.environ.get(
        "GITHUB_REPOSITORY"
    )

    event = load_github_event()

    pr_info = get_pull_request_info(
        event
    )

    pr_number = pr_info.get(
        "number"
    )

    if not token:

        raise RuntimeError(
            "GITHUB_TOKEN is not available."
        )

    if not repository:

        raise RuntimeError(
            "GITHUB_REPOSITORY is not available."
        )

    if not pr_number:

        raise RuntimeError(
            "Pull request number is not available."
        )

    url = (
        "https://api.github.com/repos/"
        + repository
        + "/issues/"
        + str(pr_number)
        + "/comments"
    )

    payload = json.dumps(
        {
            "body": body
        }
    ).encode(
        "utf-8"
    )

    request_object = request.Request(
        url,
        data=payload,
        method="POST"
    )

    request_object.add_header(
        "Authorization",
        "Bearer "
        + token
    )

    request_object.add_header(
        "Accept",
        "application/vnd.github+json"
    )

    request_object.add_header(
        "X-GitHub-Api-Version",
        "2022-11-28"
    )

    request_object.add_header(
        "Content-Type",
        "application/json"
    )

    try:

        with request.urlopen(
            request_object
        ) as response:

            if response.status not in [
                200,
                201
            ]:

                raise RuntimeError(
                    "GitHub returned HTTP "
                    + str(
                        response.status
                    )
                )

    except HTTPError as error:

        error_body = (
            error.read()
            .decode(
                "utf-8",
                errors="replace"
            )
        )

        raise RuntimeError(
            "GitHub API error "
            + str(
                error.code
            )
            + ": "
            + error_body
        )

    except URLError as error:

        raise RuntimeError(
            "Unable to connect to GitHub: "
            + str(
                error.reason
            )
        )


# ==========================================
# MAIN
# ==========================================

def main():

    print()

    print(
        "========================================"
    )

    print(
        "      BUGRADAR PULL REQUEST ANALYSIS"
    )

    print(
        "========================================"
    )

    event = load_github_event()

    pr_info = get_pull_request_info(
        event
    )

    print()

    print(
        "Pull Request:",
        pr_info.get(
            "number",
            "Unknown"
        )
    )

    print(
        "Title:",
        pr_info.get(
            "title",
            ""
        )
    )

    changed_files = get_changed_files(
        pr_info.get(
            "base_sha"
        ),
        pr_info.get(
            "head_sha"
        )
    )

    print()

    print(
        "Changed files:",
        len(
            changed_files
        )
    )

    source_files = filter_source_files(
        changed_files
    )

    print(
        "Changed C/C++ files:",
        len(
            source_files
        )
    )

    results = analyze_changed_files(
        source_files
    )

    for result in results:

        print()

        print(
            "File:",
            result["path"]
        )

        if "error" in result:

            print(
                "Analysis Error:",
                result["error"]
            )

            continue

        print(
            "Complexity:",
            result[
                "complexity"
            ][
                "file_complexity_score"
            ]
        )

        print(
            "Risk:",
            result[
                "risk"
            ][
                "file_risk_score"
            ]
        )

        print(
            "Classification:",
            result[
                "risk"
            ][
                "file_classification"
            ]
        )

    report = build_pr_report(
        pr_info,
        source_files,
        results
    )

    print()

    print(
        "Posting BugRadar report "
        "to Pull Request..."
    )

    post_pr_comment(
        report
    )

    print()

    print(
        "BugRadar PR comment posted successfully."
    )

    print()

    print(
        "========================================"
    )

    print(
        "       PR ANALYSIS COMPLETED"
    )

    print(
        "========================================"
    )

    return 0


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    raise SystemExit(
        main()
    )