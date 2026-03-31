## Hint 1
Use `driver.save_screenshot(filepath)` to capture the full page.

## Hint 2
We supply the `EVALFORGE_ARTIFACT_DIR` environment variable. You should concatenate it with a valid file name such as `screenshot.png` or `evidence.png`.

## Hint 3
An easy way to build the path is `os.path.join(artifact_dir, "my_screenshot.png")`.
