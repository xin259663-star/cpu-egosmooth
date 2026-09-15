from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reproduce_figures import reproduce
if __name__ == "__main__": reproduce(5, Path("."))
