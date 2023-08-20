from pydantic import BaseModel
from typing import List

class TenantToUpdateRequest(BaseModel):
    tenant_list: List["TenantToUpdateRequest.TenantToUpdate"]
    class TenantToUpdate(BaseModel):
        racTenantId: str
        connectorId: str
        connectorToken: str