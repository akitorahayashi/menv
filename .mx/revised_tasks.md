# Revised Tasks - SSOT Agent Skills Deployment

## Goal
Establish a single source of truth for Agent Skills, deploy them to Codex/Claude/Gemini via Ansible, and cover the changes with tests and documentation.

## Scope Review
- Add SSOT skills directory under the nodejs coder config tree.
- Avoid hardcoded enumerations by loading the target CLI list from configuration and discovering skills dynamically.
- Extend Ansible tasks to deploy skills to each CLI.
- Add integration tests for the new config artifacts.
- Update README usage notes to reflect Agent Skills deployment.

## Planned Deliverables
### Code
1. Add common skills directory under src/menv/ansible/roles/nodejs/config/common/coder/skills with the svo-cli-design skill.
2. Add skills-targets.yml to define CLI targets for deployment.
3. Update src/menv/ansible/roles/nodejs/tasks/coder.yml to load targets, discover skills, and deploy symlinks.

### Tests
4. Add tests/intg/roles/nodejs/ to validate:
   - Skills directory exists and contains at least one skill with SKILL.md.
   - Optional agents metadata presence is consistent (openai.yaml if agents/ exists).
   - skills-targets.yml schema is valid.

### Documentation
5. Update README usage notes to mention Agent Skills deployment and the SSOT location.

## Execution Order
1. Implement code changes (SSOT directory, targets config, Ansible tasks).
2. Add integration tests for skills config.
3. Update README.
4. Run tests (just test or just intg-test).
