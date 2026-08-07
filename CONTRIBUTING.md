# Contributing to Storm Financial Command Center (SFCC)

This document defines the development workflow and contribution standards for SFCC.

The goal is to keep changes small, testable, readable, and consistent with the project's architecture.

Before making changes, read:

- `ARCHITECTURE.md`
- `ROADMAP.md`
- `CHANGELOG.md`

---

# 1. Development Workflow

Use this sequence for normal development:

```text
1. Pull the latest code.
2. Make one logical change.
3. Run SFCC.
4. Test the affected pages.
5. Review `git status`.
6. Commit the working change.
7. Update CHANGELOG.md when appropriate.
8. Push the commit.
```

Avoid combining unrelated changes in one commit.

Good:

```text
Refactor Transactions page
```

Bad:

```text
Refactor Transactions + add investments + redesign dashboard + fix receipts
```

Small commits are easier to test, understand, and reverse.

---

# 2. Coding Standards

## Python Files

Use lowercase snake_case:

```text
main.py
database.py
migrations.py
transactions_card.py
```

## Functions and Variables

Use snake_case:

```python
get_monthly_summary()
transaction_id
expected_amount
```

## Classes

Use PascalCase:

```python
TransactionsPage
TransactionCard
DashboardCard
```

## Constants

Use uppercase:

```python
DB_NAME
```

---

# 3. Responsibility Rules

Follow the rules in `ARCHITECTURE.md`.

In short:

```text
Pages coordinate UI.
Widgets display reusable UI.
Database functions persist and retrieve data.
Shared calculations have one source of truth.
Python calculates.
Hermes interprets.
```

Do not duplicate calculations in multiple pages.

Do not put SQL inside page files.

Do not put Tkinter UI code inside database functions.

---

# 4. Function Design

Each function should have one clear responsibility.

Preferred:

```python
def delete_transaction(transaction_id):
    ...
```

Avoid functions that simultaneously:

- query data,
- calculate analytics,
- modify unrelated records,
- update UI,
- and perform formatting.

If a function is hard to describe in one sentence, consider splitting it.

---

# 5. Reuse Before Adding

Before creating a new function, widget, or calculation, search the codebase.

Ask:

1. Does this already exist?
2. Can an existing function be extended safely?
3. Is there already a reusable widget for this?
4. Is this calculation already available from a summary function?
5. Would this duplicate logic?

Prefer reuse over duplication.

---

# 6. Database Changes

Database schema changes require care.

Before changing the schema:

1. Check the current schema.
2. Determine whether existing users need a migration.
3. Update `migrations.py` if required.
4. Ensure new installs receive the current schema.
5. Test both startup and affected pages.

Do not manually add the same column in multiple migrations.

Do not run migrations during ordinary database reads or writes.

---

# 7. Database Connection Rules

`connect()` should only open a SQLite connection.

It should not:

- run migrations,
- create tables,
- perform queries,
- modify application state.

Migrations should run during application initialization.

Always close database connections when finished.

---

# 8. Transaction Rules

Transactions are the core financial record.

Use these transaction types exactly:

```text
Income
Expense
```

Transactions should include an explicit date.

Vendor memory may learn from Expense transactions.

Income entries should not pollute expense vendor memory.

Transaction changes should refresh affected UI.

---

# 9. Widget Rules

Create a reusable widget when the same UI pattern is used repeatedly or has meaningful standalone behavior.

Examples:

```text
TransactionCard
DashboardCard
Sidebar
ProgressBar
```

Do not create a separate widget file for a tiny one-off label or frame unless reuse is likely.

Keep the widget library useful, not ceremonial.

---

# 10. Page Rules

Pages should:

- build layout,
- read user input,
- perform basic validation,
- call shared functions,
- refresh displayed data.

Pages should not:

- contain SQL,
- duplicate financial calculations,
- run migrations,
- manage application-wide business rules.

---

# 11. Error Handling

Avoid broad exception handling.

Bad:

```python
try:
    ...
except:
    pass
```

Preferred:

```python
try:
    amount = float(value)
except ValueError:
    return
```

Important errors should not disappear silently.

---

# 12. Debugging Code

Temporary debugging is allowed during development.

Examples:

```python
print(...)
check_database.py
temporary SQL queries
```

Before committing:

- remove temporary prints,
- delete throwaway scripts,
- or convert useful checks into tests.

Do not leave mystery debugging artifacts in the repository.

---

# 13. Testing Before Commit

At minimum, run:

```powershell
py main.py
```

Then test the areas affected by the change.

For broad database or architecture changes, check:

```text
Dashboard
Transactions
Income
Budgets
Recurring
Receipts
```

Also confirm:

- no terminal traceback,
- no database lock errors,
- expected data still appears,
- add/delete/update behavior still works where affected.

---

# 14. Commit Messages

Use descriptive commit messages.

Preferred:

```text
v0.3.6 - Simplify database connection handling
v0.3.7 - Refactor transaction cards
v0.3.8 - Add transaction search
```

Avoid:

```text
fix
stuff
update
oops
changes
```

A commit message should explain what changed without opening the diff.

---

# 15. Git Hygiene

Never commit:

```text
data/*.db
__pycache__/
*.pyc
venv/
.venv/
.env
```

Keep `.gitignore` current.

Use:

```text
data/.gitkeep
```

to preserve an otherwise empty local data directory.

---

# 16. Changelog Rules

Update `CHANGELOG.md` for meaningful user-facing or architectural changes.

Use sections such as:

```text
Added
Changed
Fixed
Removed
Security
```

Minor formatting changes do not require a changelog entry.

---

# 17. Roadmap Rules

New major work should align with `ROADMAP.md`.

If priorities change, update the roadmap rather than allowing the codebase and roadmap to drift apart.

The roadmap is a planning document, not a prison. Change it deliberately.

---

# 18. Architecture Rules

All new features should follow `ARCHITECTURE.md`.

Before adding a feature, answer:

1. Where does this logic belong?
2. What is the single source of truth?
3. Does this require a reusable widget?
4. Does this require a migration?
5. Does an existing function already provide the data?
6. Can this remain useful without Hermes?

If ownership is unclear, design the feature before coding it.

---

# 19. Refactoring Rules

Refactoring should preserve behavior unless the behavior change is intentional and documented.

Preferred sequence:

```text
Identify duplication
Redirect callers
Test
Remove dead code
Test again
Commit
```

Do not perform large speculative rewrites when a smaller controlled refactor will work.

---

# 20. Hermes Rules

Hermes is an interpretation layer.

Hermes may:

- explain trends,
- identify patterns,
- suggest actions,
- flag anomalies,
- summarize financial state.

Hermes should not be the authoritative source for:

- balances,
- budget totals,
- transaction totals,
- net cash flow,
- deterministic calculations.

Rule:

```text
Python calculates.
Hermes interprets.
```

---

# 21. Pull Request Guidance

If SFCC later uses pull requests, each PR should:

- address one logical feature or refactor,
- explain what changed,
- explain how it was tested,
- mention any schema changes,
- update documentation when necessary.

Large unrelated PRs should be split.

---

# 22. Definition of Done

A change is complete when:

- the intended behavior works,
- affected pages were tested,
- no new traceback appears,
- duplicate logic was not introduced,
- architecture rules are respected,
- documentation is updated when appropriate,
- the change is committed cleanly.

---

# 23. Golden Contribution Rule

The preferred outcome of every change is:

```text
Same or better functionality
Less duplication
Clearer ownership
Fewer failure points
Readable code
```

Do not add complexity unless the feature genuinely requires it.
