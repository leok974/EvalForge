# Hints — CLI Navigation

## Hint 1 (Concept)
If you store the workspace path once (`WS="$(pwd)"`), you can always write output files safely using `"$WS/outputs/..."`.

## Hint 2 (Guided)
After `cd fixtures/site/pages`, `pwd` is the value you want for `outputs/location.txt`.

## Hint 3 (Near-solution)
Use this order:
1) `WS="$(pwd)"`
2) `mkdir -p outputs`
3) `cd fixtures/site/pages`
4) `pwd > "$WS/outputs/location.txt"`
5) `ls > "$WS/outputs/pages.txt"`
6) `cd "$WS"`
7) `pwd > outputs/back.txt`
