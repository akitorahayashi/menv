#!/bin/bash
alias cpt="copilot"

# Copilot Configuration Management
# Initialize project-specific Copilot configuration
cpt-ini() {
	# Note: .github might already exist for workflows, so we loosen the check or check specifically for the file
    if [ -f .github/copilot-instructions.md ]; then
        echo "❌ .github/copilot-instructions.md already exists"
        return 1
    fi

	# Build basic structure
	mkdir -p .github

	# Link AGENTS.md
    cpt_ln

	echo "✅ Initialized project-specific .copilot configuration"
}

# Link AGENTS.md to .github/copilot-instructions.md
alias cpt-ln=cpt_ln
cpt_ln() {
    # Ensure directory exists
    mkdir -p .github

    # Create relative symlink (force overwrite)
    # Target: ../AGENTS.md (relative from .github/copilot-instructions.md)
    ln -sf ../AGENTS.md .github/copilot-instructions.md

    echo "🔗 Linked .github/copilot-instructions.md -> ../AGENTS.md"
}
