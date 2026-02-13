export function checkNumber(n) {
    if (n > 0) return "positive";
    if (n < 0) return "negative";
    return "zero";
}

export function sumTo(n) {
    let sum = 0;
    for (let i = 1; i <= n; i++) sum += i;
    return sum;
}