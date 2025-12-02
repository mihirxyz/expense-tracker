import json
import os
from datetime import datetime
import csv

DATA_FILE = "data.json"
CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Health", "Education", "Other"]


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def divider():
    print("-" * 60)


def choose_category():
    print("\nSelect Category:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}. {cat}")
    while True:
        choice = input("Enter choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid category. Try again.")


def add_expense():
    print("\n== Add Expense ==")
    try:
        amount = float(input("Amount (₹): "))
    except:
        print("Invalid amount.")
        return

    category = choose_category()
    note = input("Note (optional): ")

    entry = {
        "id": int(datetime.now().timestamp() * 1000),
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data = load_data()
    data.append(entry)
    save_data(data)
    print("✔ Expense added successfully!")


def view_expenses():
    data = load_data()
    if not data:
        print("\nNo expenses recorded.\n")
        return

    data = sorted(data, key=lambda x: x["date"], reverse=True)

    print("\n== All Expenses ==")
    divider()
    for e in data:
        print(f"ID: {e['id']}")
        print(f"Date: {e['date']}")
        print(f"Amount: ₹{e['amount']}")
        print(f"Category: {e['category']}")
        print(f"Note: {e['note']}")
        divider()


def delete_expense():
    view_expenses()
    data = load_data()

    if not data:
        return

    val = input("Enter ID to delete: ")
    if not val.isdigit():
        print("Invalid ID.")
        return

    val = int(val)
    new_data = [d for d in data if d["id"] != val]

    if len(new_data) == len(data):
        print("No entry found with that ID.")
        return

    save_data(new_data)
    print("✔ Expense deleted.")


def update_expense():
    view_expenses()
    data = load_data()

    if not data:
        return

    val = input("Enter ID to update: ")
    if not val.isdigit():
        print("Invalid ID.")
        return
    val = int(val)

    for e in data:
        if e["id"] == val:
            print("\n== Update Fields (press Enter to skip) ==")
            amt = input("New Amount: ")
            if amt.strip():
                try:
                    e["amount"] = float(amt)
                except:
                    print("Invalid amount, skipping.")

            print("\nNew Category:")
            print("(press Enter to skip)")
            for i, c in enumerate(CATEGORIES, start=1):
                print(f"{i}. {c}")
            cat = input("Category number: ")
            if cat.isdigit() and 1 <= int(cat) <= len(CATEGORIES):
                e["category"] = CATEGORIES[int(cat) - 1]

            nt = input("New Note: ")
            if nt.strip():
                e["note"] = nt

            save_data(data)
            print("✔ Updated.")
            return

    print("ID not found.")


def monthly_summary():
    data = load_data()
    if not data:
        print("\nNo expenses yet.\n")
        return

    year = input("Year (YYYY) [Enter for current]: ")
    if not year:
        year = datetime.now().strftime("%Y")

    month = input("Month (01-12) [Enter for current]: ")
    if not month:
        month = datetime.now().strftime("%m")

    filtered = []
    category_totals = {}
    total = 0

    for e in data:
        d = datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S")
        if str(d.year) == year and f"{d.month:02d}" == month:
            filtered.append(e)
            total += e["amount"]
            category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]

    if not filtered:
        print(f"\nNo expenses for {year}-{month}.\n")
        return

    print(f"\n== Summary for {year}-{month} ==")
    divider()
    print(f"Total spent: ₹{total}")
    print("\nCategory breakdown:")
    for cat, amt in category_totals.items():
        print(f"- {cat}: ₹{amt}")

    top = max(category_totals, key=category_totals.get)
    print(f"\nTop category: {top} (₹{category_totals[top]})")
    divider()


def export_csv():
    data = load_data()
    if not data:
        print("No data to export.")
        return

    filename = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "amount", "category", "note"])
        for e in data:
            writer.writerow([e["id"], e["date"], e["amount"], e["category"], e["note"]])

    print(f"✔ CSV exported: {filename}")


def clear_all():
    confirm = input("Type YES to clear all data: ")
    if confirm == "YES":
        save_data([])
        print("All data cleared.")
    else:
        print("Cancelled.")


def main():
    while True:
        print("\n==== Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Export CSV")
        print("7. Clear All Data")
        print("8. Exit")

        choice = input("Choose: ")

        if choice == "1": add_expense()
        elif choice == "2": view_expenses()
        elif choice == "3": monthly_summary()
        elif choice == "4": update_expense()
        elif choice == "5": delete_expense()
        elif choice == "6": export_csv()
        elif choice == "7": clear_all()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
