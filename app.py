from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
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
        return redirect(url_for('get_transactions'))

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
        return redirect(url_for('get_transactions'))

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
    return redirect(url_for('get_transactions'))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
