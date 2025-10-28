export function debounce<T extends (...a: any[]) => any>(
  fn: T, wait: number, opt: { leading?: boolean; trailing?: boolean } = {}
) {
  const { leading = false, trailing = true } = opt;
  let t: any = null, lastArgs: any[] | null = null, lastThis: any = null, invoked = false;

  const invoke = () => {
    const args = lastArgs; const ctx = lastThis; lastArgs = lastThis = null;
    if (args) fn.apply(ctx, args);
  };

  const wrapper = function(this: any, ...args: any[]) {
    lastArgs = args; lastThis = this;
    if (t) clearTimeout(t);
    const callNow = leading && !invoked;
    t = setTimeout(() => { t = null; invoked = false; if (trailing) invoke(); }, wait);
    if (callNow) { invoked = true; invoke(); }
  } as T & { cancel(): void; flush(): void };

  wrapper.cancel = () => { if (t) clearTimeout(t); t = null; lastArgs = lastThis = null; invoked = false; };
  wrapper.flush = () => { if (t) { clearTimeout(t); t = null; if (trailing) invoke(); invoked = false; } };
  return wrapper;
}
