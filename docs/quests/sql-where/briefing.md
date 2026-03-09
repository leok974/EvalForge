# Briefing — Active Detroit Directory

The Archives are preparing a contact sheet for an outreach mission in **Detroit**.

You’ve been asked to produce a clean directory that includes **only active users** located in Detroit. The output must be neat and consistent so other systems can rely on it.

## Your output
Return **exactly** these columns, in this order:

1) `name`
2) `city`

## Filtering rules
- Include only users where `city = 'Detroit'`
- Include only users where `is_active = 1`

## Ordering rule
- Sort by `name` ascending (`ORDER BY name ASC`)
