### SETUP FILE FOR DATABASE

import os
from DAO.main import DAOStatic as DAO
import logging
logger = logging.getLogger(__name__)
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']

def setup():
    logger.info('tried to set up')
    conn = DAO.GetDBConnection(dbname=DB_NAME, user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST,
                               port=DB_PORT)
    DAO.AddUserToDB(conn, 'customer', 'customer', 'Lox', 'Lox', role=3)
    DAO.CreateProduct(conn, 'Steam')
    DAO.AddUserToDB(conn, 'admin', 'admin', 'admin', 'addddmin', 1)
    DAO.AddUserToDB(conn, 'dev', 'dev', 'VALDOS', 'Глущенко Владислав', role=2)
    logger.info("Setup Complete")

