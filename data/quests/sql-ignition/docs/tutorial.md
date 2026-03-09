# Tutorial: SQL Ignition

[SQL](glossary/sql/select) (Structured Query Language) is the language of databases. To get data out, you "query" it.

A [query](glossary/sql/select) is composed of clauses. The two most fundamental are:

1.  **[SELECT](glossary/sql/select)**: Specifies *what* columns you want.
2.  **[FROM](glossary/sql/from)**: Specifies *which* [table](glossary/sql/table) the data lives in.

## The Asterisk shorthand

If you want to see every column in a table, you don't have to list them all by name. You can use the `*` (asterisk) symbol, which means "all columns."

```sql
SELECT *
FROM products;
```

In this quest, you will use this same pattern to look at the `users` table.
