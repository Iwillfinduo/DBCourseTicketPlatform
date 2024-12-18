from DAO.main import DAOStatic as DAO



def generate_connections_array(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT):
    connections_array = [None]
    roles = ['manager','dev', 'customer']
    for role in roles:
        conn = DAO.GetDBConnection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
        cursor = conn.cursor()
        cursor.execute(f'SET ROLE {role}')
        conn.commit()
        cursor.close()
        connections_array.append(conn)
    return connections_array
