"""Fail closed when required QuantSyariah source files are missing."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "settings.gradle.kts", "build.gradle.kts", "app/build.gradle.kts",
    "app/src/main/AndroidManifest.xml",
    "app/src/main/java/id/quantsyariah/MainActivity.kt",
    "app/src/main/java/id/quantsyariah/Engine.kt",
    "backend/server.py", "backend/requirements.txt",
    "tests/test_kotlin_engine_runtime.py",
]
def check(root=ROOT):
    missing = [name for name in REQUIRED if not (root / name).is_file()]
    unsafe = [name for name in (".env", "local.properties") if (root / name).exists()]
    for name in missing:
        print("ERROR: Missing required source file:", name)
    for name in unsafe:
        print("ERROR: Local credential/config file must not be committed:", name)
    if not missing and not unsafe:
        print("PASS: Required source files are present; APK build still required.")
    return not missing and not unsafe
if __name__ == "__main__":
    sys.exit(0 if check() else 1)
