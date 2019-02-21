from . import database_connection


tables = [
    """
    CREATE TABLE IF NOT EXISTS users(
    user_id serial PRIMARY KEY,username varchar(30) not null UNIQUE,voter_id varchar(10) not null UNIQUE, 
    email varchar(50) not null UNIQUE, password varchar(250) not null,
    isadmin boolean not null)
    """,
    """
    CREATE TABLE IF NOT EXISTS parties(
    party_id serial PRIMARY KEY,party_name varchar(30) not null,
    hqaddress varchar(30) not null, logoUrl varchar(250) not null)
    """,
    """
    CREATE TABLE IF NOT EXISTS offices(
    office_id serial PRIMARY KEY,office_name varchar(30) not null,
    office_type varchar(30) not null)
    """,
    """
    CREATE TABLE IF NOT EXISTS candidates(
        candidate_id serial PRIMARY KEY,office_id int REFERENCES offices(office_id)not null,
        user_id int REFERENCES users(user_id) not null
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS votes(
    vote_id serial PRIMARY KEY,voter_id varchar REFERENCES users(voter_id) not null, candidate_id int REFERENCES candidates(candidate_id)not null,
    office_id int REFERENCES offices(office_id) not null
    )
    """,
]

drop_tables = [
    "DROP TABLE IF EXISTS users CASCADE",
    "DROP TABLE IF EXISTS parties CASCADE",
    "DROP TABLE IF EXISTS offices CASCADE",
    "DROP TABLE IF EXISTS candidates CASCADE",
    "DROP TABLE IF EXISTS votes CASCADE"
]


def select(table):
    db_obj = database_connection.Dbase()
    conn = db_obj.connection_to_Dbase()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {}".format(table))
    result = cursor.fetchall()
    conn.close()
    return result
