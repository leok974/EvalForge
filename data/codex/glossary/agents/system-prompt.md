# System Prompt

## Definition
A **System Prompt** is the highest-priority instruction to the assistant. It defines the rules of behavior: what the assistant is, what it must do, what it must not do, and how it should format outputs. If a user instruction conflicts with the system prompt, the system prompt wins.

## Tiny example
If the system prompt says “Return only JSON,” then the assistant should not output prose, even if the user asks for “a short paragraph.”

## Common pitfall
Putting the entire task in the system prompt makes prompts hard to reuse and can cause unintended behavior. Keep the system prompt for **rules + boundaries**, and put the specific task and data in the user prompt.

## Related
User Prompt, Instruction Hierarchy, Output Schema
