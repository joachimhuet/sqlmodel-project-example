from typing import Optional

from library.crud.base import CRUDBase
from library.models.tenant import Tenant, TenantCreate, TenantSQL, TenantUpdate


class CRUDTenant(CRUDBase[TenantSQL, TenantCreate, TenantUpdate, Tenant]):
    table_model = TenantSQL
    create_schema = TenantCreate
    update_schema = TenantUpdate
    read_schema = Tenant

    # Override method for type-hinting purposes id changes from Any to int
    def get(self, id: int) -> Optional[Tenant]:
        return super().get(id)

    def remove(self, id: int) -> Optional[Tenant]:
        return super().remove(id)

    def get_by_name(self, name: str) -> Optional[Tenant]:
        tenants = self.get_multiple(name=name, limit=1)
        return tenants[0] if tenants else None
