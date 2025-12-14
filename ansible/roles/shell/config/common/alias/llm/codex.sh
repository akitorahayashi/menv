#!/bin/bash
alias cdx="codex"

# Codex Configuration Management
# Initialize project-specific Codex configuration
cdx-ini() {
	# Guard clause: Verify prerequisites
	if [ -d .codex ]; then
		echo "❌ .codex directory already exists in current directory"
		return 1
	fi

	# Build basic structure
	mkdir -p .codex

	# Link AGENTS.md
    cdx_ln

	echo "✅ Initialized project-specific .codex configuration"
}

# Link AGENTS.md to .codex/AGENTS.md
alias cdx-ln=cdx_ln
cdx_ln() {
    if [ ! -f "AGENTS.md" ]; then
        echo "❌ AGENTS.md not found in the project root. Please run this command from the repository root." >&2
        return 1
    fi

    # Ensure directory exists
    mkdir -p .codex

    # Create relative symlink (force overwrite)
    # Target: ../AGENTS.md (relative from .codex/AGENTS.md)
    ln -sf ../AGENTS.md .codex/AGENTS.md

    echo "🔗 Linked .codex/AGENTS.md -> ../AGENTS.md"
}
