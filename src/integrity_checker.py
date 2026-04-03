import hashlib
import os
import json
import logging

class IntegrityChecker:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.baseline = {}
        self.logger = logging.getLogger("HexGuard")

    def calculate_sha256(self, file_path):
        """Calculates the SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (PermissionError, FileNotFoundError) as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return None

    def scan_directory(self):
        """Recursively scans the directory and returns a map of file:hash."""
        current_baseline = {}
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip the baseline file itself if it's in the same dir
                if file == "baseline.json" or file == ".git":
                    continue
                file_hash = self.calculate_sha256(file_path)
                if file_hash:
                    # Use relative path as key
                    rel_path = os.path.relpath(file_path, self.root_dir)
                    current_baseline[rel_path] = file_hash
        return current_baseline

    def generate_baseline(self, baseline_file="baseline.json"):
        """Generates a baseline and saves it to a file."""
        self.baseline = self.scan_directory()
        with open(baseline_file, "w") as f:
            json.dump(self.baseline, f, indent=4)
        print(f"[+] Baseline generated with {len(self.baseline)} files.")

    def verify_integrity(self, baseline_file="baseline.json"):
        """Compares current state with the saved baseline."""
        if not os.path.exists(baseline_file):
            print("[-] Error: Baseline file not found. Run with --init first.")
            return

        with open(baseline_file, "r") as f:
            saved_baseline = json.load(f)

        current_baseline = self.scan_directory()
        
        modified = []
        deleted = []
        new_files = []

        # Check for modifications and deletions
        for file_path, saved_hash in saved_baseline.items():
            if file_path not in current_baseline:
                deleted.append(file_path)
            elif current_baseline[file_path] != saved_hash:
                modified.append(file_path)

        # Check for new files
        for file_path in current_baseline.keys():
            if file_path not in saved_baseline:
                new_files.append(file_path)

        return {
            "modified": modified,
            "deleted": deleted,
            "new": new_files
        }
