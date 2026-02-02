# Chunk

## Definition
A **chunk** is a small slice of a document used for retrieval and citation. Chunks are the unit you retrieve and feed into the model.

## Tiny example
A 150–300 word section of a help article, stored with an id like `help:reset:chunk-2`.

## Common pitfall
Chunks without stable ids make citations unreliable. Store chunk metadata:
- id
- source document
- text
- (optional) location offsets or headings

## Related
Retrieval, Citation
