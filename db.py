from datetime import datetime

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class DBConnect:
    def __init__(self, db_url):
        """prepare and automap db"""

        Base = automap_base()
        self._engine = create_engine(
            db_url,
            connect_args={"options": "-c timezone=utc"}
        )
        Base.prepare(self._engine, reflect=True)

        self.Record = Base.classes.record
        self.GPS = Base.classes.gps
        self.Item = Base.classes.item

    def __enter__(self):
        self.session = Session(self._engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def get_records(self, uuid):
        records = self.session.query(self.Record).join(self.Item).filter_by(uuid=uuid)
        return records
