from pydantic import BaseModel
from typing import List

class TenantReportRequest(BaseModel):
    tenant_list: List["TenantReportRequest.TenantReportItem"]
    class TenantReportItem(BaseModel):
        racTenantId: str
        connectorId: str
        carolTenantId: str
        connectorToken: str