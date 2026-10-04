from fastapi.testclient import (
    TestClient
)

from backend.app import app


# ==========================================
# TEST CLIENT
# ==========================================

client = TestClient(
    app
)


# ==========================================
# SAMPLE C++ CODE
# ==========================================

SAMPLE_CODE = """
#include <iostream>

int calculate(int a, int b)
{
    if (a > 10)
    {
        return a + b;
    }

    return a - b;
}

int main()
{
    int result = calculate(10, 20);

    std::cout << result;

    return 0;
}
"""


# ==========================================
# ROOT ENDPOINT TEST
# ==========================================

def test_root():

    response = client.get(
        "/"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "BugRadar API"

    assert data["status"] == "running"


# ==========================================
# HEALTH ENDPOINT TEST
# ==========================================

def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


# ==========================================
# ANALYSIS ENDPOINT TEST
# ==========================================

def test_analyze():

    response = client.post(

        "/analyze",

        json={
            "filename": "sample.cpp",

            "code": SAMPLE_CODE
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert data["filename"] == "sample.cpp"

    assert "syntax_errors" in data

    assert "basic_metrics" in data

    assert "ast_metrics" in data

    assert "complexity" in data

    assert "risk" in data


# ==========================================
# INVALID FILE TYPE TEST
# ==========================================

def test_invalid_file_type():

    response = client.post(

        "/analyze",

        json={
            "filename": "sample.py",

            "code": SAMPLE_CODE
        }
    )

    assert response.status_code == 400


# ==========================================
# EMPTY CODE TEST
# ==========================================

def test_empty_code():

    response = client.post(

        "/analyze",

        json={
            "filename": "sample.cpp",

            "code": ""
        }
    )

    assert response.status_code == 422