<!--
SYNC IMPACT REPORT
==================
Version: 1.1.0 (Added User Documentation Principle)
Previous Version: 1.0.0
Constitution Created: 2025-11-19
Last Amended: 2025-11-19

Principles Defined:
  - Code Quality First (P1)
  - Comprehensive Testing Standards (P2)
  - User Experience Consistency (P3)
  - Performance Requirements (P4)
  - User Documentation (P5) ⭐ NEW
  - Use Emojis in Output (P6)

Modified Sections:
  - Core Principles (6 principles - added User Documentation)
  - Quality Gates (updated gate #6 to include user documentation)

Version Bump Rationale:
  - MINOR bump (1.0.0 → 1.1.0): New principle added (User Documentation)
  - Materially expands governance without breaking existing practices

Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section aligns with all principles
  ✅ spec-template.md - User scenarios support documentation requirements
  ✅ tasks-template.md - Task categorization can include documentation tasks

Follow-up TODOs:
  - None - all placeholders filled

Suggested Commit Message:
  docs: amend constitution to v1.1.0 (add user documentation principle)
-->

# SpecKit Constitution

## Core Principles

### I. Code Quality First

Code MUST be maintainable, readable, and follow established best practices:

- **Single Responsibility**: Every module, class, and function MUST have one clear purpose
- **Clear Naming**: Names MUST be self-documenting; avoid abbreviations unless industry-standard
- **DRY Principle**: Code duplication MUST be eliminated through proper abstraction
- **Code Reviews**: All code MUST be reviewed by at least one other developer before merge
- **Static Analysis**: Code MUST pass linting, formatting, and type-checking without warnings
- **Documentation**: Public APIs MUST have comprehensive docstrings/comments explaining purpose,
  parameters, return values, and examples

**Rationale**: Quality code reduces technical debt, accelerates feature development, and minimizes
bugs. Code is read 10x more than it is written; optimizing for readability pays dividends across
the entire development lifecycle.

### II. Comprehensive Testing Standards (NON-NEGOTIABLE)

Testing MUST be rigorous, automated, and performed before implementation:

- **Test-First Development**: Tests MUST be written and approved before implementation begins
- **Red-Green-Refactor**: Tests MUST fail first (red), implementation makes them pass (green),
  then code is refactored for quality
- **Test Coverage Minimum**: Code coverage MUST be ≥80% for unit tests; critical paths require
  100% coverage
- **Test Types Required**:
  - **Unit Tests**: All functions, methods, and classes MUST have isolated unit tests
  - **Integration Tests**: APIs, database interactions, and service boundaries MUST have
    integration tests
  - **Contract Tests**: Public interfaces MUST have contract tests verifying behavior contracts
  - **End-to-End Tests**: Critical user journeys MUST have automated E2E tests
- **Test Quality**: Tests MUST be deterministic, fast (<5s for unit, <30s for integration),
  and independent
- **Continuous Testing**: All tests MUST run on every commit via CI/CD pipeline

**Rationale**: Testing first ensures features are designed for testability and meet requirements.
Comprehensive testing catches regressions early, enables confident refactoring, and serves as
living documentation of system behavior.

### III. User Experience Consistency

User interfaces and interactions MUST be consistent, intuitive, and accessible:

- **Design System Compliance**: All UI components MUST follow the established design system
  (colors, typography, spacing, components)
- **Interaction Patterns**: Similar actions MUST behave identically across the application
  (e.g., all modals close with ESC, all forms validate on blur)
- **Accessibility Standards**: MUST comply with WCAG 2.1 Level AA:
  - Keyboard navigation for all interactive elements
  - Screen reader compatibility with ARIA labels
  - Color contrast ratios ≥4.5:1 for text
  - Focus indicators visible and clear
- **Error Handling UX**: Error messages MUST be user-friendly, actionable, and consistent in tone
- **Loading States**: All async operations MUST show loading indicators within 200ms
- **Responsive Design**: UI MUST be fully functional on mobile, tablet, and desktop viewports
- **User Feedback**: All user actions MUST provide immediate feedback (visual/haptic/audio)

**Rationale**: Consistency reduces cognitive load, improves learnability, and builds user trust.
Accessible design ensures the product serves all users and meets legal compliance requirements.

### IV. Performance Requirements

Applications MUST meet strict performance benchmarks to ensure excellent user experience:

- **Page Load Performance**:
  - Initial page load MUST complete in <2 seconds on 3G networks
  - Time to Interactive (TTI) MUST be <3 seconds
  - First Contentful Paint (FCP) MUST be <1 second
- **Runtime Performance**:
  - UI interactions MUST respond within 100ms (perceived as instant)
  - Animations MUST maintain 60fps (16.67ms frame budget)
  - Memory usage MUST not grow unbounded (no memory leaks)
- **API Performance**:
  - API response times MUST be <200ms at p95 for critical endpoints
  - API response times MUST be <500ms at p99 for all endpoints
  - Database queries MUST be optimized with indexes and <100ms execution time
- **Scalability**:
  - System MUST handle 10x current load without degradation
  - Horizontal scaling MUST be possible without code changes
- **Monitoring**: Performance metrics MUST be tracked in production with alerts for degradation

**Rationale**: Performance directly impacts user satisfaction, conversion rates, and SEO rankings.
Poor performance drives users away; investing in performance upfront prevents costly optimization
later.

### V. User Documentation

User-facing documentation MUST be comprehensive, accurate, and maintained alongside code:

- **Documentation Required**: All user-facing features MUST have corresponding documentation
- **Up-to-Date Requirement**: Documentation MUST be updated in the same PR as code changes
- **Merge Blocker**: Code CANNOT be merged to master branch if documentation is missing or outdated
- **Documentation Types**:
  - **User Guides**: Step-by-step instructions for common tasks and workflows
  - **API Documentation**: Complete reference for all public APIs with examples
  - **Release Notes**: Clear description of changes, new features, and breaking changes
  - **Troubleshooting**: Common issues and their solutions
- **Quality Standards**:
  - Clear, concise language appropriate for target audience
  - Screenshots/diagrams for complex UI flows
  - Code examples that are tested and runnable
  - Searchable and well-organized structure
- **Review Process**: Documentation changes MUST be reviewed alongside code for accuracy and clarity

**Rationale**: Documentation is the primary interface between users and the product. Outdated or
missing documentation leads to user frustration, support burden, and reduced adoption. Maintaining
documentation in sync with code ensures users always have accurate information.

### VI. Use Emojis in Output

Add emojis to every output!!

## Quality Gates

All code changes MUST pass these gates before merging:

1. **Constitution Compliance**: Code review MUST verify adherence to all core principles
2. **Test Gate**: All tests (unit, integration, E2E) MUST pass; coverage MUST meet minimums
3. **Performance Gate**: Performance benchmarks MUST not regress by >5%
4. **Accessibility Gate**: Automated accessibility tests MUST pass; manual audit for new UI
5. **Security Gate**: Security scanning MUST pass with zero high/critical vulnerabilities
6. **Documentation Gate**: Public APIs and user documentation MUST be updated; user docs MUST be
   current before merge to master

**Enforcement**: CI/CD pipeline MUST automatically check gates; any failure blocks merge.

## Implementation Standards

### Code Structure

- **Modular Architecture**: Code MUST be organized into clear modules with defined boundaries
- **Dependency Management**: Dependencies MUST be explicit, minimal, and kept up-to-date
- **Configuration**: Environment-specific config MUST be externalized (not hardcoded)

### Development Workflow

1. **Specification First**: Features start with spec.md defining user stories and acceptance
   criteria
2. **Planning**: Technical plan created (plan.md) with architecture, structure, constitution check
3. **Test Writing**: Tests written in tasks.md and implemented before feature code
4. **Implementation**: Feature code implemented following TDD cycle
5. **Review & Merge**: Code reviewed for quality, tests, performance, accessibility; then merged

### Technical Decisions

- **Complexity Justification**: Any deviation from simplicity MUST be documented with rationale
- **Technology Choices**: New technologies/libraries MUST be justified against project needs
- **Breaking Changes**: API breaking changes require MAJOR version bump and migration guide

## Governance

### Authority

This constitution supersedes all other development practices, guidelines, and preferences. When
conflicts arise, constitution principles take precedence.

### Amendments

Constitution amendments require:

1. **Proposal**: Document proposed change with rationale and impact analysis
2. **Review**: Team review and approval by majority vote
3. **Migration Plan**: If amendment changes existing requirements, provide migration plan
4. **Version Bump**: Update constitution version following semantic versioning:
   - **MAJOR**: Backward-incompatible principle removals or redefinitions
   - **MINOR**: New principles or materially expanded guidance
   - **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Compliance

- **Code Reviews**: Reviewers MUST verify constitution compliance before approval
- **Continuous Monitoring**: Teams MUST audit projects quarterly for compliance
- **Exception Process**: Rare exceptions require documented justification and team approval

### Runtime Development Guidance

For day-to-day development guidance, workflows, and agent instructions, refer to:

- **Agent Files**: `.github/agents/speckit.*.agent.md` for agent-specific execution workflows
- **Templates**: `.specify/templates/*.md` for specification, planning, and task templates
- **Prompts**: `.github/prompts/speckit.*.prompt.md` for command-specific instructions

**Version**: 1.1.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19
