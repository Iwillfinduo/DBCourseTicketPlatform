### SETUP FILE FOR DATABASE

import os
from DAO.main import DAOStatic as DAO

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']

if __name__ == '__main__':
    print('tried to set up')
    if os.environ.get('SETUP') is None:
        conn = DAO.GetDBConnection(dbname='postgres', user='postgres', passwd='postgres', host='localhost',
                                         port='5432')
        DAO.AddUserToDB(conn, 'customer', 'customer', 'Lox', 'Lox', role=3)
        DAO.CreateProduct(conn, 'Steam')
        DAO.AddUserToDB(conn, 'admin', 'admin', 'admin', 'addddmin', 1)
        DAO.AddUserToDB(conn, 'dev', 'dev', 'VALDOS', 'Глущенко Владислав', role=2)
        os.environ['SETUP'] = "OK"
        print("Setup Complete")