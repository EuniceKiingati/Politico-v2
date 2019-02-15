from app.api.v2.views import create_app
from app.api.v2.models import Dbase

dtb_obj = Dbase()
dtb_obj.create_tables()

app= create_app()

if __name__=="__main__":
    app.run(debug=True)