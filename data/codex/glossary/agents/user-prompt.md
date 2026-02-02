# User Prompt

## Definition
A **User Prompt** is the task request and inputs provided by the user. It describes what to do now: the goal, constraints, data, and acceptance criteria. It sits below the system prompt in priority.

## Tiny example
“Summarize this text in 3 bullet points. Text: …” is a user prompt. It contains the task and the input.

## Common pitfall
If the user prompt doesn’t specify output shape (like JSON keys or bullet count), the assistant will fill gaps with assumptions. Add constraints that are measurable: “3 bullets,” “max 1 sentence each,” or a JSON schema.

## Related
System Prompt, Output Schema
