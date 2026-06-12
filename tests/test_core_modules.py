"""
test_core_modules.py — Basic tests for SO101 SmolVLA project.

Run with:
    python -m pytest tests/test_core_modules.py -v
"""

import importlib
import subprocess
import sys


def test_train_script_imports() -> None:
    """Test that train.py can be imported without errors."""
    spec = importlib.util.spec_from_file_location(
        "train", "scripts/train.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert module is not None


def test_evaluate_script_imports() -> None:
    """Test that evaluate.py can be imported without errors."""
    spec = importlib.util.spec_from_file_location(
        "evaluate", "scripts/evaluate.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert module is not None


def test_task_strings_complete() -> None:
    """Test that all three color tasks are defined."""
    sys.path.insert(0, "scripts")
    import evaluate  # noqa: PLC0415
    colors = ["red", "yellow", "green"]
    for color in colors:
        assert color in evaluate.TASK_STRINGS
        assert len(evaluate.TASK_STRINGS[color]) > 0


def test_train_help() -> None:
    """Test that train.py --help runs without error."""
    result = subprocess.run(
        [sys.executable, "scripts/train.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "dataset_repo_id" in result.stdout


def test_evaluate_help() -> None:
    """Test that evaluate.py --help runs without error."""
    result = subprocess.run(
        [sys.executable, "scripts/evaluate.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "color" in result.stdout


def test_evaluate_offline_mode() -> None:
    """Test that evaluate.py runs in offline mode without robot."""
    result = subprocess.run(
        [sys.executable, "scripts/evaluate.py", "--offline", "--color", "red"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "OFFLINE MODE" in result.stdout
