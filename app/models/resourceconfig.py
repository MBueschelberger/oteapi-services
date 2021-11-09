"""
Pydantic ResourceConfig Data Model
"""

from typing import Dict, Optional
from pydantic import BaseModel, AnyUrl


class ResourceConfig(BaseModel):
    """Resource Configuration for Dataset Distributions"""

    downloadUrl: AnyUrl = None
    mediaType: str = None
    accessUrl: AnyUrl = None
    accessService: str = None
    license: Optional[str] = None
    accessRights: Optional[str] = None
    description: Optional[str] = None
    published: Optional[str] = None
    configuration: Optional[Dict] = None


class OTEUrl(BaseModel):
    """pydantic datamodel representing the AnyUrl type

    This class is useful when a strategy is created
    based on a field from AnyUrl, such as 'scheme' for
    download strategy
    """

    url: str
    scheme: str
    host: str
    tld: str
    host_type: str
    path: str
    query: str


def url_to_model(anyurl: AnyUrl) -> OTEUrl:
    """
    Convert the pydantic AnyUrl type to a OTEUrl datamodel
    """
    return OTEUrl(
        url=str(anyurl),
        scheme=anyurl.scheme,
        host=anyurl.host,
        tld=anyurl.tld,
        host_type=anyurl.host_type,
        path=anyurl.path,
        query=anyurl.path,
    )
