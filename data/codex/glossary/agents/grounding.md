# Grounding

## Definition
**Grounding** means constraining an answer to evidence you provide (retrieved chunks, rules, or a dataset). A grounded response should be explainable: “this claim comes from this source.”

## Tiny example
If the retrieved context doesn’t mention pricing, the assistant should say “Not in the provided sources,” rather than inventing a price.

## Common pitfall
If you allow “use general knowledge,” the model may blend evidence with guesses. A strict grounding policy is: “Use only the context; if insufficient, return an uncertainty response.”

## Related
RAG, Citation
