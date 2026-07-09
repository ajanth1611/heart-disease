from pathlib import Path
import runpy


page_path = Path(__file__).resolve().parent / "pages" / "3_Model_Performance.py"
runpy.run_path(str(page_path), run_name="__main__")
