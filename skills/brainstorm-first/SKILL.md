---
name: brainstorm-first
description: Design before code: draw out intent, size the work, compare 2-3 approaches, write a short design, get approval. Use before any new feature or project, when the request is vague, or when the work is bigger than a small change.
---
# Brainstorm first

People often have not finished deciding what they want. Good questions help them
decide; the agent makes the hundred small decisions later the way they would have.

## Hard gate

Do not write code, scaffold, or take implementation actions until a design is
presented and approved. This applies regardless of how simple the change looks.
A "small change" still gets a one-paragraph design, agreed in chat.

## Look before you ask

Read what they pointed at: the repo, the spec, the files, the earlier messages.
Keep reading until you can say how the relevant parts work today and what the
change would touch. Never ask what the project already answers.

## Ask one question at a time

Ask only when the answer changes what gets built and neither the request nor the
project answers it. Otherwise state your call with a one-line reason and move on.
Pick plain language, match their vocabulary, no process jargon.

## Size the work

| Size | Design |
|---|---|
| Small change | a short note: what we agreed and what it touches |
| Project | a written design a builder could plan from |

If it grows mid-task, stop, say so, and step up a size.

## The written design

- intent and the why; goals, non-goals, anti-goals
- constraints
- **approaches:** two or three ways, what each trades off, which was picked and why
  (the owner picks, not the agent, for architecture)
- the parts decided in conversation, as decided
- what is left to the builder

## Anti-patterns

- Jumping to implementation because "it's obvious".
- Asking ten questions at once; asking questions the repo answers.
- Presenting one approach as if there were no alternatives.
- Writing a design nobody can verify; every goal must be testable.
