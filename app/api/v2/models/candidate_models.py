from .database_connection import Dbase


class Candidate(Dbase):
    def __init__(self, data=None):
        if data:
            self.user_id = data['user_id']
            self.office_id = data['office_id']
            db_obj = Dbase()
            self.conn = db_obj.connection_to_Dbase()

    def save(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO candidates(office_id,user_id)\
            VALUES (%s, %s)",
                       (self.office_id, self.user_id))

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
