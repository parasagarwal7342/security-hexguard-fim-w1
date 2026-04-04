import hashlib
import os
import json
import logging
import math
import shutil
from datetime import datetime

class IntegrityChecker:
    def __init__(self, root_dir, ignore_file=".fim-ignore"):
        self.root_dir = os.path.abspath(root_dir)
        self.vault_dir = os.path.join(self.root_dir, ".fim-vault")
        self.baseline = {}
        self.ignore_list = self._load_ignore_list(ignore_file)
        self._setup_logging()
        self._ensure_vault()

    def _ensure_vault(self):
        """Ensures the secure backup vault exists."""
        if not os.path.exists(self.vault_dir):
            os.makedirs(self.vault_dir)

    def calculate_entropy(self, file_path):
        """Calculates Shannon Entropy of a file to detect potential encryption/ransomware."""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                if not data: return 0
                entropy = 0
                # Fast counting for 256 byte values
                counts = [0] * 256
                for byte in data:
                    counts[byte] += 1
                
                L = len(data)
                for count in counts:
                    if count > 0:
                        p_x = float(count) / L
                        entropy -= p_x * math.log(p_x, 2)
                return entropy
        except Exception: return 0

    def backup_file(self, rel_path):
        """Backs up a file to the secure vault."""
        src = os.path.join(self.root_dir, rel_path)
        dest = os.path.join(self.vault_dir, rel_path.replace(os.sep, "_") + ".bak")
        try:
            shutil.copy2(src, dest)
        except Exception as e:
            self.logger.error(f"Backup failed for {rel_path}: {e}")

    def restore_file(self, rel_path):
        """Restores a file from the vault (Self-Healing)."""
        src = os.path.join(self.vault_dir, rel_path.replace(os.sep, "_") + ".bak")
        dest = os.path.join(self.root_dir, rel_path)
        if os.path.exists(src):
            shutil.copy2(src, dest)
            self.logger.info(f"🛡️ SELF-HEALING: Restored {rel_path} from secure vault.")
            return True
        return False

    def _setup_logging(self):
        """Sets up dual logging to console and file."""
        self.logger = logging.getLogger("HexGuard")
        self.logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
            # File handler
            fh = logging.FileHandler("hexguard.log")
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)
            
            # Console handler
            ch = logging.StreamHandler()
            ch.setFormatter(fmt)
            self.logger.addHandler(ch)

    def _load_ignore_list(self, ignore_file):
        """Loads a list of ignored files/directories from a file."""
        ignore_path = os.path.join(self.root_dir, ignore_file)
        ignores = {".git", "baseline.json", "hexguard.log", ".fim-ignore"}
        if os.path.exists(ignore_path):
            with open(ignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        ignores.add(line)
        return list(ignores)

    def _is_ignored(self, rel_path):
        """Checks if a relative path should be ignored."""
        for pattern in self.ignore_list:
            if rel_path == pattern or rel_path.startswith(pattern + os.sep) or rel_path.startswith(pattern + "/"):
                return True
        return False

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
        """Recursively scans the directory and returns a map of file:attributes."""
        current_baseline = {}
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.root_dir)
                
                if self._is_ignored(rel_path) or ".fim-vault" in rel_path:
                    continue
                    
                file_hash = self.calculate_sha256(file_path)
                if file_hash:
                    entropy = self.calculate_entropy(file_path)
                    current_baseline[rel_path] = {
                        "hash": file_hash,
                        "entropy": entropy,
                        "timestamp": os.path.getmtime(file_path)
                    }
        return current_baseline

    def generate_baseline(self, baseline_file="baseline.json"):
        """Generates a baseline and proactively backs up all files to the secure vault."""
        self.baseline = self.scan_directory()
        for rel_path in self.baseline.keys():
            self.backup_file(rel_path)
            
        with open(baseline_file, "w") as f:
            json.dump(self.baseline, f, indent=4)
        self.logger.info(f"✅ BASELINE SECURED: {len(self.baseline)} files protected and backed up in vault.")

    def verify_integrity(self, baseline_file="baseline.json"):
        """Compares current state with the saved baseline, performing entropy forensic analysis."""
        if not os.path.exists(baseline_file):
            self.logger.error("[-] Error: Baseline file not found.")
            return None

        with open(baseline_file, "r") as f:
            saved_baseline = json.load(f)

        current_baseline = self.scan_directory()
        
        modified = []
        deleted = []
        new_files = []
        ransomware_alerts = []

        # Check for modifications and deletions
        for file_path, saved_meta in saved_baseline.items():
            if file_path not in current_baseline:
                deleted.append(file_path)
            else:
                curr_meta = current_baseline[file_path]
                if curr_meta["hash"] != saved_meta["hash"]:
                    modified.append(file_path)
                    # Forensic: Check for high entropy spikes (> 10% increase and > 7.5 total)
                    if curr_meta["entropy"] > 7.5 and curr_meta["entropy"] > saved_meta["entropy"] * 1.1:
                        ransomware_alerts.append(file_path)
                        self.logger.critical(f"🚨 RANSOMWARE ALERT: {file_path} shows high entropy spike ({curr_meta['entropy']:.2f})!")

        # Check for new files
        for file_path in current_baseline.keys():
            if file_path not in saved_baseline:
                new_files.append(file_path)

        return {
            "modified": modified,
            "deleted": deleted,
            "new": new_files,
            "ransomware": ransomware_alerts
        }
