import { defineConfig } from "vitest/config";
export default defineConfig({
  test: { 
    reporters: ["default"],
    coverage: { 
      provider: "v8", 
      reportsDirectory: "coverage" 
    } // will write coverage/coverage-final.json
  }
});
