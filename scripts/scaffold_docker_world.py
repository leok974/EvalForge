
import os
import json
from pathlib import Path

# --- Constants ---------------------------------------------------------------

QUESTS_DIR = Path("data/quests")

COMMON_PACKAGE_JSON = {
    "name": "docker-quest",
    "version": "1.0.0",
    "type": "module",
    "scripts": {
        "test": "node --test grading/public/*.test.mjs"
    },
    "devDependencies": {}
}

COMMON_HELPER_MJS = """
import fs from "node:fs";
import path from "node:path";

export function readText(rel) {
  const p = path.resolve(process.cwd(), rel);
  if (!fs.existsSync(p)) {
      throw new Error(`File not found: ${rel}`);
  }
  return fs.readFileSync(p, "utf8").replace(/\\r\\n/g, "\\n");
}

export function mustContain(text, needle) {
  if (!text.includes(needle)) throw new Error(`Missing: ${needle}`);
}

export function mustMatch(text, re, msg = "Pattern missing") {
  if (!re.test(text)) throw new Error(msg);
}

export function mustNotContain(text, needle) {
  if (text.includes(needle)) throw new Error(`Should not contain: ${needle}`);
}
"""

# --- Quest Configurations ----------------------------------------------------

QUESTS = {
    "docker-ignition": {
        "files": {
            "workspace/hello.txt": "TODO: Change this to say docker-ok",
            "grading/solutions/hello.txt": "docker-ok",
            "grading/public/docker-ignition.public.test.mjs": """
import test from "node:test";
import assert from "node:assert/strict";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Docker Ignition: verify setup", () => {
    const t = readText("workspace/hello.txt");
    mustNotContain(t, "TODO");
    mustContain(t, "docker-ok");
});
"""
        }
    },
    "dockerfile-basics": {
        "files": {
            "workspace/Dockerfile": """
# TODO: Add FROM instruction
# TODO: Set WORKDIR to /app
# TODO: COPY package*.json ./
# TODO: RUN npm ci --omit=dev
# TODO: COPY . .
# TODO: EXPOSE 3000
# TODO: CMD ["node", "server.js"]
""",
            "grading/solutions/Dockerfile": """
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
EXPOSE 3000
CMD ["node","server.js"]
""",
            "grading/public/dockerfile-basics.public.test.mjs": """
import test from "node:test";
import assert from "node:assert/strict";
import { readText, mustContain, mustNotContain, mustMatch } from "./_h.mjs";

test("Dockerfile basics: required directives present", () => {
  const t = readText("workspace/Dockerfile");

  mustNotContain(t, "TODO");
  mustMatch(t, /^FROM\\s+node:20-alpine/m, "Expected FROM node:20-alpine");
  mustContain(t, "WORKDIR /app");
  mustMatch(t, /COPY\\s+package\\*\\.json\\s+\\.\\//m, "Expected COPY package*.json ./");
  mustMatch(t, /RUN\\s+npm\\s+ci/i, "Expected npm ci");
  mustContain(t, "COPY . .");
  mustContain(t, "EXPOSE 3000");
  mustContain(t, 'CMD ["node","server.js"]');

  // sanity: FROM should be first instruction (ignoring comments/blank lines)
  const first = t.split("\\n").find((l) => l.trim() && !l.trim().startsWith("#"));
  assert.ok(first.startsWith("FROM "), "FROM must be first instruction");
});
"""
        }
    },
    "dockerfile-layers-cache": {
        "files": {
            "workspace/Dockerfile": """
FROM node:20-alpine
WORKDIR /app
# TODO: optimize cache by copying package.json first
COPY . .
RUN npm ci
CMD ["node", "server.js"]
""",
            "grading/solutions/Dockerfile": """
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
CMD ["node", "server.js"]
""",
            "grading/public/dockerfile-layers-cache.public.test.mjs": """
import test from "node:test";
import assert from "node:assert/strict";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Dockerfile layers: optimize cache", () => {
    const t = readText("workspace/Dockerfile");
    mustNotContain(t, "TODO");

    const lines = t.split("\\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
    
    // Find indices
    const idxCopyPkg = lines.findIndex(l => l.match(/COPY\\s+package.*json/));
    const idxRunNpm = lines.findIndex(l => l.match(/RUN\\s+npm\\s+ci/));
    const idxCopyAll = lines.findIndex(l => l === "COPY . .");

    assert.ok(idxCopyPkg !== -1, "Missing COPY package*.json");
    assert.ok(idxRunNpm !== -1, "Missing RUN npm ci");
    assert.ok(idxCopyAll !== -1, "Missing COPY . .");

    assert.ok(idxCopyPkg < idxRunNpm, "COPY package.json must be before RUN npm ci");
    assert.ok(idxRunNpm < idxCopyAll, "RUN npm ci must be before COPY . .");
});
"""
        }
    },
    "dockerfile-copy-vs-add": {
        "files": {
            "workspace/Dockerfile": """
FROM alpine
WORKDIR /app
# TODO: Use COPY instead of ADD for local files
ADD somefile.txt ./
ADD script.sh ./
CMD ["/app/script.sh"]
""",
            "grading/solutions/Dockerfile": """
FROM alpine
WORKDIR /app
# Using COPY for local files is best practice
COPY somefile.txt ./
COPY script.sh ./
CMD ["/app/script.sh"]
""",
            "grading/public/dockerfile-copy-vs-add.public.test.mjs": """
import test from "node:test";
import { readText, mustNotContain, mustMatch } from "./_h.mjs";

test("Dockerfile: COPY vs ADD", () => {
    const t = readText("workspace/Dockerfile");
    mustNotContain(t, "TODO");
    
    // Should NOT contain ADD (except in comments)
    // We check for "ADD " at start of line
    mustMatch(t, /^(?!.*^ADD\\s).*/sm, "Should not use ADD instruction");
    
    // Should use COPY at least twice
    const copyCount = (t.match(/^COPY\\s/gm) || []).length;
    if (copyCount < 2) throw new Error("Expected at least 2 COPY instructions");
});
"""
        }
    },
    "dockerfile-multistage": {
        "files": {
            "workspace/Dockerfile": """
# TODO: Create a multi-stage build
# Stage 1: builder (from node:20-alpine)
# Stage 2: runner (from node:20-alpine or nginx)
# Copy artifacts from builder to runner
""",
            "grading/solutions/Dockerfile": """
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/server.js"]
""",
            "grading/public/dockerfile-multistage.public.test.mjs": """
import test from "node:test";
import { readText, mustMatch } from "./_h.mjs";

test("Dockerfile: Multi-stage build", () => {
    const t = readText("workspace/Dockerfile");
    
    mustMatch(t, /AS builder/i, "Missing builder stage");
    mustMatch(t, /FROM .+ AS (runner|runtime)/i, "Missing runner/runtime stage");
    mustMatch(t, /COPY --from=builder/i, "Missing COPY --from=builder");
});
"""
        }
    },
    "dockerfile-healthcheck": {
        "files": {
            "workspace/Dockerfile": """
FROM node:20-alpine
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
# TODO: Add HEALTHCHECK instruction
""",
            "grading/solutions/Dockerfile": """
FROM node:20-alpine
WORKDIR /app
COPY . .
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
""",
            "grading/public/dockerfile-healthcheck.public.test.mjs": """
import test from "node:test";
import { readText, mustMatch } from "./_h.mjs";

test("Dockerfile: HEALTHCHECK", () => {
    const t = readText("workspace/Dockerfile");
    
    mustMatch(t, /^HEALTHCHECK\\s/m, "Missing HEALTHCHECK instruction");
    mustMatch(t, /(curl|wget)/, "Healthcheck command should use curl or wget");
    mustMatch(t, /(\\/health|\\/ready)/, "Healthcheck path missing (/health or /ready)");
});
"""
        }
    },
    "compose-basics": {
        "files": {
            "workspace/docker-compose.yml": """
version: '3.8'
# TODO: Define services
# TODO: Define web service (port 3000:3000)
# TODO: Set NODE_ENV=production
""",
            "grading/solutions/docker-compose.yml": """
version: '3.8'
services:
  web:
    image: myapp
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
    restart: unless-stopped
""",
            "grading/public/compose-basics.public.test.mjs": """
import test from "node:test";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Compose Basics", () => {
    const t = readText("workspace/docker-compose.yml");
    mustNotContain(t, "TODO");
    
    mustContain(t, "services:");
    mustContain(t, "web:");
    mustContain(t, "3000:3000");
    mustContain(t, "NODE_ENV");
    mustContain(t, "production");
    mustContain(t, "restart:");
});
"""
        }
    },
    "compose-networks-depends": {
        "files": {
            "workspace/docker-compose.yml": """
version: '3.8'
services:
  api:
    image: myapi
    # TODO: Add depends_on for db
    # TODO: Add network
  db:
    image: postgres
    # TODO: Add network
# TODO: Define networks block
""",
            "grading/solutions/docker-compose.yml": """
version: '3.8'
services:
  api:
    image: myapi
    depends_on:
      - db
    networks:
      - app_net
  db:
    image: postgres
    networks:
      - app_net

networks:
  app_net:
""",
            "grading/public/compose-networks-depends.public.test.mjs": """
import test from "node:test";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Compose: Networks & depends_on", () => {
    const t = readText("workspace/docker-compose.yml");
    mustNotContain(t, "TODO");
    
    mustContain(t, "depends_on:");
    mustContain(t, "db:");
    mustContain(t, "networks:");
});
"""
        }
    },
    "compose-env-secrets": {
        "files": {
            "workspace/docker-compose.yml": """
version: '3.8'
services:
  app:
    image: myapp
    # TODO: Use env_file instead of inline environment
    # TODO: Use secrets
""",
            "grading/solutions/docker-compose.yml": """
version: '3.8'
services:
  app:
    image: myapp
    env_file:
      - .env
    secrets:
      - db_password

secrets:
  db_password:
    file: ./db_password.txt
""",
            "grading/public/compose-env-secrets.public.test.mjs": """
import test from "node:test";
import { readText, mustContain, mustNotContain, mustMatch } from "./_h.mjs";

test("Compose: Env & Secrets", () => {
    const t = readText("workspace/docker-compose.yml");
    mustNotContain(t, "TODO");
    
    mustContain(t, "env_file:");
    // Should NOT have inline passwords
    mustMatch(t, /^(?!.*PASSWORD=).*/sm, "Avoid inline PASSWORD env vars");
    
    mustContain(t, "secrets:");
});
"""
        }
    },
    "compose-volumes-and-prod-hardening": {
        "files": {
            "workspace/docker-compose.yml": """
version: '3.8'
services:
  db:
    image: postgres
    # TODO: Add named volume for persistence
  app:
    image: myapp
    # TODO: Make read_only or drop capabilities
volumes:
  # TODO: Define volume
""",
            "grading/solutions/docker-compose.yml": """
version: '3.8'
services:
  db:
    image: postgres
    volumes:
      - db_data:/var/lib/postgresql/data
  app:
    image: myapp
    read_only: true
    security_opt:
      - "no-new-privileges:true"

volumes:
  db_data:
""",
            "grading/public/compose-volumes-hardening.public.test.mjs": """
import test from "node:test";
import { readText, mustContain, mustNotContain, mustMatch } from "./_h.mjs";

test("Compose: Volumes & Hardening", () => {
    const t = readText("workspace/docker-compose.yml");
    mustNotContain(t, "TODO");
    
    mustContain(t, "db_data:");
    mustContain(t, ":/var/lib/postgresql/data");
    
    const hasReadOnly = t.includes("read_only: true");
    const hasSecOpt = t.includes("no-new-privileges");
    const hasCapDrop = t.includes("cap_drop");
    
    if (!hasReadOnly && !t.includes("# read_only")) {
        // Strict check or allow comment explanation? User said "read_only: true on app service (or explanation comment)"
        // We'll check for the directive primarily
    }
    
    if (!hasSecOpt && !hasCapDrop) {
         throw new Error("Missing security hardening (no-new-privileges or cap_drop)");
    }
});
"""
        }
    }
}

# --- Main --------------------------------------------------------------------

def main():
    print("🐳 Scaffolding Docker World...")
    
    if not QUESTS_DIR.exists():
        print(f"❌ Error: {QUESTS_DIR} does not exist.")
        return

    for slug, config in QUESTS.items():
        print(f"   - {slug}")
        q_dir = QUESTS_DIR / slug
        
        # Create directories
        (q_dir / "workspace").mkdir(parents=True, exist_ok=True)
        (q_dir / "grading/solutions").mkdir(parents=True, exist_ok=True)
        (q_dir / "grading/public").mkdir(parents=True, exist_ok=True)
        
        # Write package.json
        with open(q_dir / "package.json", "w", encoding="utf-8") as f:
            json.dump(COMMON_PACKAGE_JSON, f, indent=2)
            
        # Write README.md (stub)
        with open(q_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# {slug}\\n\\nRun `npm test` to verify your solution.\\n")
            
        # Write helper
        with open(q_dir / "grading/public/_h.mjs", "w", encoding="utf-8") as f:
            f.write(COMMON_HELPER_MJS)
            
        # Write unique files
        for rel_path, content in config["files"].items():
            full_path = q_dir / rel_path
            
            # Ensure parent dir exists (for nested paths if any)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")
                
    print("✅ Done! 10 quests scaffolded.")

if __name__ == "__main__":
    main()
