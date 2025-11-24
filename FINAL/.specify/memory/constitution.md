<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.0.1
Change Type: PATCH - Clarification of documentation requirements
Modified Principles:
  - I. Code Quality First - Added explicit user documentation requirement

Added Requirements:
  - User documentation MUST be created and kept up-to-date with every feature release
  - Code review checklist now includes user documentation verification

Templates Status:
  ✅ plan-template.md - No changes needed (already supports documentation planning)
  ✅ spec-template.md - No changes needed (already captures user scenarios)
  ✅ tasks-template.md - No changes needed (can include documentation tasks)
  ⚠️ Future consideration: Add documentation template for user-facing guides

Agent Files Status:
  ✅ All agents - No changes needed (documentation tasks can be included in task breakdowns)

Follow-up Actions:
  - Reviewers should verify user documentation is updated during PR reviews
  - Consider adding documentation task template in future
  - README, usage guides, and troubleshooting docs must accompany features

Rationale: PATCH version (1.0.1) - Clarification that user documentation is a mandatory quality standard, not optional. This prevents undocumented features and reduces support burden.
-->

# SpecKit Constitution

## Core Principles

### I. Code Quality First

**Description**: Every line of code MUST meet rigorous quality standards before merging to main.

**Non-Negotiable Rules**:
- All code MUST pass automated linting and formatting checks with zero warnings
- Code complexity MUST be justified; cyclomatic complexity >10 requires documented rationale
- All public APIs MUST have comprehensive documentation (purpose, parameters, returns, examples)
- Code duplication >5 lines MUST be refactored into reusable components
- All functions MUST have single, clear responsibilities (Single Responsibility Principle)
- Type safety MUST be enforced where language supports it (strict typing required)
- User documentation MUST be created and kept up-to-date with every feature release (installation guides, usage examples, troubleshooting)

**Rationale**: Code quality debt compounds exponentially. Enforcing quality at write-time prevents technical debt accumulation and reduces long-term maintenance costs. Clear, well-documented code enables team scalability and reduces onboarding friction. User documentation ensures features are discoverable and usable, preventing support burden and user frustration.

### II. Testing Standards (NON-NEGOTIABLE)

**Description**: Test-Driven Development is mandatory; tests are the contract, implementation follows.

**Non-Negotiable Rules**:
- **Test-First Workflow**: Tests MUST be written and approved BEFORE implementation begins
- **Red-Green-Refactor Cycle**: Tests MUST fail initially, then pass after implementation
- **Test Coverage Minimum**: 80% line coverage required; critical paths require 100%
- **Test Categories Required**:
  - **Unit Tests**: All business logic, utilities, models (isolated, fast, deterministic)
  - **Integration Tests**: API contracts, database interactions, service boundaries
  - **Contract Tests**: All public API endpoints and inter-service communication
  - **Edge Case Tests**: Boundary conditions, error scenarios, invalid inputs
- **Test Independence**: Each test MUST run independently with no shared state
- **Test Documentation**: Each test MUST clearly document Given/When/Then scenarios

**Rationale**: Tests define expected behavior and serve as living documentation. Test-first prevents scope creep, ensures testability by design, and catches regressions before they reach production. This is NON-NEGOTIABLE because quality cannot be retrofitted.

### III. User Experience Consistency

**Description**: User-facing interfaces MUST deliver consistent, predictable, and delightful experiences.

**Non-Negotiable Rules**:
- **Response Time Standards**: User-initiated actions MUST acknowledge within 100ms; complete within 1s for 95th percentile
- **Error Messages MUST be**:
  - Human-readable and actionable (no technical jargon unless developer-facing)
  - Consistent in tone, format, and structure across the application
  - Logged with sufficient context for debugging (correlation IDs, timestamps, stack traces)
- **Accessibility Requirements**:
  - WCAG 2.1 Level AA compliance for all user interfaces
  - Keyboard navigation MUST be fully functional
  - Screen reader compatibility MUST be tested
- **Design System Adherence**: All UI components MUST use approved design tokens (colors, spacing, typography)
- **Loading States**: All async operations MUST show progress indicators
- **Offline Resilience**: Graceful degradation required when services unavailable

**Rationale**: Inconsistent UX erodes user trust and increases support burden. Establishing strict UX standards ensures professional polish, reduces cognitive load, and creates predictable user journeys that scale across features.

### IV. Performance Requirements

**Description**: Performance is a feature; systems MUST meet defined performance budgets.

**Non-Negotiable Rules**:
- **Performance Budgets MUST be defined** for every feature during planning phase:
  - Response time targets (p50, p95, p99 latency)
  - Memory consumption limits
  - CPU utilization thresholds
  - Network payload sizes
- **Performance Testing Required**:
  - Load tests for all API endpoints (expected traffic + 50% headroom)
  - Stress tests to identify breaking points
  - Profiling of hot paths and optimization of bottlenecks
- **Regression Prevention**:
  - Performance benchmarks MUST run in CI/CD pipeline
  - Performance degradation >10% blocks deployment
- **Monitoring & Alerts**:
  - Real-time performance metrics MUST be collected (latency, throughput, errors)
  - Alerts MUST trigger before user impact (proactive, not reactive)
- **Database Performance**:
  - All queries MUST have execution plans reviewed
  - N+1 queries are PROHIBITED
  - Indexes MUST exist for all WHERE/JOIN clauses on production data

**Rationale**: Performance problems are expensive to fix post-launch and directly impact user satisfaction. Defining budgets upfront forces architectural decisions that scale, prevents costly rewrites, and ensures competitive user experiences.

## Development Standards

### Code Review Process

**Requirements**:
- All code changes MUST be reviewed by at least one team member before merging
- Reviewers MUST verify constitution compliance (quality, tests, UX, performance)
- Review checklists MUST include:
  - ✅ Tests exist and pass (Red-Green-Refactor verified)
  - ✅ Code quality standards met (linting, complexity, documentation)
  - ✅ Performance budgets validated (benchmarks pass)
  - ✅ UX consistency verified (design system adherence, error handling)
  - ✅ Edge cases covered
  - ✅ User documentation updated (README, guides, examples)
- Self-merging is PROHIBITED unless emergency hotfix (requires post-facto review)

### Branching & Version Control

**Requirements**:
- Feature branches MUST follow convention: `###-feature-name`
- Commits MUST be atomic and follow conventional commit format
- Main branch MUST always be deployable (all tests pass, no known critical bugs)
- Breaking changes MUST be documented in migration guides

## Technical Decisions

### Architecture Principles

**Decision Framework**: All architectural decisions MUST be:
1. **Documented**: Use Architecture Decision Records (ADRs) for significant choices
2. **Justified**: Include context, options considered, trade-offs, and rationale
3. **Aligned**: Must support constitution principles (quality, testability, UX, performance)
4. **Reversible**: Prefer decisions that can be changed with minimal cost

### Technology Selection

**Criteria**: New dependencies/technologies MUST meet:
- **Maturity**: Stable release with active maintenance (not experimental)
- **Community**: Strong community support and documentation
- **Security**: No known critical vulnerabilities; regular security updates
- **Performance**: Meets or exceeds performance budgets
- **Licensing**: Compatible with project licensing requirements
- **Testing**: Must be mockable/testable for unit test isolation

### Complexity Justification

**When required**: Complexity that violates simplicity principles MUST document:
- **Problem**: What problem requires this complexity?
- **Alternatives**: What simpler approaches were considered and why rejected?
- **Trade-offs**: What are we gaining vs. the complexity cost?
- **Mitigation**: How will we manage/contain this complexity?
- **Review Trigger**: When will we revisit this decision?

## Governance

### Constitutional Authority

- This constitution SUPERSEDES all other development practices and guidelines
- When conflicts arise, constitution principles take precedence
- All team members MUST understand and agree to uphold these principles
- Violations require explicit justification and approval via Complexity Justification process

### Amendment Process

**To amend this constitution**:
1. **Proposal**: Document proposed change with rationale and impact analysis
2. **Review**: Team review of proposal (minimum 3 business days for feedback)
3. **Approval**: Unanimous consent required for MAJOR changes; majority for MINOR/PATCH
4. **Migration**: Create migration plan if changes affect existing code
5. **Communication**: Announce changes to all stakeholders
6. **Versioning**: Update version number per semantic versioning rules

**Version Semantics**:
- **MAJOR**: Backward-incompatible principle removals or fundamental redefinitions
- **MINOR**: New principles added or material expansions to governance
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Compliance & Enforcement

**Quality Gates**:
- All PRs/commits MUST pass automated constitution compliance checks:
  - Linting and formatting validation
  - Test coverage threshold enforcement
  - Performance benchmark validation
  - Accessibility compliance checks
- Manual review MUST verify:
  - Test-first workflow followed (tests written before implementation)
  - UX consistency maintained
  - Complexity justified when necessary

**Continuous Improvement**:
- Constitution effectiveness MUST be reviewed quarterly
- Metrics tracked: code quality trends, test coverage, performance regressions, UX consistency scores
- Retrospectives MUST identify constitution gaps or enforcement challenges

**Accountability**:
- Repeated violations trigger process improvement discussions
- Systematic compliance failures indicate constitution needs amendment
- Team leads responsible for ensuring team understanding and adherence

### Template & Tool Integration

**Specification Workflow**:
- `.specify/templates/spec-template.md` MUST enforce testable user stories aligned with Principle III
- `.specify/templates/plan-template.md` MUST include Constitution Check gates validating all 4 principles
- `.specify/templates/tasks-template.md` MUST structure tasks to support test-first workflow

**Agent Guidance**:
- All agents (plan, implement, tasks) MUST reference and enforce constitution principles
- Agents MUST block progress when constitution violations detected without justification
- Agent outputs MUST be validated against quality, testing, UX, and performance standards

**Version**: 1.0.1 | **Ratified**: 2025-11-23 | **Last Amended**: 2025-11-23
