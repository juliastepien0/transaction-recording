from flask import Flask, Blueprint, render_template, request, redirect, url_for
#app = Flask(__name__)

app = Blueprint('app', __name__, template_folder='templates')

# example data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
@app.route('/')
def get_transactions():
    return render_template('transactions.html',transactions=transactions)

# Route to handle the creation of a new transaction
@app.route("/add", methods=['GET', 'POST'])
def add_transaction():
    # Check if the request method is POST
    if request.method == 'POST':
        # Assign form field values
        date = request.form['date']
        amount = request.form['amount']
        # Create a new transaction object
        new_transaction = {'id': len(transactions)+1, 'date': date, 'amount': float(amount)}
        # Append the new transaction to the transaction list
        transactions.append(new_transaction)
        # Redirect to the transactions list page
        return redirect(url_for('app.get_transactions'))

    # If the request method is GET, redner the form template
    return render_template('form.html')

# Update
@app.route("/edit/<int:transaction_id>", methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = request.form['amount']

        # Find the matching transaction and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = float(amount)
                break

        # Redirect to the transactions list page
        return redirect(url_for('app.get_transactions'))

    # If request method is GET, find the matching transaction and render edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template('edit.html',transaction=transaction)

# Delete
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find matching transaction
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Remove the transaction
            transactions.remove(transaction)
            break
    # Redirect user to the transactions list page
    return redirect(url_for('app.get_transactions'))

# Search transactions
@app.route("/search", methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        # Assign the values from input field
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        # Filter and append transactions based on the required min and max amounts
        filtered_transactions = []
        for transaction in transactions:
            if transaction['amount'] >= min_amount and transaction['amount'] <= max_amount:
                filtered_transactions.append(transaction)
        # Return only filtered transactions
        return render_template('transactions.html', transactions=filtered_transactions)
    # If request method GET, render search template
    return render_template('search.html')

# Display total amount
@app.route("/balance")
def total_balance():
    balance = 0
    # Sum the amounts from each transaction
    for transaction in transactions:
        balance += transaction['amount']
    # Prepare output string
    string = f"Total balance: {balance}."
    # Return transactions list with balance
    return render_template('transactions.html', transactions=transactions, balance_string=string)

# Run the app
#if __name__ == "__main__":
#    app.run(debug=True)
