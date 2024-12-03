from DAO.main import DAOStatic as DAO


class FormsGenerator():

    @staticmethod
    def GenerateTicketInfo(conn,ticket):
        messages = DAO.GetMessagesUnderTicket(conn, ticket['ticketid'])
        date = messages[0]['date']
        user = DAO.GetUserFromDB(conn, ticket['authorlogin'])
        product_name = DAO.GetProductName(conn, ticket['productid'])
        assignees = DAO.GetAllTicketAssignmentsByRole(conn, ticket['ticketid'], 2)
        name = 'None'
        try:
            for message in messages:
                if message['message'].startswith('!'):
                    name = message['message'][1:]
                    break
        except Exception as e:
            print(e)
        element = dict()
        element['ticket_id'] = ticket['ticketid']
        element['name'] = name
        element['product_name'] = product_name
        element['creation_date'] = date
        element['author'] = user['name']
        element['assignees'] = [assignee['login'] for assignee in assignees]
        if int(ticket['status']) == 1:
            element['status'] = "Open"
        elif int(ticket['status']) == 2:
            element['status'] = "In Progress"
        elif int(ticket['status']) == 3:
            element['status'] = "Closed"
        return element