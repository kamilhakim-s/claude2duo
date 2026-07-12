# Build & deployment — transfer-service

## Build
Gradle Kotlin DSL, single module (`settings.gradle.kts`: rootProject `transfer-service`).

| Task | Command |
|---|---|
| Run tests | `./gradlew test` |
| Build boot jar | `./gradlew bootJar` |
| Run locally | `./gradlew bootRun` (H2 in-memory, no setup needed) |

## Deployment
UNKNOWN — verify with the team. This repository contains **no** Dockerfile, OpenShift
manifests, Helm charts, or CI pipeline definitions. Route patterns, probes, resource
limits and image build process cannot be derived from the code.

## What to touch when…
| Change | Files |
|---|---|
| New endpoint | `..controller`, `..dto`, `..service` (+ tests) — no deployment file exists to update |
| New config property | `src/main/resources/application.yml` only |
