
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = {".py", ".json", ".yaml", ".yml", ".toml", ".md", ".mjs", ".js", ".txt", ".cff"}
SKIP = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
PRIVATE = re.compile(r"(?i)([A-Z]:\\Users\\|[A-Z]:\\|/Users/|/home/[^/]+/|12944)")
HIGH_RISK = re.compile(r"(?i)(OPENAI_API_KEY|github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+|sk-[A-Za-z0-9]{12,}|AKIA[A-Z0-9]{12,}|DEEPSEEK\s*[:=])")
ASSIGNMENT = re.compile(r"(?i)(api[_-]?key|apikey|password|passwd|bearer|authorization|cookie|session)\s*[:=]\s*['\"][^'\"]+['\"]")
ALLOW = {"PUBLIC_RELEASE_AUDIT.md", "PUBLIC_RELEASE_SECURITY_REPORT.md", "FINAL_SECURITY_SCAN.md", "final_security_scan.py", "security_scan.py"}
hits = []
notebooks = []
for path in ROOT.rglob("*"):
    if any(part in SKIP for part in path.parts) or not path.is_file():
        continue
    if path.suffix.lower() == ".ipynb": notebooks.append(path.relative_to(ROOT).as_posix())
    if path.suffix.lower() not in TEXT or path.name in ALLOW:
        continue
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if PRIVATE.search(line) or HIGH_RISK.search(line) or ASSIGNMENT.search(line):
            hits.append((path.relative_to(ROOT).as_posix(), line_no))
large = [
    (p.relative_to(ROOT).as_posix(), p.stat().st_size)
    for p in ROOT.rglob("*")
    if p.is_file()
    and not any(part in SKIP for part in p.parts)
    and p.stat().st_size > 10 * 1024 * 1024
]
if hits or notebooks or large:
    print({"sensitive_hits": hits, "notebooks": notebooks, "large_files": large})
    raise SystemExit(1)
print("confirmed_credentials = 0")
print("private_absolute_paths = 0")
print("unreviewed_large_files = 0")
