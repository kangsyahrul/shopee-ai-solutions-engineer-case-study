"""pytest configuration file."""
import sys
import os

# Add the scripts directory to Python path for testing
scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)