function apply(val, fns) {
  return fns.reduce((acc, fn) => fn(acc), val);
}
console.log(apply(5, [v => v*2, v => v+1]));