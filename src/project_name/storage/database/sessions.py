import logging
import traceback
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session as SQLAlchemySession
from project_name.config import DATABASE_URL

logger = logging.getLogger(__name__)


class Session:

    def __init__(self, url) -> None:
        self.url = url

        self.engine = create_engine(self.url)
        session_factory = sessionmaker(bind=self.engine, autoflush=False)

        self._session = scoped_session(session_factory)
        self._session_refs_count = 0

    def __enter__(self) -> SQLAlchemySession:
        self._session_refs_count += 1
        return self._session()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            if self._session_refs_count == 1:
                self._session().commit()
            else:
                self._session().flush()
        else:
            try:
                if self._session_refs_count == 1:
                    self._session().rollback()
            except Exception as e:
                logger.error(str(e))
                logger.error(traceback.format_exc())
            logger.error(traceback.format_tb(exc_tb))
        self._session_refs_count -= 1


class SessionManager:

    def __init__(self) -> None:
        self._main_session = None  # type: Optional[Session]

    @property
    def main(self) -> Session:
        if not self._main_session:
            self._main_session = Session(DATABASE_URL)

        return self._main_session
