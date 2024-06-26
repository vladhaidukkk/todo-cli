from datetime import datetime
from typing import Annotated

from sqlalchemy import FetchedValue
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime,
    mapped_column(server_default=func.current_timestamp()),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=func.current_timestamp(),
        server_onupdate=FetchedValue(for_update=True),
    ),
]
