# TASK-TEMPLATE — transfer-service

> Stack: Spring Boot 3.3.5, Java 21, JPA, H2. Copy everything below the line into GitLab Duo / Copilot to start a task. Fill in the `{...}` placeholders. Attach the context files and the in-scope source files.

---

You are working on **transfer-service**, a Spring Boot 3.3.5 / Java 21 payments microservice (package `com.example.payments`). Follow these steps strictly and do not skip any.

**Attached context (read these FIRST, before writing any code):**
- `docs/ai-context/ARCHITECTURE.md` — codebase map, runtime flow, invariants
- `docs/ai-context/CONVENTIONS.md` — layering, naming, error handling, testing rules
- `docs/ai-context/API-SIGNATURES.md` — public signatures of every class
- Source files in scope: includeded in chat

**Task:** Add a description field (max 140 chars, optional) to transfers. It must be persisted and returned in the response.

**Acceptance criteria:**

**Constraints:**
- Obey the layering rule: controller → service → repository → model. Do not add business logic to controllers.
- Follow CONVENTIONS.md: constructor injection into `private final` fields; DTOs are `record`s; entities have no setters (change state via intent-named methods); money is `BigDecimal` compared with `compareTo`; business rules return String reason codes and persist REJECTED transfers; missing resources throw and are mapped in `GlobalExceptionHandler`.
- Do not modify existing behavior unless the task requires it.

**Procedure — do these one message at a time, waiting for my reply between each:**
1. **Restate understanding.** In your own words, describe the relevant flow (which classes/methods are involved and in what order) that this task touches. Do NOT write code yet.
2. **Propose a plan.** List the concrete steps, files to create/edit, and any new tests. Then STOP and wait for my approval.
3. **Implement one step at a time.** After I approve, make the change for a single step, show the diff, and wait for me to confirm before the next step.
4. **Add/adjust tests** following the existing pattern: JUnit 5 + AssertJ, `@SpringBootTest @Transactional`, real repositories (no mocks), sentence-style test method names.
5. **Finish** by listing which files in `docs/ai-context/` are now stale (e.g. new endpoint → ARCHITECTURE + API-SIGNATURES; new convention → CONVENTIONS) so a human can update them and log the session in `docs/ai-context/HANDOVER.md`.

Begin with Step 1 only.
