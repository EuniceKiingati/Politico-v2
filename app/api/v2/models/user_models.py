from .database_connection import Dbase
from werkzeug.security import generate_password_hash


class User(Dbase):
    def __init__(self, data=None):
        if data:
            self.username = data['username'].strip()
            self.voter_id = data['voter_id'].strip()
            self.password = generate_password_hash(data['password'].strip())
            self.email = data['email'].strip()
            self.isadmin = data['isadmin']
            db_obj = Dbase()
            self.conn = db_obj.connection_to_Dbase()

    def save(self):

        try:
            db_obj = Dbase()
            self.conn = db_obj.connection_to_Dbase()
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users(username,voter_id,email,password,isadmin)\
            VALUES (%s, %s, %s, %s, %s)",
                           (self.username, self.voter_id, self.email, self.password, self.isadmin))

            # cursor.execute(query)
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e, "could not save")

    def get_all_User(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()  # create connection to db
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
