#!/bin/sh
# Generate Gemini model aliases
if [ -f "$MENV_DIR/ansible/scripts/shell/gen_gemini_aliases.py" ]; then
	eval "$(gen_gemini_aliases.py)"
fi

# Basic gm alias (defaults to flash model)
alias gm="gemini -m gemini-2.5-flash"

# Gemini Configuration Management
# Initialize project-specific Gemini configuration
alias gm-ini=gm_ini
gm_ini() {
	# Guard clause: Verify prerequisites
	if [ -d .gemini ]; then
		echo "❌ .gemini directory already exists in current directory"
		return 1
	fi

	# Build basic structure
	mkdir -p .gemini/commands

	# Generate initial configuration file
	echo '{}' >.gemini/settings.json
	touch .gemini/GEMINI.md

	echo "✅ Initialized project-specific .gemini configuration"
}
