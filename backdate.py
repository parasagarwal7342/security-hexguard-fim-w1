import subprocess
import random
import os
from datetime import datetime, timedelta

# ─── CONFIGURATION ──────────────────────────────────────
START_DATE     = "2025-09-07"   # Start of backdate range
END_DATE       = "2026-04-03"   # End of backdate range
MIN_COMMITS    = 2              # Min commits on active day
MAX_COMMITS    = 8              # Max commits on active day
SKIP_WEEKENDS  = False          # True = no weekend commits
COMMIT_CHANCE  = 0.75           # 75% chance to commit on any day
LOG_FILE       = "activity.log" # File to update each commit
# ────────────────────────────────────────────────────────

COMMIT_MESSAGES = [
  "feat: improve module structure",
  "fix: resolve edge case in parser",
  "refactor: clean up utility functions",
  "docs: update inline comments",
  "chore: update dependencies",
  "test: add command coverage",
  "feat: add validation layer",
  "fix: handle null response",
  "refactor: simplify logic",
  "docs: improve README",
  "chore: remove imports",
  "feat: extend config",
  "fix: correct error",
  "test: add edge cases",
  "refactor: rename variables",
  "ci: update trigger rules",
  "feat: add retry mechanism",
  "fix: patch security",
  "docs: add examples",
  "chore: format with linter",
]

def run(cmd):
    # Specialized for Windows PowerShell based on the user's OS metadata
    subprocess.run(["pwsh", "-Command", cmd], check=True)

def backdate_commits():
    start = datetime.strptime(START_DATE, "%Y-%m-%d")
    end   = datetime.now() # Until now
    current = start
    total_commits = 0

    # Initialize log file
    with open(LOG_FILE, "w") as f:
        f.write("# Activity Log\n")
    
    run(f"git add {LOG_FILE}")
    run('git commit -m "chore: init activity log"')

    while current <= end:
        # Skip weekends if configured
        if SKIP_WEEKENDS and current.weekday() >= 5:
            current += timedelta(days=1)
            continue

        # Randomly skip some days for natural look
        if random.random() > COMMIT_CHANCE:
            current += timedelta(days=1)
            continue

        # Random number of commits for this day
        num_commits = random.randint(MIN_COMMITS, MAX_COMMITS)

        for i in range(num_commits):
            hour   = random.randint(8, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            commit_dt = current.replace(
                hour=hour, minute=minute, second=second
            )
            date_str = commit_dt.strftime("%Y-%m-%dT%H:%M:%S")

            with open(LOG_FILE, "a") as f:
                f.write(f"\n[{date_str}] - commit {i+1}/{num_commits}")

            msg = random.choice(COMMIT_MESSAGES)

            run(f"git add {LOG_FILE}")
            
            # PowerShell environment variable setting syntax
            ps_cmd = (
                f'$env:GIT_AUTHOR_DATE="{date_str}"; '
                f'$env:GIT_COMMITTER_DATE="{date_str}"; '
                f'git commit -m "{msg}"'
            )
            run(ps_cmd)
            total_commits += 1

        print(f"✅ {current.strftime('%Y-%m-%d')} — {num_commits} commits")
        current += timedelta(days=1)

    # Push everything to GitHub
    run("git push origin main")
    print(f"\n🎉 Done! Total commits pushed: {total_commits}")

if __name__ == "__main__":
    backdate_commits()
