from pydantic import BaseModel
from typing import (List, Union)
from enum import Enum

class CalendarInterval(str, Enum):
    year = 'year'
    month = 'month'
    day = 'day'


class Term(BaseModel):
    field: str


class DateHistogram(BaseModel):
    field: str
    calendar_interval: CalendarInterval = CalendarInterval.month

class Facet(BaseModel):
    facet: Union[Term, DateHistogram]
