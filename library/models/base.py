from typing import Any, Callable, ClassVar, Optional, Union
from sqlmodel import SQLModel


class BaseModel(SQLModel):
    def get_date(self):
        if hasattr(self, "date"):
            return self.date
        return None


class BaseTableModel(
    BaseModel
):  # Cannot set `table=True` here because it is a base class
    """Inheriting table must set table=True and
    provide a __tablename__ attribute."""

    __tablename__: ClassVar[Union[str, Callable[..., str]]]


class BaseSearchCriteria(BaseModel):
    offset: int = 0
    limit: Optional[int] = None
    order_by: Optional[str] = None
    order_desc: bool = False

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        kwargs.pop("exclude_none", None)  # remove exclude_none from kwargs
        return super().model_dump(*args, exclude_none=True, **kwargs)
