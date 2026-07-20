---
name: efficient-action
description: "Use when: you need to do more work with fewer tokens, fewer tool calls, and less credit usage."
---

# Efficient Action

Use this skill when the goal is to maximize progress while minimizing cost, verbosity, and unnecessary back-and-forth.

## Core Principles

- Prefer the next useful action over a long explanation.
- Favor one strong step that advances the task instead of many small conversational steps.
- Reuse existing context instead of restating it.
- Keep responses concise, direct, and outcome-focused.
- Do the minimum necessary verification to confirm the result.

## Workflow

1. Identify the highest-value next action.
   - Choose the step that most directly moves the task forward.
   - Avoid planning overhead when implementation is possible.

2. Act first, then refine.
   - Make the change, run the smallest relevant check, and adjust only if needed.
   - Do not wait for perfect conditions before taking a useful step.

3. Batch related work.
   - Combine edits, checks, or requests when they belong to the same task.
   - Reduce repeated tool calls and repeated context loading.

4. Keep communication lean.
   - Use short updates, compact summaries, and clear next steps.
   - Avoid filler, long apologies, or redundant explanations.

5. Verify with the lightest useful test.
   - Prefer a targeted check over a broad one when the task is localized.
   - Stop once the result is confirmed and the goal is met.

## Decision Guide

- If the task is clear and actionable, execute it directly.
- If the task needs multiple steps, do them in a compact sequence rather than a long discussion.
- If there is uncertainty, resolve it with the smallest possible probe rather than a large exploration pass.
- If polishing would cost more than value, defer it until the core outcome is complete.

## Completion Checks

- The task moved forward in a meaningful way.
- The response stayed concise and avoided unnecessary token spend.
- The result was verified with a minimal, relevant check.
- No extra work was done beyond the stated goal.
