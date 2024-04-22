from typing import Any, Generic, Optional, Type, TypeVar
from sqlmodel import desc
from sqlalchemy.orm import Session

from ..models.base import BaseTableModel, BaseModel

TableModelType = TypeVar("TableModelType", bound=BaseTableModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[TableModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]
):
    db: Session
    table_model: Type[TableModelType]
    create_schema: Type[CreateSchemaType]
    update_schema: Type[UpdateSchemaType]
    read_schema: Type[ReadSchemaType]

    def __init__(self, db: Session) -> None:
        self.db = db

    def _from_create(self, to_create: CreateSchemaType) -> TableModelType:
        """Converts a CreateSchemaType object to a TableModelType object."""
        return self.table_model.model_validate(to_create)

    def _from_table(self, table: TableModelType) -> ReadSchemaType:
        """Converts a TableModelType object to a ReadSchemaType object."""
        return self.read_schema.model_validate(table)

    def add(self, to_create: CreateSchemaType) -> ReadSchemaType:
        created: TableModelType = self._from_create(to_create)
        self.db.add(created)
        self.db.commit()
        self.db.refresh(
            created
        )  # updates the object with the new entries of the db
        return self._from_table(created)

    def update(self, to_update: UpdateSchemaType) -> Optional[ReadSchemaType]:
        # get current object of same id on db
        current: Optional[TableModelType] = self._get(to_update.id)

        if not current:
            # if object does not exist, return None
            return None

        # update each field of the current object with the new values
        for field, value in to_update.model_dump(
            # exclude unset values to not put every unset field to None
            exclude_unset=True,
            # keep none if you need to set a field specifically to None
            exclude_none=False,
        ).items():
            setattr(current, field, value)

        self.db.commit()
        self.db.refresh(current)
        return self._from_table(current)

    def remove(self, id: Any) -> Optional[ReadSchemaType]:
        to_delete = self._get(id)
        if not to_delete:
            return None
        self.db.delete(to_delete)
        self.db.commit()
        return self._from_table(to_delete)

    def _get_multiple(
        self,
        *args,
        offset: int = 0,
        limit: Optional[int] = None,
        order_by: Optional[list[str]] = None,
        order_desc: bool = False,
        **kwargs
    ) -> list[TableModelType]:
        args = tuple(arg for arg in args if arg is not None)
        _query = (
            self.db.query(self.table_model).filter(*args).filter_by(**kwargs)
        )
        if order_by:
            if order_desc:
                _query = _query.order_by(*[desc(ob) for ob in order_by])
            else:
                _query = _query.order_by(*order_by)
        if limit:
            _query = _query.limit(limit)
        if offset:
            _query = _query.offset(offset)

        return _query.all()

    def get_multiple(
        self,
        *args,
        offset: int = 0,
        limit: Optional[int] = None,
        order_by: Optional[list[str]] = None,
        order_desc: bool = False,
        **kwargs
    ) -> list[ReadSchemaType]:
        results = self._get_multiple(
            *args,
            offset=offset,
            limit=limit,
            order_by=order_by,
            order_desc=order_desc,
            **kwargs,
        )
        return [self._from_table(result) for result in results]

    def count(self, *args, **kwargs) -> int:
        return (
            self.db.query(self.table_model)
            .filter(*args)
            .filter_by(**kwargs)
            .count()
        )

    def _get(self, id: Any) -> Optional[TableModelType]:
        return self.db.query(self.table_model).filter_by(id=id).first()

    def get(self, id: Any) -> Optional[ReadSchemaType]:
        result = self._get(id)
        if result:
            return self._from_table(result)
        return None
