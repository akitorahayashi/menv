---
created_at: "2024-05-20"
author_role: "rustacean"
confidence: "high"
---

## Statement

The `run_playbook` method in `AnsibleAdapter` uses silent fallbacks by defaulting exit codes to `-1` and repo paths to `.` using `unwrap_or`. This violates the principle of explicit error handling and surfacing failures at boundaries, losing important context when processes terminate without an exit code (e.g. by signal) or when the repo path resolution fails.

## Evidence

- path: "src/adapters/ansible/executor.rs"
  loc: "line 82"
  note: "`self.ansible_dir.parent().unwrap_or(Path::new(\".\")).display()` silently defaults to the current directory when the parent path is not available."

- path: "src/adapters/ansible/executor.rs"
  loc: "line 107"
  note: "`code.unwrap_or(-1)` silently defaults an exit code to -1 without differentiating whether it was terminated by a signal or failed."
