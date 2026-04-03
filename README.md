# 🛡️ HexGuard — File Integrity Monitor (FIM)
## Week 1: Security Project Release v1.0.0

HexGuard is a lightweight, CLI-based file integrity monitoring tool designed to detect unauthorized changes to specific directories. It generates a cryptographic baseline (SHA-256) of folders and alerts the user to any file modifications, deletions, or new file creations.

---

### 📋 Project Status: ✅ DEPLOYED
This project follows a strict 6-day development lifecycle (Monday-Saturday).

#### Monday — Project Init
- [x] Initialized project structure and planning documentation.

#### Tuesday — Core Logic
- [x] Implemented SHA-256 hashing and recursive directory scanning.

#### Wednesday — Features + Edge Cases
- [x] Added `.fim-ignore` support and dual-stream forensic logging.

#### Thursday — Testing + Polish
- [x] Verified logic with 100% passing Pytest suite (4 core items).

#### Friday — Documentation + Deploy
- [x] Finalized documentation, tagged release `v1.0.0`, and deployed.

---

### ⚙️ Installation
1. Clone the repository:
```bash
git clone https://github.com/parasagarwal7342/security-hexguard-fim-w1.git
cd security-hexguard-fim-w1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

---

### 🚀 Usage Guide

#### Step 1: Create a Baseline
Generate a cryptographic snapshot of your target directory:
```bash
python src/main.py --init sample_input
```

#### Step 2: Verify Integrity
Check the current state against your baseline:
```bash
python src/main.py --check sample_input
```

#### Step 3: Use Ignore Lists
Create a `.fim-ignore` file in the root to skip specific paths:
```bash
echo "secret.txt" > .fim-ignore
python src/main.py --check sample_input
```

---

### 🔍 Forensic Logs
All scan events are recorded in `hexguard.log` for audit purposes:
```text
2026-04-03 22:15:21 - INFO - Scanning directory: sample_input
2026-04-03 22:15:21 - INFO - No violations detected.
```

---

### 🧪 Educational Use Only
> **⚠️ Disclaimer:** This tool is designed for educational purposes and personal file monitoring. While its hashing logic is robust, it is not a substitution for advanced EDR or corporate-grade File Integrity Monitoring systems. Use responsibly.

---

### 📄 License
MIT License - Paras Agarwal (2026)
