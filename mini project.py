import json
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# File to store expense data
DATA_FILE = 'expenses.json'

# Load existing expenses from file
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

# Save expenses to file
def save_expenses(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

# Add a new expense
def add_expense(expenses):
    try:
        amount = float(input("Enter amount: $"))
        category = input("Enter category (e.g., Food, Transport): ").strip()
        date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
        if date_input:
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
        else:
            date_obj = datetime.now()
        expense = {
            'amount': amount,
            'category': category,
            'date': date_obj.strftime("%Y-%m-%d")
        }
        expenses.append(expense)
        print("Expense added successfully.")
    except ValueError:
        print("Invalid input. Please try again.")

# View summary of expenses
def view_summary(expenses):
    if not expenses:
        print("No expenses recorded.")
        return
    
    print("\n--- Expense Summary ---")
    total_overall = 0
    category_totals = defaultdict(float)
    date_totals = defaultdict(float)  # for daily, weekly, monthly summaries
    
    for exp in expenses:
        amount = exp['amount']
        total_overall += amount
        category_totals[exp['category']] += amount
        
        date_obj = datetime.strptime(exp['date'], "%Y-%m-%d")
        day_str = date_obj.strftime("%Y-%m-%d")
        week_str = date_obj.strftime("%Y-W%U")
        month_str = date_obj.strftime("%Y-%m")
        date_totals['Daily ' + day_str] += amount
        date_totals['Weekly ' + week_str] += amount
        date_totals['Monthly ' + month_str] += amount
    
    print(f"Total expenditure: ${total_overall:.2f}")
    print("\nSpending by Category:")
    for cat, total in category_totals.items():
        print(f" - {cat}: ${total:.2f}")
    
    print("\nSpending over time:")
    for period, total in date_totals.items():
        print(f" {period}: ${total:.2f}")
    print("------------------------\n")
    
    # Plotting graphical summaries
    plot_expenses(category_totals, total_overall)

def plot_expenses(category_totals, total_overall):
    # Pie chart for category distribution
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    
    # Bar chart for overall spending
    plt.subplot(1, 2, 2)
    plt.bar(['Total Spending'], [total_overall], color='skyblue')
    plt.ylabel('Amount ($)')
    plt.title('Total Spending')
    
    plt.tight_layout()
    plt.show()

# Delete an expense
def delete_expense(expenses):
    if not expenses:
        print("No expenses to delete.")
        return
    print("Expenses:")
    for idx, exp in enumerate(expenses, 1):
        print(f"{idx}. ${exp['amount']:.2f} | {exp['category']} | {exp['date']}")
    try:
        choice = int(input("Enter the number of the expense to delete: "))
        if 1 <= choice <= len(expenses):
            del expenses[choice - 1]
            print("Expense deleted.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

# Edit an expense
def edit_expense(expenses):
    if not expenses:
        print("No expenses to edit.")
        return
    print("Expenses:")
    for idx, exp in enumerate(expenses, 1):
        print(f"{idx}. ${exp['amount']:.2f} | {exp['category']} | {exp['date']}")
    try:
        choice = int(input("Enter the number of the expense to edit: "))
        if 1 <= choice <= len(expenses):
            exp = expenses[choice - 1]
            print(f"Editing expense: ${exp['amount']:.2f} | {exp['category']} | {exp['date']}")
            new_amount = input(f"Enter new amount (or press Enter to keep ${exp['amount']:.2f}): ").strip()
            new_category = input(f"Enter new category (or press Enter to keep '{exp['category']}'): ").strip()
            new_date = input(f"Enter new date (YYYY-MM-DD) or press Enter to keep '{exp['date']}': ").strip()
            
            if new_amount:
                exp['amount'] = float(new_amount)
            if new_category:
                exp['category'] = new_category
            if new_date:
                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    exp['date'] = new_date
                except ValueError:
                    print("Invalid date format. Keeping original date.")
            print("Expense updated.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

# Main menu
def main():
    expenses = load_expenses()
    while True:
        print("Personal Expense Tracker")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Delete Expense")
        print("4. Edit Expense")
        print("5. Exit")
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            add_expense(expenses)
            save_expenses(expenses)
        elif choice == '2':
            view_summary(expenses)
        elif choice == '3':
            delete_expense(expenses)
            save_expenses(expenses)
        elif choice == '4':
            edit_expense(expenses)
            save_expenses(expenses)
        elif choice == '5':
            save_expenses(expenses)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()