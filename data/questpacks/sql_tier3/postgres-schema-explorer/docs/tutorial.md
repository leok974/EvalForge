### Database Exploration Guide

Welcome to the PostgreSQL Workbench! In this mission, you'll be using the **Database Explorer** to understand the structure of the `archives` database.

#### How to use the Database Explorer
1. Click the **Database** tab in the left-hand pane (Quest Drawer).
2. You will see a list of schemas (e.g., `public`, `inventory`, `analytics`).
3. Click a table (e.g., `users`, `events`) to see its column definitions and types.
4. Use the **Preview** button to see a sample of the actual data in that table.

#### Why this matters
Real-world database work often starts with a "blank screen" and an unfamiliar schema. Learning to navigate schemas without a map is a core skill for any senior engineer.

#### pgvector Support
This environment has `pgvector` enabled! You can inspect vector columns just like any other data type. Look for columns with the type `vector(N)`.
