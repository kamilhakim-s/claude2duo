# transfer-service (sample app for AI context-file testing)

Minimal Spring Boot 3.3 / Java 21 app with one functionality: immediate payments
between internal accounts (`POST /api/v1/transfers`) with idempotency and
business-rule rejection (self-transfer, currency mismatch, insufficient funds).

Purpose: run the prompts in `../prompts/` against this repo in Claude Code,
then test whether the generated `docs/ai-context/` files make GitLab Duo /
Copilot effective in a fresh session. See `../prompts/test-protocol.md`.

Build: `./gradlew test` (or import into IntelliJ; uses in-memory H2).
