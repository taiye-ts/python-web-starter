from typing import Optional, Generic, List, TypeVar

from project_name.exceptions import NotFoundInRepository
from project_name.storage.database import db
from project_name.storage.database.base import CommonQueryBuilderMixin, CommonSerializerMixin
from project_name.storage.database.sessions import Session


T_ID = TypeVar('T_ID')  # pylint: disable=invalid-name
T = TypeVar('T')  # pylint: disable=invalid-name


class BaseSyncRepository(Generic[T, T_ID], CommonQueryBuilderMixin, CommonSerializerMixin[T, T_ID]):
    used_db = 'main'
    not_found_exception_cls = NotFoundInRepository

    def _get_db_for_query(self, db_name: str) -> Session:
        db_name = self.used_db or db_name
        return getattr(db, db_name)

    def _fetchall(self, query, use_db='', **params):
        with self._get_db_for_query(use_db) as session:
            records = session.execute(query, params).fetchall()
        return records

    def _fetchone(self, query, use_db='', **params):
        with self._get_db_for_query(use_db) as session:
            record = session.execute(query, params).fetchone()
        return record

    def _execute(self, query, use_db='', **params):
        with self._get_db_for_query(use_db) as session:
            return session.execute(query, params)

    def get_by_id(self, instance_id: T_ID, for_update: bool = False) -> Optional[T]:
        if for_update:
            query = self.get_by_id_for_update_query()
        else:
            query = self.get_by_id_query()

        record = self._fetchone(query, **self.instance_id_as_dict(instance_id))
        if not record:
            return None

        return self.get_instance(record)

    def get_or_raise_by_id(self, instance_id: T_ID, for_update: bool = False) -> T:
        instance = self.get_by_id(instance_id, for_update=for_update)

        if not instance:
            raise self.not_found_exception_cls()

        return instance

    def insert(self, instance: T) -> int:
        query = self.insert_query()
        params = self.instance_to_dict(instance)
        result = self._execute(query, **params)
        return result.rowcount

    def update(self, instance: T) -> int:
        params = self.instance_to_dict(instance)
        if 'id' in params:
            params['instance_id'] = params['id']
            # Any other cases should be treated directly because general solution can be very complicated.
        query = self.update_query()
        result = self._execute(query, **params)
        return result.rowcount

    def delete_by_id(self, instance_id: T_ID) -> None:
        self._execute(self.delete_by_id_query(), **self.instance_id_as_dict(instance_id))

    def delete(self, instance: T) -> None:
        id_ = self.get_instance_id(instance)
        self.delete_by_id(id_)

    def delete_all(self):
        return self._execute(self.delete_all_query())

    def get_all(self) -> List[T]:
        return self.get_instances(self._execute(self.get_all_query()))

    def insert_many(self, instances: List[T]) -> None:
        if not instances:
            return
        query = self.insert_query()
        params_list = [self.instance_to_dict(instance) for instance in instances]

        with self._get_db_for_query(self.used_db) as session:
            session.execute(query, params_list)
