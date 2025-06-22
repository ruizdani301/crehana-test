import sys
from pathlib import Path

# Añade el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))