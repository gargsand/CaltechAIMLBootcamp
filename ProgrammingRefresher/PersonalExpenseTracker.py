import os

import pandas as pd

EXPENSES_FILE = "expenses.xlsx"
expenses = {}
budget = {}


def load_expenses_and_budget():
    global expenses, budget
    if os.path.exists(EXPENSES_FILE):
        with pd.ExcelFile(EXPENSES_FILE) as xls:
            for sheet_name in xls.sheet_names:
                if sheet_name == "Budget":
                    budget_df = pd.read_excel(xls, sheet_name=sheet_name)
                    budget = {row['Person']: row['Budget'] for _, row in budget_df.iterrows()}
                else:
                    expenses[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name).to_dict(orient='records')


def save_expenses():
    with pd.ExcelWriter(EXPENSES_FILE) as writer:
        for user, records in expenses.items():
            df = pd.DataFrame(records)
            df.to_excel(writer, sheet_name=user, index=False)
        budget_df = pd.DataFrame([{'Person': person, 'Budget': amount} for person, amount in budget.items()])
        budget_df.to_excel(writer, sheet_name="Budget", index=False)


def add_expense():
    user = input("Enter the name of the person the expense is for: ")
    if user not in expenses:
        create_new = input(f"No record found for {user}. Do you want to create a new sheet? (yes/no): ")
        if create_new.lower() != 'yes':
            return
        expenses[user] = []

    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the category (e.g., Food, Travel, Bills): ")
    amount = float(input("Enter the amount spent: "))
    description = input("Enter a brief description: ")

    expenses[user].append({'Date': date, 'Category': category, 'Amount': amount, 'Description': description})
    print("Expense added successfully!")


def view_expenses():
    user = input("Enter the name of the person: ")
    if user not in expenses or not expenses[user]:
        print(f"No expenses recorded yet for {user}.")
    else:
        print(f"\nExpenses for {user}:")
        for exp in expenses[user]:
            print(f"{exp['Date']} | {exp['Category']} | ${exp['Amount']:.2f} | {exp['Description']}")


def set_budget():
    user = input("Enter the name of the person: ")
    amount = float(input(f"Enter the monthly budget for {user}: "))
    budget[user] = amount
    print(f"Budget set to ${amount:.2f} for {user}")


def track_budget():
    user = input("Enter the name of the person: ")
    total_spent = sum(exp['Amount'] for exp in expenses.get(user, []))
    user_budget = budget.get(user, 0)
    print(f"Total expenses for {user}: ${total_spent:.2f}")
    if total_spent > user_budget:
        print(f"Warning: {user} has exceeded their budget!")
    else:
        print(f"Remaining budget for {user}: ${user_budget - total_spent:.2f}")


if __name__ == "__main__":
    load_expenses_and_budget()
    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Set Budget")
        print("4. Track Budget")
        print("5. Save & Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            set_budget()
        elif choice == '4':
            track_budget()
        elif choice == '5':
            save_expenses()
            print("Expenses saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
