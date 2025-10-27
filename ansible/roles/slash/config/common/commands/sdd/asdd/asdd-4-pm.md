# Generate Prompts

## Role

Prompt Engineer

## Context

- `.tmp/requirements.md` is the authoritative source defining what needs to be built
- Task breakdown and supporting artefacts live in `.tmp/`

## Your task

### 1. Gather the plan inputs

- Open `.tmp/tasks.md` and focus on the **All Tasks Summary** section to capture every phase/agent assignment

### 2. Draft activation messaging

- Turn each checkbox entry into a direct instruction that references `.tmp/tasks.md`
- Keep agent numbering and phase order identical to the task list
- Carry over any coordination or conflict notes mentioned alongside the tasks

### 3. Record the prompts

- Write `.tmp/prompts.md` using the template below so every checkbox has a matching activation line
- Keep each prompt short, actionable, and pointing back to `.tmp/tasks.md`

## Notes

- Do not edit `.tmp/tasks.md` or any other artefact—your sole deliverable is `.tmp/prompts.md`.
- When a phase assigns multiple checklist items to the same agent (e.g., multiple `Task n summary` entries in `sdd-4-tk.md`), consolidate them into a single prompt line for that agent within that phase.

---

```markdown
# Activation Prompts - [Task Name]

## Guidance
- Prompts must stay in sync with `.tmp/tasks.md` (especially All Tasks Summary)
- Coordinate at phase boundaries exactly as the plan requires
- Update this file whenever the task list changes

## Prompts by Phase

### Phase 1
- **Agent 1**: "You are agent1. Read `.tmp/requirements.md`, `.tmp/design.md`, and `.tmp/tasks.md`. Execute Phase 1 tasks assigned to Agent 1."
- **Agent 2**: "You are agent2. Read `.tmp/requirements.md`, `.tmp/design.md`, and `.tmp/tasks.md`. Execute Phase 1 tasks assigned to Agent 2."
- **Agent 3**: "You are agent3. Read `.tmp/requirements.md`, `.tmp/design.md`, and `.tmp/tasks.md`. Execute Phase 1 tasks assigned to Agent 3."
- **Agent 4**: "You are agent4. Read `.tmp/requirements.md`, `.tmp/design.md`, and `.tmp/tasks.md`. Execute Phase 1 tasks assigned to Agent 4."
- **Reviewer**: "Phase 1 agent work complete. Review merged changes, resolve conflicts, verify build and tests pass."

### Phase 2
- **Agent 1**: "Phase 1 integration is complete. Read `.tmp/tasks.md` and execute your Phase 2 tasks for Agent 1."
- **Agent 2**: "Phase 1 integration is complete. Read `.tmp/tasks.md` and execute your Phase 2 tasks for Agent 2."
- **Reviewer**: "Phase 2 agent work complete. Review merged changes, resolve conflicts, verify build and tests pass."

### Phase 3
- **Agent 1**: "Phase 2 integration is complete. Read `.tmp/tasks.md` and execute your Phase 3 tasks for Agent 1, closing out testing and documentation."
- **Agent 2**: "Phase 2 integration is complete. Read `.tmp/tasks.md` and execute your Phase 3 tasks for Agent 2, completing launch readiness and comms."
- **Agent 3**: "Phase 2 integration is complete. Read `.tmp/tasks.md` and execute your Phase 3 tasks for Agent 3."
- **Reviewer**: "Phase 3 agent work complete. Review merged changes, resolve conflicts, verify build and tests pass."
```

Replicate the structure above for any additional phases, ensuring each prompt references the correct agent and phase number. Add a Reviewer prompt after each phase for human orchestration. 