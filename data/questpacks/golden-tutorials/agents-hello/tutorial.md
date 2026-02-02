## Outcome
You will learn how an agent prompt is structured (roles, message order, and constraints) so you can reliably “ask for the right thing” and get predictable outputs.

## Concept in 30 seconds
Think of an agent prompt like a contract: you are defining the rules of the conversation and what counts as a correct response. The most important idea is **message roles + ordering**. The model reads messages in order and uses the **System Prompt** as the highest-level rules. If you want consistent behavior, keep instructions clear, scoped, and explicit about output format.

## Key terms
- **System Prompt**: Top-level rules the assistant should follow.
- **User Prompt**: The task request and inputs (what you want done).
- **Instruction Hierarchy**: Which instructions win when messages conflict (System > User).
- **Output Schema**: A structured shape (like JSON) that the response must follow.
- **Determinism**: Reducing randomness so repeated runs produce similar outputs.

## Walkthrough
1) Read the quest’s objective and identify the “contract”: what must the assistant output and what must it avoid?
2) Put the unbreakable rules in the **System Prompt** (format, safety boundaries, scope).
3) Put the specific request + data in the **User Prompt** (inputs, examples, acceptance criteria).
4) Make the output shape explicit (e.g., “Return JSON with keys: …”).
5) Click **Run** to sanity-check: does the response match the schema and constraints?
6) Iterate: small edits, re-run, confirm the assistant follows the hierarchy.
7) Use **Submit** only when the output consistently matches requirements.

## Example implementation
Here’s a minimal “prompt anatomy” example using a messages array. The key is: System sets rules, User asks the task, Output schema is explicit.

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a strict JSON generator. Return only JSON. If unsure, return {\"error\":\"insufficient_info\"}."
    },
    {
      "role": "user",
      "content": "Summarize this text in 3 bullet points. Text: \"Cats are curious animals...\""
    }
  ],
  "response_format": {
    "type": "json_schema",
    "schema": {
      "type": "object",
      "properties": {
        "bullets": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 3 }
      },
      "required": ["bullets"],
      "additionalProperties": false
    }
  }
}
```

## Common mistakes
- **Writing the task in the System Prompt** (makes reuse harder). Put rules in System, task in User.
- **Forgetting to specify output format** (“Return JSON only”). The model will default to prose.
- **Mixing multiple goals in one prompt** without prioritizing (leads to partial compliance).
- **Making constraints vague** (“Be concise”) without measurable limits (like bullet count).
- **Changing too many instructions at once**; do small edits and re-run.

## Check yourself
- Which role should contain “Return only JSON” and why?
- What happens if the System Prompt and User Prompt conflict?
- How does an output schema reduce ambiguity?
