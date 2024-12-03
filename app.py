import bcrypt
from flask import Flask, request, flash, redirect, url_for, jsonify
from flask import render_template, session
import os

from DAO.main import DAO
from DAO.utils import FormsGenerator

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
SECRET_KEY = os.environ['SECRET_KEY']

conn = DAO.GetDBConnection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
@app.route('/')
def root():
    if session.get('username'):
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        user = DAO.GetUserFromDB(conn, username)
        print(user)
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['passwordhash'].encode('utf-8')):
                session['username'] = username
                session['role'] = int(user['role'])
                return redirect(url_for('homepage'))
            else:
                flash('Invalid username or password')
        else:
            flash('User not found')

    except Exception as e:
        flash(f"Database error: {e}")

    return redirect(url_for("root"))

@app.route('/homepage')
def homepage():
    if 'username' in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for('root'))

@app.route('/api/tickets', methods=['GET'])
def tickets_table():
    if 'username' in session:
        output = []
        if session['role'] == 1:
            tickets = DAO.GetAllTickets(conn)

            for ticket in tickets:
                element = FormsGenerator.GenerateTicketInfo(conn, ticket)
                output.append(element)
        return jsonify(output)

@app.route("/create-ticket")
def create_ticket():
    if 'username' in session:
        return render_template("create-ticket.html")

@app.route("/api/create-ticket", methods=['POST', 'GET'])
def api_create_ticket():
    if 'username' in session:
        if request.method == 'POST':
            data = request.json
            ticket_name = data.get("name")
            product_id = data.get("product_id")
            description = data.get("description")

            if not ticket_name or not product_id or not description:
                return jsonify({"error": "All fields are required"}), 400

            # Generate a new ticket ID
            new_ticket_id = DAO.CreateTicket(conn, product_id, session["username"])['create_ticket']
            DAO.SendMessageUnderTicket(conn, session["username"], new_ticket_id, "!" + ticket_name)
            DAO.SendMessageUnderTicket(conn, session["username"], new_ticket_id, description)
            return jsonify({"success": True, "ticket_id": new_ticket_id})

@app.route("/api/products", methods=['GET'])
def products_table():
    if 'username' in session:
        products = DAO.GetAllProducts(conn)
        return jsonify(products)



@app.route('/ticket/<ticket_id>')
def ticket_info(ticket_id):
    if 'username' in session:
        ticket_id = str(ticket_id)
        print(ticket_id)
        ticket = DAO.GetTicketById(conn, ticket_id)
        print(ticket)
        if ticket:
            element = FormsGenerator.GenerateTicketInfo(conn, ticket)
            return render_template("ticket_info.html", ticket=element, ticket_id=ticket_id, username=session['username'])

@app.route("/chat/<ticket_id>/", methods=['POST','GET'])
def chat_api(ticket_id):
    if 'username' in session:
        if request.method == "GET":
            messages = DAO.GetMessagesUnderTicket(conn, ticket_id)
            for message in messages:
                message['date'] = str(message['date'].isoformat())
            return jsonify(messages)
        if request.method == "POST":
            data = request.json
            print(data)
            user = data['user']
            message = data['message']
            DAO.SendMessageUnderTicket(conn, user, ticket_id , message)
            return '200'


@app.route('/api/<ticket_id>/assignees', methods=['POST'])
def update_ticket_assignees(ticket_id):
    print('try_to_update')
    if 'username' in session and session['role'] == 1:
        ticket = DAO.GetTicketById(conn, ticket_id)
        who_made_assignment = session['username']
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404
        DAO.DeleteTicketAssignments(conn, ticket_id)
        assignees = DAO.GetAllUsersByRole(conn, 2)
        assignees_logins = [assignee.get('login') for assignee in assignees]
        print(assignees)
        data = request.json
        new_assignees = data.get("assignees", [])
        print(new_assignees)
        print(assignees_logins)
        if new_assignees == []:
            return jsonify({"error": "Got zero logins"}), 400
        DAO.AddAssignmentToTicketAssignments(conn, ticket_id, new_assignees)
        return jsonify({"success": True, "assignees": new_assignees})
    else:
        return '404'

@app.route('/api/<ticket_id>/status', methods=['POST'])
def update_ticket_status(ticket_id):
    if 'username' in session and (session['role'] == 1 or session['role'] == 2):
        ticket = DAO.GetTicketById(conn, ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404
        data = request.json
        print(data)
        new_status = data['status']
        valid_statuses = ["Open", "In Progress", "Closed"]
        if new_status not in valid_statuses:
            return jsonify({"error": "Invalid status"}), 400
        new_status_index = valid_statuses.index(new_status) + 1
        print(new_status_index)
        DAO.ChangeTicketStatus(conn, ticket_id, new_status_index)
        return jsonify({"success": True, "status": new_status})




@app.route('/api/all_assignees', methods=['GET'])
def get_assignees():
    assignees = DAO.GetAllUsersByRole(conn, 2)
    print(assignees)
    return jsonify(assignees)

@app.route('/api/<ticket_id>/assignees', methods=['GET'])
def get_assignees_under_ticket(ticket_id):
    assignees = DAO.GetAllTicketAssignmentsByRole(conn, ticket_id, 2)
    print(assignees)
    print(jsonify({'assignees': assignees}).json)
    return jsonify({'assignees': assignees})




if __name__ == '__main__':

    app.run(port=5002)
