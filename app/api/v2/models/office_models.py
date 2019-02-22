from .database_connection import Dbase
from .sql import select


class Office(Dbase):
    def __init__(self, data=None):
        if data:
            self.office_name = data['office_name']
            self.office_type = data['office_type']

    def save_office(self):
        db_obj = Dbase()
        self.conn = db_obj.connection_to_Dbase()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO offices(office_name,office_type)\
            VALUES (%s, %s)",
                       (self.office_name, self.office_type))

        self.conn.commit()
        self.conn.close()

    def get_all_offices(self):

        result = select("offices")
        officelist = []

        for office in result:
            single_office = {}
            single_office['office_id'] = office[0]
            single_office["office_name"] = office[1]
            single_office["office_type"] = office[2]
            officelist.append(single_office)

        return officelist
