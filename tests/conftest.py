# ==========================================
# BUGRADAR PYTEST CONFIGURATION
# ==========================================

import sys
from pathlib import Path


# ==========================================
# PROJECT ROOT DIRECTORY
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ==========================================
# ADD PROJECT ROOT TO PYTHON PATH
# ==========================================

project_root_string = str(
    PROJECT_ROOT
)


if project_root_string not in sys.path:

    sys.path.insert(
        0,
        project_root_string
    )