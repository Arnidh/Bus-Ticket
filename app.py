from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Create a basic SQLite database for storing tickets
def init_db():
    with sqlite3.connect('bus_tickets.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tickets
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         passenger_name TEXT, 
                         destination TEXT, 
                         departure_time TEXT)''')

@app.route('/')
def home():
    # Fetch all tickets from the database
    with sqlite3.connect('bus_tickets.db') as conn:
        tickets = conn.execute('SELECT * FROM tickets').fetchall()
    return render_template('bus.html', tickets=tickets)

@app.route('/reserve', methods=['POST'])
def reserve_ticket():
    passenger_name = request.form['passenger_name']
    destination = request.form['destination']
    departure_time = request.form['departure_time']
    with sqlite3.connect('bus_tickets.db') as conn:
        conn.execute('INSERT INTO tickets (passenger_name, destination, departure_time) VALUES (?, ?, ?)', (passenger_name, destination, departure_time))
    return 'Ticket reserved successfully!'

@app.route('/update', methods=['POST'])
def update_ticket():
    ticket_id = int(request.form['id'])
    passenger_name = request.form['passenger_name']
    destination = request.form['destination']
    departure_time = request.form['departure_time']
    with sqlite3.connect('bus_tickets.db') as conn:
        conn.execute('UPDATE tickets SET passenger_name = ?, destination = ?, departure_time = ? WHERE id = ?', (passenger_name, destination, departure_time, ticket_id))
    return 'Ticket updated successfully!'

@app.route('/cancel', methods=['POST'])
def cancel_ticket():
    ticket_id = int(request.form['id'])
    with sqlite3.connect('bus_tickets.db') as conn:
        conn.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    return 'Ticket canceled successfully!'

@app.route('/search', methods=['GET'])
def search_tickets():
    search_query = request.args.get('query', '')
    try:
        search_query = int(search_query)  # Try converting query to an integer (ticket ID)
        with sqlite3.connect('bus_tickets.db') as conn:
            result = conn.execute('SELECT * FROM tickets WHERE id = ?', (search_query,)).fetchone()
        if result:
            # Ticket found, render template with ticket details
            return render_template('bus.html', tickets=[result])
        else:
            # Ticket not found, render template with message
            return render_template('bus.html', not_found=True)
    except ValueError:
        # Invalid input (not a valid integer), render template with message
        return render_template('bus.html', not_found=True)



if __name__ == '__main__':
    init_db()
    app.run(port=5011) 
