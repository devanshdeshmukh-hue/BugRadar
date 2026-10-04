from fastapi import (
    FastAPI,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.schemas import (
    AnalyzeRequest,
    AnalyzeResponse
)

from backend.service import (
    analyze_source
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(

    title="BugRadar API",

    description=(
        "Backend API for BugRadar source-code "
        "complexity and bug-risk analysis."
    ),

    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():

    return {

        "name": "BugRadar API",

        "version": "1.0.0",

        "status": "running"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {

        "status": "healthy",

        "service": "BugRadar Backend"
    }


# ==========================================
# SOURCE CODE ANALYSIS
# ==========================================

@app.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze(
    request: AnalyzeRequest
):

    try:

        result = analyze_source(

            code=request.code,

            filename=request.filename
        )

        return result

    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(
                error
            )
        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                "BugRadar analysis failed: "
                + str(error)
            )
        )