# 🛡️ HexGuard — File Integrity Monitor (FIM)
## Week 1: Security Project

HexGuard is a lightweight, CLI-based file integrity monitoring tool designed to detect unauthorized changes to specific directories. It generates a cryptographic baseline (SHA-256) of folders and alerts the user to any file modifications, deletions, or new file creations.

---

### 📋 Project Plan

#### Monday — Project Init
- [x] Choose the week's project (Security: File Integrity Monitor)
- [x] Create project structure
- [x] Initialize README.md, .gitignore, and LICENSE
- [x] Commit: "chore: project init and planning docs"

#### Tuesday — Core Logic
- [x] Implement hashing function (SHA-256)
- [x] Develop recursive directory scanner
- [x] Implement baseline storage (JSON-based)
- [x] Commit: "feat: implement core scanning and hashing logic"

#### Wednesday — Features + Edge Cases
- [x] Add CLI arguments using `argparse` (init, check, status)
- [x] Implement ignore-list functionality (.fim-ignore)
- [x] Handle permission errors and missing files
- [x] Commit: "feat: add CLI interface and error handling"

#### Thursday — Testing + Polish
- [x] Write unit tests for hashing and scanner logic
- [x] Add logging support for security events
- [x] Refactor for clean, modular code
- [x] Commit: "test: add unit tests | refactor: clean up code"

#### Friday — Documentation + Deploy
- [ ] Finalize README with installation and usage guide
- [ ] Add `requirements.txt`
- [ ] Create a sample test environment
- [ ] Tag release v1.0.0
- [ ] Commit: "docs: finalize README | release: v1.0.0"

#### Saturday — Post-Deploy Improvements
- [ ] Add GitHub Actions CI for linting and testing
- [ ] Implement a simple HTML/Rich-CLI reporting feature
- [ ] Add `CONTRIBUTING.md`
- [ ] Commit: "ci: add GitHub Actions workflow"

---

### ⚙️ Tech Stack
- **Language:** Python 3.10+
- **Security:** `hashlib`, `cryptography` (for secure baseline storage)
- **CLI:** `argparse` / `click`
- **Testing:** `pytest`
- **Logging:** `logging` module

---

### 🚀 Usage (Internal Use Only)
> **Disclaimer:** This tool is for educational use and personal file monitoring. Use responsibly and do not run on sensitive system directories without proper backup.

```bash
python src/main.py --init /path/to/watch
python src/main.py --check
```
