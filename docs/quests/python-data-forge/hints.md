# Hints — Data Forge

## Hint 1 (Files)
Use `json.load(open('fixtures/raw_contacts.json'))` to read the data.

## Hint 2 (Normalization)
- **Strings**: `'  foo  '.strip().title()` becomes `'Foo'`.
- **Lists**: `sorted(set(tags))` forces unique order.
- **Booleans**: Create a set of truthy strings: `{'yes', 'true', '1'}`.

## Hint 3 (Validation)
Printing `json.dumps(result)` is enough. The validator parses your output and compares it structurally to the expected data.
