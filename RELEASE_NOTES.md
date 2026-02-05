# Release Notes: React Foundations RC1

## 🚀 Feature: React Foundations World
10 new quests teaching React core concepts using **pure JavaScript** (`React.createElement`) and `react-test-renderer`.

### 🌍 World Content (`world-react`)
| Slug | Topic | Concepts |
|---|---|---|
| `react-ignition` | Hello World | `createElement`, `data-testid` |
| `react-components` | Composition | Nesting components |
| `react-props` | Data Flow | Props, Defaults |
| `react-conditional-render` | Logic | Ternaries, `null` returns |
| `react-lists` | Collections | `.map()`, `key` prop |
| `react-state-counter` | State Basics | `useState`, numbers |
| `react-state-toggle` | State Logic | Boolean state, functional updates |
| `react-effects-mount` | Lifecycle | `useEffect`, mount/unmount |
| `react-context-theme` | Deep Data | `createContext`, `useContext` |
| `react-reducer-cart` | Complex State | `useReducer`, dispatch |

## 🛠️ Infrastructure Updates
- **New Helper**: `data/quests/_shared/react_test_helpers.mjs` (simulates React testing without DOM).
- **Runner Update**: `scripts/run_world_public_tests.mjs` now supports `.mjs` quest files.
- **CI Integration**: Added `Verify React World` step to `.github/workflows/questpacks.yml`.
- **Documentation**: New `docs/world-react.md` guide and pure-JS tutorials for all quests.

## ✅ Verification
- **Regression Sweep**:
    - `cli_core`: 10/10 PASS
    - `infra_core`: 10/10 PASS
    - `react_core`: 10/10 PASS
- **Gates**:
    - Tutorials Validated: ✅
    - Codex Audit: ✅ (Zero missing references)
    - Legacy Audit: ✅ (Clean DB)

## ⚠️ Known Issues
- **API Availability**: The `/api/quests` endpoint is currently returning `500 Internal Server Error` for multiple worlds (`world-python`, `world-react`) in the test environment. This blocks the final API-level count verification script (`verify_db_integrity.py`), but does not affect quest functionality or local verification.
