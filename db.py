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

        self.Movie = Base.classes.movie

    def __enter__(self):
        self.session = Session(self._engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def get_movie(self, uuid):
        movie = self.session.query(self.Movie).filter_by(id=uuid).first()
        return movie
