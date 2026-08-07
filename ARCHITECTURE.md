# Storm Financial Command Center (SFCC) Architecture

## Purpose

This document defines the architectural rules for SFCC.

The goal is simple:

- Keep the codebase small.
- Keep responsibilities clear.
- Avoid duplicate logic.
- Make future features easy to add.
- Preserve existing functionality while the project grows.
- Prefer simple, readable code over unnecessary abstraction.

SFCC should remain easy to understand even as Transactions, Budgets, Receipts, Investments, Reports, and Hermes become more capable.

---

# 1. Core Principles

## 1.1 One Responsibility Per Function

Each function should do one clear job.

Good:

```python
def get_transactions():
    ...

def delete_transaction(transaction_id):
    ...
```

Avoid functions that:

- query the database,
- calculate analytics,
- update the UI,
- and perform unrelated side effects

all at once.

If a function becomes difficult to describe in one sentence, it probably owns too much.

---

## 1.2 One Source of Truth

Every financial calculation should have one authoritative implementation.

Examples:

- Monthly income
- Monthly expenses
- Monthly net cash flow
- Budget remaining
- Income variance
- Upcoming recurring transactions

Do not create multiple functions that calculate the same value independently.

Preferred:

```python
summary = get_monthly_summary()
income = summary["income"]
```

Avoid:

```python
get_monthly_income()
get_actual_income()
calculate_income_again_somewhere_else()
```

Duplicate calculations eventually disagree. Humans already provide enough disagreement without asking the software to join in.

---

## 1.3 Keep the Simplest Architecture That Works

Do not add layers simply because large enterprise systems use them.

SFCC should not contain:

- unnecessary repository classes,
- dependency-injection frameworks,
- abstract factories,
- duplicated service wrappers,
- abstractions with only one implementation.

Add a new layer only when it removes duplication or makes responsibilities meaningfully clearer.

---

# 2. Application Layers

SFCC uses four primary layers.

```text
User
  |
  v
Pages
  |
  v
Reusable Widgets
  |
  v
Database / Business Functions
  |
  v
SQLite
```

Hermes and analytics will eventually consume the same business functions rather than duplicating financial calculations.

---

# 3. Pages

Location:

```text
pages/
```

Pages own application screens and user interaction.

Examples:

```text
dashboard.py
transactions.py
budgets.py
income.py
recurring.py
receipts.py
investments.py
reports.py
goals.py
settings.py
```

## Pages May

- Create page layouts.
- Read values from widgets.
- Validate basic user input.
- Call database/business functions.
- Refresh displayed data.
- Coordinate reusable widgets.

## Pages Should Not

- Contain SQL.
- Recalculate financial metrics already available elsewhere.
- Duplicate database logic.
- Manage database connections directly.
- Contain reusable UI components that belong in `widgets/`.

Example:

```python
def save_transaction(self):

    add_transaction(
        description,
        category,
        amount,
        transaction_type,
        transaction_date
    )

    self.load_transactions()
```

The page coordinates the action. The database layer owns persistence.

---

# 4. Widgets

Location:

```text
widgets/
```

Widgets are reusable visual components.

Examples:

```text
sidebar.py
cards.py
progress_bar.py
transactions_card.py
```

## Widgets May

- Display data.
- Format values for presentation.
- Expose buttons or callbacks.
- Notify the parent page when an action occurs.

## Widgets Should Not

- Recalculate application-wide financial metrics.
- Own database schema logic.
- Run migrations.
- Duplicate page-level workflows.

A widget may call a narrow database action when that behavior is intrinsic to the component, but callback-based coordination is preferred when practical.

Example:

```python
TransactionCard(
    parent,
    transaction,
    refresh_callback=self.load_transactions
)
```

---

# 5. Database Layer

The database layer owns persistence and shared financial calculations.

Current implementation:

```text
database.py
migrations.py
```

Long-term target:

```text
database/
    connection.py
    transactions.py
    planning.py
    receipts.py
    migrations.py
```

Do not split `database.py` merely to reduce line count. Split it when its internal sections are stable and cohesive enough to move without changing behavior.

## Database Layer Owns

- SQLite connections.
- CRUD operations.
- Transaction persistence.
- Budget persistence.
- Income forecasts.
- Recurring transactions.
- Receipt relationships.
- Vendor memory.
- Shared financial summaries.

## Database Layer Does Not Own

- Tkinter widgets.
- Page layout.
- User-facing dialogs.
- Visual formatting.
- Hermes prompt construction.

---

# 6. Database Connections

`connect()` has one responsibility:

```python
def connect():
    return sqlite3.connect(
        DB_NAME,
        timeout=10
    )
```

It should not:

- run migrations,
- initialize tables,
- perform queries,
- modify application state.

Database migrations run during application initialization, not every time a database connection is opened.

Expected startup flow:

```text
main.py
   |
   v
initialize_database()
   |
   +--> run_migrations()
   |
   +--> ensure current tables exist
   |
   v
Application starts
```

---

# 7. Database Schema Changes

Schema changes must be deliberate.

## New Install

`initialize_database()` must be capable of creating the current required schema.

## Existing Install

`migrations.py` upgrades older databases safely.

## Rules

- Do not manually add the same column in multiple places.
- Do not create migrations for fields that already exist without checking schema state.
- Do not run migrations on every normal database connection.
- A migration should perform one clearly defined schema change.
- Migration order must remain deterministic.

---

# 8. Transactions

Transactions are the central financial record in SFCC.

Canonical transaction data:

```text
id
date
category
description
amount
type
```

Transaction type should use consistent values:

```text
Income
Expense
```

Avoid alternate spellings or casing.

## Transaction Rules

- Every transaction has an explicit date.
- The UI may default the date to today.
- The database stores the date supplied by the user.
- Expense transactions may update vendor memory.
- Income transactions should not pollute expense vendor memory.
- Transaction deletion must refresh affected UI.
- Transaction display should use reusable transaction cards.

---

# 9. Vendor Memory

Vendor memory provides lightweight transaction intelligence without requiring Hermes.

Example:

```text
Walmart -> Groceries
Shell   -> Fuel
```

Vendor memory should:

- learn only from appropriate transactions,
- suggest rather than blindly override user choices,
- remain deterministic,
- remain usable without AI access.

Hermes may later enhance vendor intelligence, but basic vendor memory must continue working independently.

---

# 10. Receipts

Receipts are optional financial records.

A transaction does not require a receipt.

A receipt may exist without an attachment.

Receipt relationships should support:

```text
receipt -> transaction
```

Receipt matching logic should remain separate from receipt presentation.

Future receipt features may include:

- image/PDF attachment,
- OCR,
- automatic vendor extraction,
- transaction matching,
- tax documentation,
- warranty tracking.

These features should extend the existing receipt model rather than create parallel receipt systems.

---

# 11. Monthly Financial Summary

`get_monthly_summary()` is the authoritative source for:

```text
income
expenses
net
```

Example result:

```python
{
    "income": 4000.00,
    "expenses": 1750.00,
    "net": 2250.00
}
```

Other pages and features should consume this result rather than independently querying monthly income or expenses.

This applies to:

- Dashboard
- Income page
- Reports
- Hermes
- Future analytics

---

# 12. Income Forecasting

SFCC distinguishes between:

```text
Expected Income
Actual Income
Variance
```

Expected income comes from forecasts.

Actual income comes from transactions.

Variance is:

```text
actual - expected
```

Actual income calculations should reuse the monthly summary rather than create a separate income query.

---

# 13. Budgets

Budgets represent planned spending.

Budget functions should clearly distinguish:

```text
budget limit
actual spending
remaining amount
percentage used
```

Budget calculations must respect the requested month and year.

Avoid mixing all-time spending with monthly budget calculations unless a function is explicitly intended to be all-time.

---

# 14. Recurring Transactions

Recurring transactions represent scheduled future financial events.

They may be:

```text
Income
Expense
```

Recurring processing should:

1. Find due recurring records.
2. Create a transaction.
3. Advance the next scheduled date.
4. Avoid duplicate processing.

Recurring transaction logic belongs in the database/business layer.

The UI only manages recurring records and displays status.

---

# 15. Dashboard

The Dashboard consumes shared financial information.

It should not become a second analytics engine.

Preferred:

```python
summary = get_monthly_summary()
variance = get_income_variance()
upcoming = get_upcoming_recurring_transactions()
```

The Dashboard then displays those values.

The Dashboard should eventually support:

- actual income,
- projected income,
- income variance,
- actual expenses,
- projected expenses,
- cash flow,
- budget health,
- upcoming bills,
- recent transactions,
- financial alerts.

Calculations remain outside the page wherever practical.

---

# 16. Hermes

Hermes is an analysis layer, not a replacement for deterministic financial logic.

Hermes should consume structured SFCC data.

Example:

```text
monthly summary
budget status
income variance
upcoming obligations
investment holdings
transaction patterns
```

Hermes may:

- explain,
- summarize,
- identify patterns,
- provide suggestions,
- flag unusual activity.

Hermes should not be the authoritative calculator for balances, budgets, or transaction totals.

Rule:

```text
Python calculates.
Hermes interprets.
```

This keeps financial numbers deterministic and auditable.

---

# 17. Investments

Investment functionality should remain separate from normal cash transactions where appropriate, while still supporting transfers and contributions.

Future investment modules may track:

- accounts,
- holdings,
- cost basis,
- contributions,
- dividends,
- DRIP,
- allocation,
- performance,
- projected dividend income,
- retirement projections.

Investment calculations should have one source of truth just like cash-flow calculations.

---

# 18. Naming Conventions

Use lowercase snake_case for Python files.

Preferred:

```text
main.py
database.py
config.py
transactions_card.py
```

Functions and variables:

```python
get_monthly_summary()
transaction_id
expected_amount
```

Classes:

```python
TransactionsPage
TransactionCard
DashboardCard
```

Constants:

```python
DB_NAME
```

Avoid mixing singular/plural class names for the same component.

---

# 19. Data Access

Existing code currently uses SQLite tuples.

Example:

```python
transaction[4]
```

New code should avoid introducing additional fragile positional assumptions where practical.

Long-term target:

```python
conn.row_factory = sqlite3.Row
```

allowing:

```python
transaction["amount"]
transaction["date"]
```

Do not convert the entire codebase at once unless the change is isolated and fully tested.

---

# 20. Error Handling

Do not silently ignore important failures.

Avoid:

```python
except:
    pass
```

Prefer narrow exception handling:

```python
except ValueError:
    return
```

For user-input failures, the UI should eventually display understandable feedback.

Database failures should not be silently converted into incorrect financial values.

---

# 21. Debug Code

Temporary debugging code must not become permanent production behavior.

Examples:

```python
print(...)
check_database.py
temporary SQL scripts
```

Once debugging is complete:

- remove it,
- convert it into a proper test,
- or move it into a deliberate developer utility.

---

# 22. Git and Local Data

Never commit live financial databases or secrets.

`.gitignore` must exclude:

```text
data/*.db
*.db-journal
*.db-wal
*.db-shm
.env
venv/
.venv/
__pycache__/
*.pyc
```

The repository may preserve the empty `data/` directory using:

```text
data/.gitkeep
```

User financial information remains local unless an explicit secure synchronization system is built later.

---

# 23. Testing Rule

Every meaningful refactor follows this sequence:

```text
1. Identify current behavior.
2. Make one focused change.
3. Run SFCC.
4. Test affected pages.
5. Commit working state.
6. Continue.
```

Do not combine unrelated refactors in one change.

A successful refactor should ideally produce:

```text
Same behavior
Less duplication
Clearer ownership
Fewer failure points
```

---

# 24. Feature Development Rule

Before adding a new feature, ask:

1. Does an existing function already provide this data?
2. Does an existing widget already provide this presentation pattern?
3. Is this business logic or UI logic?
4. What is the single source of truth?
5. Can this be added without duplicating an existing calculation?
6. Does this feature require a schema migration?
7. Can the feature remain useful without Hermes?

If these questions cannot be answered clearly, the feature design is not ready.

---

# 25. Refactoring Rule

Do not refactor merely because a file is long.

Refactor when:

- responsibilities are mixed,
- logic is duplicated,
- code becomes hard to locate,
- functions repeatedly change together,
- a section has become a stable standalone domain.

The goal is maintainability, not winning a contest for the most folders.

---

# 26. Current Architectural Direction

The intended evolution is:

```text
Current
-------

main.py
database.py
migrations.py
pages/
widgets/


Intermediate
------------

main.py
database.py
migrations.py
pages/
widgets/

Clean duplicated logic first.


Later
-----

main.py

database/
    connection.py
    transactions.py
    planning.py
    receipts.py
    migrations.py

pages/
widgets/
```

The split into database modules occurs only after the current database sections are internally clean.

---

# 27. SFCC Design Philosophy

SFCC should answer four questions:

```text
What happened?
Why did it happen?
What is coming next?
What should I do about it?
```

The database answers:

```text
What happened?
```

Forecasting and analytics answer:

```text
What is coming next?
```

Hermes helps answer:

```text
Why did it happen?
What should I do about it?
```

The architecture should preserve those boundaries.

---

# 28. Golden Rules

When in doubt:

```text
One function = one job.

One calculation = one source of truth.

Pages coordinate.

Widgets display.

Database persists.

Python calculates.

Hermes interprets.

Migrations change schema.

Git never stores personal financial data.

Working code gets committed before the next refactor.
```

If a proposed change violates several of these rules, reconsider the design before writing more code.
