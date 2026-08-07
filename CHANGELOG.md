# Changelog

All notable changes to the Storm Financial Command Center (SFCC) project are documented here.

The format loosely follows Keep a Changelog and uses semantic, human-readable release notes.

---

## v0.3.5 - Project Standards

### Added
- ARCHITECTURE.md defining project design rules.
- ROADMAP.md outlining planned development milestones.
- Formal architectural principles for future development.

### Changed
- Established a single-source-of-truth philosophy for financial calculations.
- Defined responsibilities for Pages, Widgets, and the Database layer.

---

## v0.3.4 - Database Cleanup

### Changed
- Simplified database initialization.
- Separated database connections from migration execution.
- Removed unreachable code from transaction handling.

### Removed
- Duplicate transaction logic.
- Duplicate monthly calculation functions.

---

## v0.3.3 - Monthly Summary Refactor

### Changed
- Consolidated monthly income calculations into `get_monthly_summary()`.
- Updated Income page to consume shared monthly summary data.

### Removed
- `get_actual_income()`
- Duplicate monthly income calculation paths.

---

## v0.3.2 - Transactions V2

### Added
- Reusable `TransactionCard` widget.
- Transaction list built from reusable cards.
- Manual transaction date entry.

### Changed
- Refactored Transactions page into smaller helper methods.
- Improved vendor memory integration.

---

## v0.3.1 - Repository Cleanup

### Changed
- Removed generated cache files from version control.
- Added `.gitignore`.
- Removed local SQLite database from the repository.

---

## Future Releases

Each release should include:

### Added
New functionality.

### Changed
Behavior or architecture improvements.

### Fixed
Bug fixes.

### Removed
Deprecated or duplicate code removed.

### Security
Security-related improvements, if applicable.
