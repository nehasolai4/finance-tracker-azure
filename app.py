from flask import Flask, render_template, request, redirect
from db import get_connection
from blob import upload_file
from flask import flash

app = Flask(__name__)


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET","POST"])
def login():

    try:

        if request.method=="POST":

            username=request.form["username"]
            password=request.form["password"]

            conn=get_connection()
            cursor=conn.cursor()

            cursor.execute(
                "SELECT * FROM Users WHERE username=? AND password=?",
                (username,password)
            )

            user=cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                return redirect("/dashboard")
            else:
                return "Invalid Credentials"

        return render_template("login.html")
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return str(e), 500


@app.route("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM Expenses")
    expense = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM Investments")
    investment = cursor.fetchone()[0] or 0

    cursor.execute("SELECT monthly_budget FROM Budget")

    budget = cursor.fetchone()

    if budget:
        budget = budget[0]
    else:
        budget = 0

    remaining = budget - expense

    cursor.execute("""
        SELECT title, category, amount, expense_date
        FROM Expenses
        ORDER BY expense_date DESC
    """)

    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        expense=expense,
        investment=investment,
        budget=budget,
        remaining=remaining,
        expenses=expenses
    )


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Expenses(user_id,title,category,amount,expense_date)
            VALUES(?,?,?,?,?)
        """, (1, title, category, amount, date))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_expense.html")



@app.route("/set-budget", methods=["GET", "POST"])
def set_budget():

    if request.method == "POST":

        budget = request.form["budget"]

        conn = get_connection()
        cursor = conn.cursor()

        # Remove old budget
        cursor.execute("DELETE FROM Budget WHERE user_id = ?", (1,))

        # Insert new budget
        cursor.execute(
            "INSERT INTO Budget(user_id, monthly_budget) VALUES(?, ?)",
            (1, budget)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/dashboard")

    return render_template("budget.html")


@app.route("/add-investment", methods=["GET", "POST"])
def add_investment():

    if request.method == "POST":

        name = request.form["name"]
        amount = request.form["amount"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Investments(user_id, investment_name, amount)
            VALUES (?, ?, ?)
        """, (1, name, amount))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/dashboard")

    return render_template("investment.html")

@app.route("/upload", methods=["GET","POST"])
def upload():

    if request.method=="POST":

        file=request.files["receipt"]

        if file:

            upload_file(file)

            return redirect("/dashboard")

    return render_template("upload.html")


if __name__=="__main__":
    app.run(debug=True)