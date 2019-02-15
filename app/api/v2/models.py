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
        if os.getenv("APP_SETTINGS") == "development":
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
        self.conn = psycopg2.connect(
                os.environ['DATABASE_URL'], sslmode='require')
        return self.conn
    
    def create_tables(self):
        tables= [
            """
            CREATE TABLE IF NOT EXISTS users(
            user_id serial PRIMARY KEY, username varchar(30) not null,
            email varchar(50) not null, password varchar(250) not null,
            role varchar(10) not null)
            """,
            """
            CREATE TABLE IF NOT EXISTS parties(
            party_id serial PRIMARY KEY,party_name varchar(30) not null,
            hqaddress varchar(30) not null, logoUrl varchar(250) not null)
            """
    
            
            
        ]
        try:
            cursor= self.connection_to_Dbase().cursor()
            for table in tables:
                cursor.execute(table)
        except Exception as e:
            print(e, "cannot execute")
        self.conn.commit()
        self.conn.close()
        
        
class User(Dbase):
    def __init__(self, data=None):
        if data:
            self.username= data['username'].strip()
            self.password=data['password'].strip()
            self.email=data['email'].strip()
            self.role=data['role'].strip()
            db_obj=Dbase()
            self.conn=db_obj.connection_to_Dbase()


    def save(self):
        print(self.username, self.email, self.password)
        try:
            db_obj=Dbase()
            self.conn=db_obj.connection_to_Dbase()
            cursor=self.conn.cursor()
            cursor.execute("INSERT INTO users(username,email,password,role)\
            VALUES (%s, %s, %s, %s)",
            (self.username,self.email,self.password,self.role))

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
            single_user["email"] = user[2]
            single_user["password"] = user[3]
            single_user['role'] = user[4]
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
        Parties = []

        for Party in result:
            single_party = {}
            single_party['party_id'] = Party[0]
            single_party["party_name"] = Party[1]
            single_party["hqaddress"]=Party[2]
            single_party['logoUrl'] = Party[3]
            Parties.append(single_party)

        self.conn.close()
        return Parties        
       
      
     