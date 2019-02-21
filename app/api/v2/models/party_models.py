from .database_connection import Dbase


class Party(Dbase):
    def __init__(self, data=None):
        if data:
            self.party_name = data['party_name']
            self.hqaddress = data['hqaddress']
            self.logoUrl = data['logoUrl']

    def save_party(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO parties(party_name,hqaddress,logoUrl)\
            VALUES (%s, %s, %s)",
                       (self.party_name, self.hqaddress, self.logoUrl))

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
            single_party["hqaddress"] = Party[2]
            single_party['logoUrl'] = Party[3]
            partylist.append(single_party)

        self.conn.close()
        return partylist

    def update__party(self, party_id, party_name):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        # update a party
        cursor.execute(
            """UPDATE parties SET party_name = %s
            WHERE party_id = %s""", (party_name, party_id),
        )
        self.conn.commit()
        self.conn.close()

    def delete__party(self, party_id):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        # delete a party
        try:
            cursor.execute(
                "DELETE FROM parties WHERE party_id = %s",
                (party_id, )
            )
        except Exception as exception:
            print(exception)
        self.conn.commit()
        self.conn.close()
