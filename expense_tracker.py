import json
import os
import argparse
from datetime import datetime
import calendar

FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(description, amount):
    data = load_expenses()
    data_id = len(data) + 1
    expense = {
        "id": data_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": int(amount)
    }
    data.append(expense)
    save_expenses(data)
    print(f"Expense added successfully (ID:{data_id})")

def list_expenses():
    data = load_expenses()
    print("# ID  Date       Description  Amount")
    for expense in data:
        print(f"# {expense['id']}   {expense['date']}  {expense['description']}       ${expense['amount']}")

def delete_expenses(expense_id):
    data = load_expenses()
    for expense in data:
        if expense["id"] == expense_id:
            data.remove(expense)
            save_expenses(data)
            print(f"Expense deleted successfully")
            return 
    print("Expense ID not found")

def summary_expenses(month=None):
    data = load_expenses()
    amount_sum = 0
    for expense in data:
        expense_month = datetime.strptime(expense["date"], "%Y-%m-%d").month
        if month and expense_month == month:
            amount_sum += int(expense["amount"])
        elif not month:
            amount_sum += int(expense["amount"])

    if month:
        month_name = calendar.month_name[month]
        print(f"Total expenses for {month_name}: ${amount_sum}")
    else:
        print(f'Total expenses: ${amount_sum}')

def update_expenses(expense_id, new_description, new_amount):
    data = load_expenses()
    for expense in data:
        if expense["id"] == expense_id:
            expense["description"] = new_description
            expense["amount"] = new_amount
            save_expenses(data)
            print(f"Expense updated successfully!")
            return 
    print(f"Expense ID-{expense_id} cannot be found")

def main():
    parser = argparse.ArgumentParser(prog="expense-tracker", description="Expense Tracker CLI")
    sub_parser = parser.add_subparsers(dest="command")

    add_parser = sub_parser.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--description", required=True, type=str, help="Description of the expense")
    add_parser.add_argument("--amount", required=True, type=float, help="Amount of the expense")

    sub_parser.add_parser("list", help="List all expenses")

    delete_parser = sub_parser.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", required=True, type=int, help="ID of the expense to delete")

    summary_parser = sub_parser.add_parser("summary", help="Summary of all expenses or summary of expenses by specific month")
    summary_parser.add_argument(
       "--month", 
        nargs="?", 
        type=int, 
        choices=range(1, 13), 
        help="Filter expenses by month"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "delete":
        delete_expenses(args.id)  # Correct function call here
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        if args.month:
            summary_expenses(args.month)
        else:
            summary_expenses()

if __name__ == "__main__":
    main()
