from typing import Optional

from library.crud.base import CRUDBase
from library.models.site import Site, SiteCreate, SiteSQL, SiteUpdate


class CRUDSite(CRUDBase[SiteSQL, SiteCreate, SiteUpdate, Site]):
    table_model = SiteSQL
    create_schema = SiteCreate
    update_schema = SiteUpdate
    read_schema = Site

    # Override method for type-hinting purposes id changes from Any to int
    def get(self, id: int) -> Optional[Site]:
        return super().get(id)

    def remove(self, id: int) -> Optional[Site]:
        return super().remove(id)
