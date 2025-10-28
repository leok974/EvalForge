import { describe, it, expect, vi } from "vitest";
import { debounce } from "../src/debounce";

describe("debounce", () => {
  it("trailing call happens once after wait", () => {
    vi.useFakeTimers();
    const fn = vi.fn(); const d = debounce(fn, 50);
    d(); vi.advanceTimersByTime(49); expect(fn).toHaveBeenCalledTimes(0);
    vi.advanceTimersByTime(1); expect(fn).toHaveBeenCalledTimes(1);
  });

  it("leading true triggers immediately", () => {
    vi.useFakeTimers();
    const fn = vi.fn(); const d = debounce(fn, 50, { leading: true, trailing: false });
    d(); expect(fn).toHaveBeenCalledTimes(1);
    vi.advanceTimersByTime(60); expect(fn).toHaveBeenCalledTimes(1);
  });
});
