# HEAD

## Definition
**HEAD** is a pointer to your current checkout — the commit and branch your working tree is based on. It answers: “Where am I right now?”

## Tiny example
On `main`, HEAD points to `main`’s latest commit. If you checkout a specific commit, HEAD becomes “detached.”

## Common pitfall
Detached HEAD can confuse people: commits made in detached mode are not on a named branch unless you create one. If you see “detached HEAD,” create a branch to keep your work.

## Related
Branch, Switch/Checkout
