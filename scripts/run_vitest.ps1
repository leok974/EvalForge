$TARGET = if ($args.Count -gt 0) { $args[0] } else { "debounce" }

Push-Location exercises\js
try {
    npm ci --silent 2>&1 | Out-Null
    npm run -s test
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}

exit $exitCode
