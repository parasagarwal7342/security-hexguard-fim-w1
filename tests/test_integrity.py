import pytest
import os
import shutil
import tempfile
from src.integrity_checker import IntegrityChecker

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)

def test_calculate_sha256(temp_dir):
    """Test SHA-256 calculation."""
    checker = IntegrityChecker(temp_dir)
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("hello world")
    
    hash1 = checker.calculate_sha256(test_file)
    assert hash1 is not None
    assert len(hash1) == 64  # SHA-256 is 64 hex chars
    
    # Modify and check
    with open(test_file, "w") as f:
        f.write("hello world!")
    hash2 = checker.calculate_sha256(test_file)
    assert hash1 != hash2

def test_scan_directory(temp_dir):
    """Test directory scanning."""
    checker = IntegrityChecker(temp_dir)
    os.makedirs(os.path.join(temp_dir, "subdir"))
    with open(os.path.join(temp_dir, "f1.txt"), "w") as f: f.write("a")
    with open(os.path.join(temp_dir, "subdir", "f2.txt"), "w") as f: f.write("b")
    
    baseline = checker.scan_directory()
    assert "f1.txt" in baseline
    assert "subdir/f2.txt" in baseline or "subdir\\f2.txt" in baseline
    assert len(baseline) == 2

def test_integrity_verification(temp_dir):
    """Test full integrity flow."""
    checker = IntegrityChecker(temp_dir)
    baseline_file = os.path.join(temp_dir, "baseline.json")
    
    # 1. Baseline creation
    f1 = os.path.join(temp_dir, "f1.txt")
    with open(f1, "w") as f: f.write("original")
    checker.generate_baseline(baseline_file)
    
    # 2. Modify
    with open(f1, "w") as f: f.write("modified")
    
    # 3. Add new
    f2 = os.path.join(temp_dir, "f2.txt")
    with open(f2, "w") as f: f.write("new")
    
    results = checker.verify_integrity(baseline_file)
    assert "f1.txt" in results["modified"]
    assert "f2.txt" in results["new"]
    assert len(results["deleted"]) == 0

def test_ignore_functionality(temp_dir):
    """Test that .fim-ignore works."""
    ignore_file = os.path.join(temp_dir, ".fim-ignore")
    with open(ignore_file, "w") as f:
        f.write("secret\n")
    
    os.makedirs(os.path.join(temp_dir, "secret"))
    with open(os.path.join(temp_dir, "secret", "hush.txt"), "w") as f: f.write("hush")
    with open(os.path.join(temp_dir, "public.txt"), "w") as f: f.write("hi")
    
    checker = IntegrityChecker(temp_dir, ignore_file=".fim-ignore")
    baseline = checker.scan_directory()
    
    assert "public.txt" in baseline
    assert "secret/hush.txt" not in baseline
    assert "secret\\hush.txt" not in baseline
    assert len(baseline) == 1
