"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

Fields required to set the clock

{
  "speed": 4,
  "year": 1930,
  "month": 1,
  "day": 1,
  "hour": 6
}

{
    "speed": 4,
    "offset": 3029029272.269169,
    "start": "2025-12-26T11:01:12.269+00:00"
}
"""

from typing import Annotated

from annotated_types import Gt, Le, Ge
from pydantic import BaseModel

from mrcs_core.operations.clock import Clock


# ----------------------------------------------------------------------------------------------------------------

Speed = Annotated[int, Ge(1), Le(10)]
Year = Annotated[int, Gt(Clock.START_OF_TIME)]
Month = Annotated[int, Ge(1), Le(12)]
Day = Annotated[int, Ge(1), Le(31)]
Hour = Annotated[int, Ge(0), Le(23)]
Minute = Annotated[int, Ge(0), Le(59)]
Second = Annotated[int, Ge(0), Le(59)]


class ClockSetModel(BaseModel):
    speed: Speed

    year: Year
    month: Month
    day: Day
    hour: Hour
    minute: Minute = 0
    second: Second = 0


# ----------------------------------------------------------------------------------------------------------------

class ClockConfModel(BaseModel):
    speed: int
    offset: float
    start: str
