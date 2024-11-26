import uuid

import bcrypt
from psycopg2 import connect
from psycopg2.extras import RealDictCursor, register_uuid


class DAO:

    @staticmethod
    def GetDBConnection(dbname: str, user: str, passwd: str, host: str, port: str):
        return connect(
            dbname=dbname,
            user=user,
            password=passwd,
            host=host,
            port=port,
            cursor_factory=RealDictCursor,
            options="-c search_path=project"
        )

    @staticmethod
    def GetUserFromDB(connection, got_login: str):
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM users WHERE login = \'{got_login}\'')
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def AddUserToDB(connection, login: str, password: str, name: str, full_name: str, role: int):
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM users WHERE login = \'{login}\'')
        user = cursor.fetchone()
        if user is None:
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print(len(password))
            print(password)
            try:
                cursor.execute(f"insert into Users(Login, name, fullname, passwordhash, role) "
                               f"values ('{login}', '{name}', '{full_name}', '{str(password)}', {role});")
                connection.commit()
            except Exception as e:
                connection.rollback()
                print(e)

    @staticmethod
    def GetAllTickets(connection):
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM tickets')
        tickets = cursor.fetchall()
        cursor.close()
        return tickets

    @staticmethod
    def CreateTicket(connection, ProductID, AuthorLogin):
        cursor = connection.cursor()
        try:
            cursor.execute(f"select create_ticket('{ProductID}','{AuthorLogin}');")
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
            cursor.execute(
                f"insert into Products(ProductID, Name) values (gen_random_uuid(), '{ProductName}');")
            connection.commit()
        except Exception as e:
            connection.rollback()
        cursor.close()

    @staticmethod
    def GetAllProducts(connection):
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM products')
        products = cursor.fetchall()
        cursor.close()
        return products

    @staticmethod
    def SendMessageUnderTicket(connection,author_login,ticket_id, message):
        cursor = connection.cursor()
        try:
            cursor.execute(f"select send_message('{author_login}','{ticket_id}','{message}');")
            connection.commit()
            out = cursor.fetchone()
        except Exception as e:
            out = None
            print(e)
            connection.rollback()
        cursor.close()
        return out

    @staticmethod
    def GetMessagesUnderTicket(connection,ticket_id):
        cursor = connection.cursor()
        cursor.execute(f"select * from messages where ticketid = '{ticket_id}' order by date ;")
        messages = cursor.fetchall()
        cursor.close()
        return messages

    @staticmethod
    def GetProductName(connection, ProductID):
        cursor = connection.cursor()
        cursor.execute(f"select name from Products where ProductID = '{ProductID}';")
        name = cursor.fetchone()['name']
        cursor.close()
        return name

    @staticmethod
    def GetTicketById(connection, ticket_id):
        cursor = connection.cursor()
        cursor.execute(f"select * from tickets where ticketid = '{ticket_id}';")
        ticket = cursor.fetchone()
        cursor.close()
        return ticket

    @staticmethod
    def GetAllUsersByRole(connection, role):
        cursor = connection.cursor()
        cursor.execute(f"select * from users where role = '{role}';")
        users = cursor.fetchall()
        cursor.close()
        return users

    @staticmethod
    def GetAllTicketAssignmentsByRole(connection, ticket_id, role):
        cursor = connection.cursor()
        cursor.execute(f"select * from participants join users on participants.userlogin = users.login where"
                       f" ticketid = '{ticket_id}' and role = {role};")
        output = cursor.fetchall()
        cursor.close()
        return output

    @staticmethod
    def AddAssignmentToTicketAssignments(connection, ticket_id, assignments_logins:list):
        cursor = connection.cursor()
        try:
            for assignment_login in assignments_logins:
                cursor.execute(f"insert into Participants(userlogin, ticketid)"
                               f"values ('{assignment_login}', '{ticket_id}'); ")

            connection.commit()
        except Exception as e:
            connection.rollback()
            print(e)

        cursor.close()

    @staticmethod
    def ChangeTicketStatus(connection, ticket_id, new_status):
        cursor = connection.cursor()
        try:
            cursor.execute(f"update tickets set status = {new_status} where ticketid = '{ticket_id}';")
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()

if __name__ == '__main__':
    conn = DAO.GetDBConnection(dbname='postgres', user='postgres', passwd='postgres', host='localhost', port='5432')
    # DAO.AddUserToDB(conn, 'admin', 'admin', 'HOUSE', 'HOUSE_GREGORY_AZATOVYCH', role=1)
    DAO.CreateProduct(conn, 'Steam')
    # DAO.CreateTicket(conn, DAO.GetAllProducts(conn)[0]['productid'], 'admin')
    #DAO.SendMessageUnderTicket(conn, 'admin', 'b2206e6a-5796-4501-9644-c0220efad069', 'I love you')
    #print(DAO.GetMessagesUnderTicket(conn, 'b2206e6a-5796-4501-9644-c0220efad069'))
    print(DAO.GetUserFromDB(conn, 'admin'))
    print(DAO.GetAllTickets(conn))
    print(DAO.GetAllProducts(conn))
    print(DAO.GetProductName(conn, '33f03031-6767-4aa4-adb4-df4a6f3177b8'))
    #DAO.AddUserToDB(conn, 'dev2', 'dev2', 'VALDOS', 'Глущенко Владислав', role=2)
    print(DAO.GetAllTicketAssignmentsByRole(conn, 'b2206e6a-5796-4501-9644-c0220efad069', 2))