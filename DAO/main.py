import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
import bcrypt


class DAOStatic:

    @staticmethod
    def GetDBConnection(dbname: str, user: str, passwd: str, host: str, port: str):
        return psycopg2.connect(
            dbname=dbname,
            user=user,
            password=passwd,
            host=host,
            port=port,
            cursor_factory=RealDictCursor,
            options="-c search_path=project"
        )

    @staticmethod
    def GetUserFromDB(connection, got_login: str, cursor=None):
        is_cursor = True
        if cursor is None:
            is_cursor = False
            cursor = connection.cursor()

        query = sql.SQL("SELECT * FROM users WHERE login = {login}").format(
            login=sql.Literal(got_login)
        )
        cursor.execute(query)
        user = cursor.fetchone()
        if not is_cursor:
            cursor.close()
        return user

    @staticmethod
    def AddUserToDB(connection, login: str, password: str, name: str, full_name: str, role: int, cursor=None):
        is_cursor = True
        if cursor is None:
            is_cursor = False
            cursor = connection.cursor()

        query = sql.SQL("SELECT * FROM users WHERE login = {login}").format(
            login=sql.Literal(login)
        )
        cursor.execute(query)
        user = cursor.fetchone()

        if user is None:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            try:
                insert_query = sql.SQL("""
                    INSERT INTO Users(Login, name, fullname, passwordhash, role)
                    VALUES ({login}, {name}, {fullname}, {passwordhash}, {role})
                """).format(
                    login=sql.Literal(login),
                    name=sql.Literal(name),
                    fullname=sql.Literal(full_name),
                    passwordhash=sql.Literal(password_hash),
                    role=sql.Literal(str(role))  # Role should be converted to string for SQL
                )
                cursor.execute(insert_query)
                connection.commit()
            except Exception as e:
                connection.rollback()
                print(e)

        cursor.close()

    @staticmethod
    def GetAllTickets(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tickets")
        tickets = cursor.fetchall()
        cursor.close()
        return tickets

    @staticmethod
    def GetTicketByAuthor(connection, author_login):
        cursor = connection.cursor()
        cursor.callproc('get_info_about_your_tickets', [author_login])
        tickets = cursor.fetchall()
        connection.commit()
        cursor.close()
        return tickets

    @staticmethod
    def CreateTicket(connection, ProductID, AuthorLogin):
        cursor = connection.cursor()
        try:
            query = sql.SQL("SELECT create_ticket({ProductID}, {AuthorLogin})").format(
                ProductID=sql.Literal(ProductID),
                AuthorLogin=sql.Literal(AuthorLogin)
            )
            cursor.execute(query)
            result = cursor.fetchone()
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
            result = None
        cursor.close()
        return result

    @staticmethod
    def CreateProduct(connection, ProductName):
        cursor = connection.cursor()
        try:
            insert_query = sql.SQL("""
                INSERT INTO Products(ProductID, Name) 
                VALUES (gen_random_uuid(), {ProductName})
            """).format(
                ProductName=sql.Literal(ProductName)
            )
            cursor.execute(insert_query)
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()

    @staticmethod
    def GetAllProducts(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        return products

    @staticmethod
    def SendMessageUnderTicket(connection, author_login, ticket_id, message):
        cursor = connection.cursor()
        try:
            query = sql.SQL("SELECT send_message({author_login}, {ticket_id}, {message})").format(
                author_login=sql.Literal(author_login),
                ticket_id=sql.Literal(ticket_id),
                message=sql.Literal(message)
            )
            cursor.execute(query)
            connection.commit()
            out = cursor.fetchone()
        except Exception as e:
            out = None
            print(e)
            connection.rollback()
        cursor.close()
        return out

    @staticmethod
    def GetMessagesUnderTicket(connection, ticket_id):
        cursor = connection.cursor()
        query = sql.SQL("SELECT * FROM messages WHERE ticketid = {ticket_id} ORDER BY date").format(
            ticket_id=sql.Literal(ticket_id)
        )
        cursor.execute(query)
        messages = cursor.fetchall()
        cursor.close()
        return messages

    @staticmethod
    def GetProductName(connection, ProductID):
        cursor = connection.cursor()
        query = sql.SQL("SELECT name FROM Products WHERE ProductID = {ProductID}").format(
            ProductID=sql.Literal(ProductID)
        )
        cursor.execute(query)
        name = cursor.fetchone()['name']
        cursor.close()
        return name

    @staticmethod
    def GetTicketById(connection, ticket_id):
        cursor = connection.cursor()
        query = sql.SQL("SELECT * FROM tickets WHERE ticketid = {ticket_id}").format(
            ticket_id=sql.Literal(ticket_id)
        )
        cursor.execute(query)
        ticket = cursor.fetchone()
        cursor.close()
        return ticket

    @staticmethod
    def GetAllUsersByRole(connection, role):
        cursor = connection.cursor()
        query = sql.SQL("SELECT * FROM users WHERE role = {role}").format(
            role=sql.Literal(role)
        )
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users

    @staticmethod
    def GetAllTicketAssignmentsByRole(connection, ticket_id, role):
        cursor = connection.cursor()
        query = sql.SQL("""
            SELECT * FROM participants
            JOIN users ON participants.userlogin = users.login
            WHERE ticketid = {ticket_id} AND role = {role}
        """).format(
            ticket_id=sql.Literal(ticket_id),
            role=sql.Literal(role)
        )
        cursor.execute(query)
        output = cursor.fetchall()
        cursor.close()
        return output

    @staticmethod
    def AddAssignmentToTicketAssignments(connection, ticket_id, assignments_logins):
        cursor = connection.cursor()
        try:
            for assignment_login in assignments_logins:
                query = sql.SQL("""
                    INSERT INTO Participants(userlogin, ticketid)
                    VALUES ({assignment_login}, {ticket_id})
                """).format(
                    assignment_login=sql.Literal(assignment_login),
                    ticket_id=sql.Literal(ticket_id)
                )
                cursor.execute(query)
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()

    @staticmethod
    def ChangeTicketStatus(connection, ticket_id, new_status):
        cursor = connection.cursor()
        try:
            query = sql.SQL("""
                UPDATE tickets SET status = {new_status} WHERE ticketid = {ticket_id}
            """).format(
                new_status=sql.Literal(new_status),
                ticket_id=sql.Literal(ticket_id)
            )
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()

    @staticmethod
    def DeleteTicketAssignments(connection, ticket_id):
        cursor = connection.cursor()
        try:
            query = sql.SQL("""
                DELETE FROM participants WHERE ticketid = {ticket_id}
                AND userlogin IN (SELECT userlogin FROM users WHERE role = 2)
            """).format(
                ticket_id=sql.Literal(ticket_id)
            )
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()


if __name__ == '__main__':
    conn = DAOStatic.GetDBConnection(dbname='postgres', user='postgres', passwd='postgres', host='localhost', port='5432')
    DAOStatic.AddUserToDB(conn, 'customer', 'customer', 'Lox', 'Lox', role=3)
    DAOStatic.CreateProduct(conn, 'Steam')
    DAOStatic.AddUserToDB(conn, 'admin', 'admin', 'admin', 'addddmin', 1)
    # DAO.CreateTicket(conn, DAO.GetAllProducts(conn)[0]['productid'], 'admin')
    #DAO.SendMessageUnderTicket(conn, 'admin', 'b2206e6a-5796-4501-9644-c0220efad069', 'I love you')
    #print(DAO.GetMessagesUnderTicket(conn, 'b2206e6a-5796-4501-9644-c0220efad069'))
    print(DAOStatic.GetUserFromDB(conn, 'customer'))
    # print(DAO.GetAllTickets(conn))
    # print(DAO.GetAllProducts(conn))
    # print(DAO.GetProductName(conn, '33f03031-6767-4aa4-adb4-df4a6f3177b8'))
    DAOStatic.AddUserToDB(conn, 'dev2', 'dev2', 'VALDOS', 'Глущенко Владислав', role=2)
    print(DAOStatic.GetAllTicketAssignmentsByRole(conn, 'b2206e6a-5796-4501-9644-c0220efad069', 2))
    DAOStatic.DeleteTicketAssignments(conn, ticket_id='b2206e6a-5796-4501-9644-c0220efad069')
    print(DAOStatic.GetAllTicketAssignmentsByRole(conn, 'b2206e6a-5796-4501-9644-c0220efad069', 2))
    DAOStatic.AddUserToDB(conn, 'customer', 'customer', 'Anton', 'Антоша Бордвайн', role=3)