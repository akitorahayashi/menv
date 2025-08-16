# Makefile for tool installers

# Shell settings
SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

# Directories
export REPO_ROOT := $(CURDIR)
SCRIPT_DIR := $(REPO_ROOT)/scripts
CONFIG_DIR := $(REPO_ROOT)/config

# Configuration
MACHINES := macbook mac-mini
COMPONENTS := brew git vscode ruby python java flutter node

# Default target
.DEFAULT_GOAL := help

# Help command to display available targets
.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS=":.*## "; OFS=" "} /^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# === Dynamic Target Generation ===

# Template for generating rules for a single machine and component
define COMPONENT_template
.PHONY: $(1)-$(2)
$(1)-$(2): ## Setup $(2) for $(1) (common + specific)
	@echo "🚀 Running $(2) setup for $(1)..."
	@$(SHELL) -euo pipefail "$(SCRIPT_DIR)/$(2).sh" "$(CONFIG_DIR)/common" "$(CONFIG_DIR)/$(1)"

.PHONY: only-$(1)-$(2)
only-$(1)-$(2): ## Setup $(2) for $(1) (specific only)
	@echo "🚀 Running $(2) setup for $(1) (specific only)..."
	@$(SHELL) -euo pipefail "$(SCRIPT_DIR)/$(2).sh" "$(CONFIG_DIR)/$(1)"

endef

# Instantiate the template for each machine and component
$(foreach machine,$(MACHINES),$(foreach component,$(COMPONENTS),$(eval $(call COMPONENT_template,$(machine),$(component)))))

# === Aggregate Targets ===

# Generate 'all' target for each machine
$(foreach machine,$(MACHINES),$(eval .PHONY: $(machine)-all) $(eval $(machine)-all: $(addprefix $(machine)-,$(COMPONENTS))))
$(foreach machine,$(MACHINES),$(eval $(machine)-all: ## Setup all components for $(machine)))

# A new default 'all' target that runs the setup for a specific machine (e.g., macbook)
.PHONY: all
all: macbook-all ## Run all setup scripts for MacBook by default

# For backward compatibility, create simple targets that default to macbook
$(foreach component,$(COMPONENTS),$(eval .PHONY: $(component)) $(eval $(component): macbook-$(component)))
$(foreach component,$(COMPONENTS),$(eval $(component): ## Setup $(component) for MacBook (default)))
