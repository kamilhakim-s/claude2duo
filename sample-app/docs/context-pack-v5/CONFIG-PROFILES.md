# Configuration & profiles — transfer-service

> Single `application.yml`; no profile-specific files exist.

## Profiles
None defined. There is no `application-<profile>.yml` and no `@Profile` usage.
Environment-specific configuration strategy: UNKNOWN — verify with the team.

## Properties (`src/main/resources/application.yml`)
| Property | Value | Effect |
|---|---|---|
| spring.application.name | transfer-service | Service name |
| spring.datasource.url | jdbc:h2:mem:transfers | In-memory H2; data lost on restart |
| spring.jpa.hibernate.ddl-auto | create-drop | Hibernate creates/drops schema; no migrations |

## Feature flags
None.

## Secrets
No credentials exist in this repo (H2 in-memory needs none). Secret-injection mechanism
for real environments: UNKNOWN — verify with the team.

## Adding configuration
Add the property to `application.yml` and inject via `@Value` or a
`@ConfigurationProperties` record — note there is **no existing example of either** in
this codebase, so establish the pattern deliberately when first needed.
