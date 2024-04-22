from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship

from library.models.base import BaseModel, BaseTableModel
from library.models.tenant import Tenant

if TYPE_CHECKING:
    from library.models.tenant import TenantSQL


class SiteBase(BaseModel):
    name: str


class SiteSQL(SiteBase, BaseTableModel, table=True):
    __tablename__ = "sitesql"

    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key="tenantsql.id")
    tenant: "TenantSQL" = Relationship(
        back_populates="sites",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class SiteCreate(SiteBase):
    tenant_id: int


class SiteUpdate(SiteBase):
    id: int
    name: Optional[str] = None
    tenant_id: Optional[int] = None


class Site(SiteBase):
    id: int
    tenant: Tenant
