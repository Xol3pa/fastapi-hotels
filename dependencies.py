from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Page number", ge=1)]
    per_page: Annotated[int | None, Query(3, description="Number of hotels per page", ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]