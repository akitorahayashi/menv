#!/bin/bash
alias cld="claude"
alias cld-y="claude --dangerously-skip-permissions"
alias cld-p="claude --print"
alias cld-yp="claude --dangerously-skip-permissions --print"

# MCP
alias cld-m-st="claude mcp serve"
alias cld-m-a="claude mcp add"
alias cld-m-rm="claude mcp remove"
alias cld-m-ls="claude mcp list"

# Link README.md to .claude/CLAUDE.md
alias cld-ln=cld_ln
cld_ln() {
	if [ ! -f "README.md" ]; then
		echo "❌ README.md not found in the project root. Please run this command from the repository root." >&2
		return 1
	fi

	# Ensure directory exists
	mkdir -p .claude

	# Create relative symlink (force overwrite)
	# Target: ../README.md (relative from .claude/CLAUDE.md)
	ln -sf ../README.md .claude/CLAUDE.md

	echo "🔗 Linked .claude/CLAUDE.md -> ../README.md"
}

alias cdx="codex"

alias cpt="copilot"

# Generate Gemini model aliases
eval "$(gen_gemini_aliases.py)"

# Basic gm alias
alias gm="gemini"
