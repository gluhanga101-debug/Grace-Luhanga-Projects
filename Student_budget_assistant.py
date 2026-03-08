"""
Student Budget Assistant
- User input/output, loops, conditionals, lists, dicts, functions, and a class.
- Plan categories, enter expenses, check savings goal, and get cut suggestions.
"""

# ---------- Simple class to hold plan + actuals ----------
class Budget:
    def __init__(self, monthly_income: float, savings_goal: float):
        self.monthly_income = monthly_income
        self.savings_goal = savings_goal
        self.planned: dict[str, float] = {}         # category -> planned $
        self.expenses: dict[str, list[float]] = {}  # category -> list of $ amounts

    def add_category(self, name: str, planned_amount: float) -> None:
        self.planned[name] = planned_amount
        self.expenses.setdefault(name, [])

    def add_expense(self, category: str, amount: float) -> bool:
        if category not in self.planned:
            return False
        self.expenses[category].append(amount)
        return True

    def totals(self) -> tuple[float, float, float]:
        total_planned = sum(self.planned.values())
        total_spent = sum(sum(v) for v in self.expenses.values())
        leftover_before_saving = self.monthly_income - total_spent
        return total_planned, total_spent, leftover_before_saving


# ---------- Input helpers ----------
def ask_float(prompt: str, min_value: float = 0.0) -> float:
    while True:
        try:
            val = float(input(prompt).strip())
            if val < min_value:
                print(f"Please enter a number ≥ {min_value}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number (e.g., 123.45).")

def ask_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter a non-empty value.")


# ---------- Analysis ----------
def category_variances(b: Budget) -> list[tuple[str, float]]:
    """
    [(category, variance)] where variance = planned - actual.
    Positive = under budget, Negative = over budget. Sorted worst first.
    """
    rows: list[tuple[str, float]] = []
    for cat, planned in b.planned.items():
        actual = sum(b.expenses.get(cat, []))
        rows.append((cat, round(planned - actual, 2)))
    rows.sort(key=lambda x: x[1])  # most negative (over) first
    return rows

def suggest_cuts(b: Budget, needed: float) -> list[tuple[str, float]]:
    """
    Suggest trims from under-spent categories to close a shortfall.
    Greedy: largest positive variance first.
    """
    suggestions: list[tuple[str, float]] = []
    slack = [(c, v) for c, v in category_variances(b) if v > 0]
    slack.sort(key=lambda x: x[1], reverse=True)

    remaining = needed
    for cat, avail in slack:
        if remaining <= 0:
            break
        cut = min(avail, remaining)
        suggestions.append((cat, round(cut, 2)))
        remaining -= cut
    return suggestions


# ---------- Flow ----------
def set_up_budget() -> Budget:
    print("=== Student Budget Assistant ===")
    income = ask_float("Monthly income (after tax): $", 0.0)
    goal = ask_float("Savings goal this month: $", 0.0)
    b = Budget(income, goal)

    print("\nAdd planned categories (e.g., Rent, Food, Transport).")
    print("Type 'done' when finished.")
    while True:
        name = input("Category (or 'done'): ").strip()
        if not name:
            print("Please enter a category name or 'done'.")
            continue
        if name.lower() == "done":
            if not b.planned:
                print("Add at least one category.")
                continue
            break
        amt = ask_float(f"Planned monthly amount for '{name}': $", 0.0)
        b.add_category(name, amt)

    total_planned = sum(b.planned.values())
    buffer = income - goal
    if total_planned > buffer:
        print("\n⚠️  Warning: planned total exceeds income minus savings goal.")
        print(f"Planned: ${total_planned:.2f} vs Buffer: ${buffer:.2f}")
    return b

def enter_expenses(b: Budget) -> None:
    print("\nEnter expenses (type 'done' to stop).")
    print(f"Categories: {', '.join(b.planned.keys())}")
    while True:
        cat = input("Category (or 'done'): ").strip()
        if cat.lower() == "done":
            break
        if cat not in b.planned:
            print("Unknown category. Use one from your plan.")
            continue
        amt = ask_float(f"Expense for '{cat}': $", 0.01)
        b.add_expense(cat, amt)

def report(b: Budget) -> None:
    print("\n=== Monthly Report ===")
    total_planned, total_spent, leftover_before_saving = b.totals()
    print(f"Income:                 ${b.monthly_income:.2f}")
    print(f"Savings goal:           ${b.savings_goal:.2f}")
    print(f"Total planned spending: ${total_planned:.2f}")
    print(f"Total actual spending:  ${total_spent:.2f}")
    print(f"Leftover before saving: ${leftover_before_saving:.2f}")

    print("\nCategory breakdown (Planned / Actual / Variance):")
    print("-" * 62)
    for cat in b.planned:
        planned = b.planned[cat]
        actual = sum(b.expenses.get(cat, []))
        var = planned - actual
        print(f"{cat:<15} ${planned:>7.2f}  /  ${actual:>7.2f}  /  ${var:>7.2f}")

    # Savings decision
    if leftover_before_saving >= b.savings_goal:
        print(f"\n You can meet your savings goal of ${b.savings_goal:.2f}.")
        surplus = leftover_before_saving - b.savings_goal
        print(f"Projected cash after saving: ${surplus:.2f}")
    else:
        short = b.savings_goal - leftover_before_saving
        print(f"\n Short by ${short:.2f} to meet your savings goal.")
        cuts = suggest_cuts(b, short)
        if cuts:
            print("Suggested trims to close the gap:")
            for cat, cut in cuts:
                print(f"  - Reduce '{cat}' by about ${cut:.2f}")
        else:
            print("No under-spent categories to cut. Consider revising plan or income.")

def main():
    b = set_up_budget()
    enter_expenses(b)
    while True:
        report(b)
        print("\nOptions: [A]dd expense  [R]eport again  [Q]uit")
        choice = input("Choose: ").strip().lower()
        if choice == "a":
            enter_expenses(b)
        elif choice == "r":
            continue
        elif choice == "q":
            print("Good luck with your budgeting! 🧮")
            break
        else:
            print("Please choose A, R, or Q.")

if __name__ == "__main__":
    main()
