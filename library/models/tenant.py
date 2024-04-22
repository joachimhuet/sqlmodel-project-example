from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from library.models.base import BaseModel, BaseTableModel

if TYPE_CHECKING:
    from library.models.site import SiteSQL


class TenantBase(BaseModel):
    name: str


class TenantSQL(TenantBase, BaseTableModel, table=True):

    __tablename__ = "tenantsql"

    id: Optional[int] = Field(default=None, primary_key=True)

    sites: list["SiteSQL"] = Relationship(
        back_populates="tenant",
        sa_relationship_kwargs=dict(lazy="selectin", cascade="delete"),
    )


class TenantCreate(TenantBase): ...


class TenantUpdate(TenantBase):
    id: int
    name: Optional[str] = None


class Tenant(TenantBase):
    id: int
