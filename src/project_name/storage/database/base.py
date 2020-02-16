import pickle
from typing import TypeVar, Optional, Generic, List, Dict, Callable, Any, Union

from sqlalchemy import Table
from sqlalchemy.engine import RowProxy
from sqlalchemy.sql.expression import select, Select, delete, Delete, bindparam, insert, Insert, Update, update

T_ID = TypeVar('T_ID')  # pylint: disable=invalid-name
T = TypeVar('T')  # pylint: disable=invalid-name

FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)  # pylint: disable=invalid-name


class CommonQueryBuilderMixin:
    @property
    def table(self) -> Table:
        raise NotImplementedError()

    @property
    def id_query(self):
        return self.table.c.id == bindparam('instance_id')

    def get_by_id_query(self) -> Select:
        return self.get_all_query().where(self.id_query)

    def get_by_id_for_update_query(self) -> Select:
        return self.get_all_query().with_for_update().where(self.id_query)

    def delete_by_id_query(self) -> Delete:
        return delete(self.table).where(self.id_query)

    def get_all_query(self) -> Select:
        return select([self.table])

    def insert_query(self) -> Insert:
        return insert(self.table)

    def update_query(self) -> Update:
        return update(self.table).where(self.id_query)

    def delete_all_query(self) -> Delete:
        return delete(self.table)


class CommonSerializerMixin(Generic[T, T_ID]):

    def get_instance_id(self, instance: T) -> T_ID:
        raise NotImplementedError()

    def get_instances(self, records: List[RowProxy]) -> List[T]:
        return list(map(self.get_instance, records))

    def get_instance(self, record: RowProxy) -> T:
        raise NotImplementedError()

    def instance_to_dict(self, instance: T) -> Dict:
        serializer = getattr(instance, 'to_dict', None)
        if callable(serializer):
            return serializer()
        raise NotImplementedError()

    def _deserialize(self, result: Optional[bytes]) -> Optional[Union[List[T], T]]:
        if isinstance(result, bytes):
            return pickle.loads(result)
        return None

    def _serialize(self, instance: T) -> bytes:
        return pickle.dumps(instance, protocol=4)

    def instance_id_as_dict(self, instance_id: T_ID) -> Dict[str, Any]:
        """Use this function if table has multicolumn primary key.
        See RegistrationRepository for example."""
        return {'instance_id': instance_id}
