import psycopg2
import os


class Dbase():
    def __init__(self):
        self.db_name = 'politico'
        self.db_host = 'localhost'
        self.db_user ='postgres'
        self.db_password ='Yunis1500'
        self.conn = None

    def connection_to_Dbase(self):
        # get from app settings:development
            try:
                self.conn= psycopg2.connect(
                    database= self.db_name,
                    host=self.db_host,
                    user=self.db_user,
                    password=self.db_password
                )
                print("connection successful")
            except Exception as e:
                print( e, "can't connect to database")

            return self.conn
    
    def create_tables(self):
        tables= [
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
    
            
            
        
        try:
            cursor= self.connection_to_Dbase().cursor()
            for table in tables:
                cursor.execute(table)
        except Exception as e:
            print(e, "cannot execute")
        self.conn.commit()
        self.conn.close()
    def destroy_tables(self):
        cursor = self.connection_to_Dbase().cursor()

        sql = [
            "DROP TABLE IF EXISTS users CASCADE",
            "DROP TABLE IF EXISTS parties CASCADE",
            "DROP TABLE IF EXISTS offices CASCADE",
            "DROP TABLE IF EXISTS candidates CASCADE",
            "DROP TABLE IF EXISTS votes CASCADE"
        ]
        for query in sql:
            cursor.execute(query)
        self.conn.commit()
        self.conn.close()
    
        
class User(Dbase):
    def __init__(self, data=None):
        if data:
            self.username= data['username'].strip()
            self.voter_id=data['voter_id'].strip()
            self.password=data['password'].strip()
            self.email=data['email'].strip()
            self.isadmin=data['isadmin']
            db_obj=Dbase()
            self.conn=db_obj.connection_to_Dbase()


    def save(self):
        
        try:
            db_obj=Dbase()
            self.conn=db_obj.connection_to_Dbase()
            cursor=self.conn.cursor()
            cursor.execute("INSERT INTO users(username,voter_id,email,password,isadmin)\
            VALUES (%s, %s, %s, %s, %s)",
            (self.username,self.voter_id,self.email,self.password,self.isadmin))

            # cursor.execute(query)
            self.conn.commit()
            self.conn.close()
            print("user signed up successfully")
        except Exception as e:
            print( e, "could not save")
    
    def get_all_User(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()#create connection to db
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Users")
        result = cursor.fetchall()
        Userlist = []
        for user in result:
            
            single_user = {}
            single_user['user_id'] = user[0]
            single_user["username"] = user[1]
            single_user["voter_id"] = user[2]
            single_user["email"] = user[3]
            single_user["password"] = user[4]
            single_user['isadmin'] = user[5]
            Userlist.append(single_user)

        self.conn.close()
        return Userlist

class Party(Dbase):
    def __init__(self, data=None):
        if data:
            self.party_name= data['party_name']
            self.hqaddress= data['hqaddress']
            self.logoUrl= data['logoUrl']
            
    
    def save_party(self):
        db_obj=Dbase()
        self.conn=db_obj.connection_to_Dbase()
        cursor=self.conn.cursor()
        cursor.execute("INSERT INTO parties(party_name,hqaddress,logoUrl)\
            VALUES (%s, %s, %s)",
            (self.party_name,self.hqaddress,self.logoUrl))
            
        self.conn.commit()
        self.conn.close()

    def get_all_parties(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM parties")
        result = cursor.fetchall()
        partylist = []

        for Party in result:
            single_party = {}
            single_party['party_id'] = Party[0]
            single_party["party_name"] = Party[1]
            single_party["hqaddress"]=Party[2]
            single_party['logoUrl'] = Party[3]
            partylist.append(single_party)

        self.conn.close()
        return partylist 

class Office(Dbase):
    def __init__(self, data=None):
        if data:
            self.office_name= data['office_name']
            self.office_type= data['office_type']

    def save_office(self):
        db_obj=Dbase()
        self.conn=db_obj.connection_to_Dbase()
        cursor=self.conn.cursor()
        cursor.execute("INSERT INTO offices(office_name,office_type)\
            VALUES (%s, %s)",
            (self.office_name,self.office_type))
            
        self.conn.commit()
        self.conn.close()        
       
      
    def get_all_offices(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM offices")
        result = cursor.fetchall()
        officelist = []

        for office in result:
            single_office = {}
            single_office['office_id'] = office[0]
            single_office["office_name"] = office[1]
            single_office["office_type"]=office[2]
            officelist.append(single_office)

        self.conn.close()
        return officelist  

class Candidate(Dbase):
    def __init__(self, data=None):
        if data:
            self.user_id= data['user_id']
            self.office_id=data['office_id']
            db_obj=Dbase()
            self.conn=db_obj.connection_to_Dbase()


    def save(self):
        db_obj=Dbase()
        self.conn=db_obj.connection_to_Dbase()
        cursor=self.conn.cursor()
        cursor.execute("INSERT INTO candidates(office_id,user_id)\
            VALUES (%s, %s)",
            (self.office_id,self.user_id))
            
        self.conn.commit()
        self.conn.close() 
            
    def get_all_candidates(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("SELECT candidates.candidate_id,users.user_id,users.username,offices.office_id,offices.office_name\
        FROM users JOIN candidates ON users.user_id=candidates.user_id JOIN offices ON\
        offices.office_id=candidates.office_id")
    
        result = cursor.fetchall()
        candidatelist = []

        for candidate in result:
            single_candidate = {}
            single_candidate['candidate_id'] = candidate[0]
            single_candidate['user_id'] = candidate[1]
            single_candidate['username'] = candidate[2]
            single_candidate['office_id'] = candidate[3]
            single_candidate['office_name'] = candidate[4]
            candidatelist.append(single_candidate)

        self.conn.close()
        return candidatelist 

class Vote(Dbase):
    def __init__(self, data=None):
        if data:
            self.voter_id= data['voter_id']
            print(self.voter_id, "\n\n\n")
            self.candidate_id=data['candidate_id']
            self.office_id=data['office_id']
            db_obj=Dbase()
            self.conn=db_obj.connection_to_Dbase()
    
    def save_vote(self):
        db_obj=Dbase()
        self.conn=db_obj.connection_to_Dbase()
        cursor=self.conn.cursor()
        cursor.execute("INSERT INTO votes(voter_id,candidate_id,office_id)\
            VALUES (%s, %s,%s)",
            (self.voter_id,self.candidate_id,self.office_id,))
            
        self.conn.commit()
        self.conn.close() 
    
    def get_all_votes(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("SELECT votes.vote_id,users.voter_id,users.username,offices.office_id,offices.office_name,candidate.candidate_id,candidate.candidate_name,\
        FROM users JOIN votes ON users.voter_id=votes.voter_id JOIN candidates ON\
        candidates.candidate_id=votes.candidate_id JOIN offices ON offices.office_id=votes.office_id")
    
        result = cursor.fetchall()
        voteslist = []

        for vote in result:
            single_vote = {}
            single_vote['vote_id'] = vote[0]
            single_vote['voter_id'] = vote[1]
            single_vote['username'] = vote[2]
            single_vote['office_id'] = vote[3]
            single_vote['office_name'] = vote[4]
            single_vote['candidate_id'] = vote[5]
            single_vote['candidate_name'] = vote[6]
            voteslist.append(single_vote)

        self.conn.close()
        return voteslist 