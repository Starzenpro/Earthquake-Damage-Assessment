"""
Project Configuration Module
Handles all paths and configuration settings for the project
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    load_dotenv(env_file)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

# Create directories if they don't exist
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR,
                 REPORTS_DIR, FIGURES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Data settings
TARGET_COLUMN = "severe_damage"
TEST_SIZE = 0.2
RANDOM_STATE = int(os.getenv("RANDOM_SEED", "42"))
SAMPLE_SIZE = int(os.getenv("SAMPLE_SIZE", "10000"))

# Visualization settings
PLOT_DPI = 300
FIGURE_SIZE = (12, 8)
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'warning': '#C73E1D',
    'success': '#4C9A8A',
    'neutral': '#6C757D'
}

# Damage severity levels
DAMAGE_LEVELS = list(range(1, 11))
DAMAGE_LABELS = [f'Level {i}' for i in DAMAGE_LEVELS]

# Default distribution for sample data
# Realistic imbalanced distribution
DEFAULT_DISTRIBUTION = [0.05, 0.08, 0.12, 0.15, 0.18, 
                        0.15, 0.12, 0.08, 0.05, 0.02]

def get_config():
    """Return all configuration as a dictionary"""
    return {
        'PROJECT_ROOT': PROJECT_ROOT,
        'DATA_DIR': DATA_DIR,
        'RAW_DATA_DIR': RAW_DATA_DIR,
        'TARGET_COLUMN': TARGET_COLUMN,
        'RANDOM_STATE': RANDOM_STATE,
        'SAMPLE_SIZE': SAMPLE_SIZE,
        'DAMAGE_LEVELS': DAMAGE_LEVELS,
        'DAMAGE_LABELS': DAMAGE_LABELS,
        'DEFAULT_DISTRIBUTION': DEFAULT_DISTRIBUTION,
        'COLORS': COLORS
    }

if __name__ == "__main__":
    print("✅ Configuration loaded successfully")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Random State: {RANDOM_STATE}")
    print(f"Sample Size: {SAMPLE_SIZE}")
