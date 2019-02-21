from .database_connection import Dbase

class Vote(Dbase):
    def __init__(self, data=None):
        if data:
            self.voter_id = data['voter_id']
            print(self.voter_id, "\n\n\n")
            self.candidate_id = data['candidate_id']
            self.office_id = data['office_id']
            db_obj = Dbase()
            self.conn = db_obj.connection_to_Dbase()

    def save_vote(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO votes(voter_id,candidate_id,office_id)\
            VALUES (%s, %s,%s)",
                       (self.voter_id, self.candidate_id, self.office_id,))

        self.conn.commit()
        self.conn.close()

    def get_all_votes(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("SELECT offices.office_id,candidates.candidate_id\
        FROM offices JOIN candidates ON offices.office_id=candidates.office_id")

        result = cursor.fetchall()
        voteslist = []

        for vote in result:
            single_vote = {}
            single_vote['office_id'] = vote[0]
            single_vote['candidate_id'] = vote[1]
            voteslist.append(single_vote)

        self.conn.close()
        return voteslist
