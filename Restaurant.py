
import sqlite3
import datetime

con = sqlite3.connect("hotel.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS dish(code INTEGER PRIMARY KEY, name TEXT, price INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS bill(no INTEGER PRIMARY KEY, total INTEGER, date TEXT)")
con.commit()

def today():
    return datetime.date.today().strftime("%d-%m-%Y")

def add_dish():
    code = int(input("Enter dish code: "))
    name = input("Enter name: ")
    price = int(input("Enter price: "))
    cur.execute("INSERT INTO dish VALUES(?,?,?)", (code, name, price))
    con.commit()
    print("Added")

def view_dish():
    cur.execute("SELECT * FROM dish")
    data = cur.fetchall()
    for i in data:
        print(i)

def update_price():
    code = int(input("Enter code: "))
    price = int(input("Enter new price: "))
    cur.execute("UPDATE dish SET price=? WHERE code=?", (price, code))
    con.commit()
    print("Updated")

def create_bill():
    total = 0
    while True:
        code = int(input("Enter code (0 to stop): "))
        if code == 0:
            break

        cur.execute("SELECT * FROM dish WHERE code=?", (code,))
        d = cur.fetchone()

        if d:
            qty = int(input("Enter qty: "))
            amount = d[2] * qty
            total += amount
            print("Added:", amount)
        else:
            print("Not found")

    cur.execute("INSERT INTO bill(total, date) VALUES(?,?)", (total, today()))
    con.commit()
    print("Total =", total)

def today_total():
    cur.execute("SELECT * FROM bill")
    data = cur.fetchall()
    t = today()
    total = 0

    for i in data:
        if i[2] == t:
            total += i[1]

    print("Today total =", total)

def date_total():
    d = input("Enter date: ")
    cur.execute("SELECT * FROM bill")
    data = cur.fetchall()
    total = 0

    for i in data:
        if i[2] == d:
            total += i[1]

    print("Total =", total)

def between_total():
    d1 = input("Start date: ")
    d2 = input("End date: ")

    cur.execute("SELECT * FROM bill")
    data = cur.fetchall()
    total = 0

    for i in data:
        if d1 <= i[2] <= d2:
            total += i[1]

    print("Between total =", total)

while True:
    print("\n1.Create Bill")
    print("2.View Dish")
    print("3.Update Price")
    print("4.Add Dish")
    print("5.Today Total")
    print("6.Date Total")
    print("7.Between Total")
    print("0.Exit")

    ch = input("Enter choice: ")

    if ch == "1":
        create_bill()
    elif ch == "2":
        view_dish()
    elif ch == "3":
        update_price()
    elif ch == "4":
        add_dish()
    elif ch == "5":
        today_total()
    elif ch == "6":
        date_total()
    elif ch == "7":
        between_total()
    elif ch == "0":
        break
    else:
        print("Wrong choice")

con.close()