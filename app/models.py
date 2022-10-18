import re
from typing import Union

from fastapi import Query
from pydantic import BaseModel, validator

REGEX_FOR_CHECK_PHRASE = re.compile(
    r'([-+()]?[0-9]*\.?[0-9]+[\/\+\-\*])+([-+]?[0-9]*\.?[0-9]+)'
)


class QueryPhrase(BaseModel):
    """Model class for working with the string parameter."""

    phrase: str = Query(max_length=100)

    @validator('phrase')
    def check_query_phrase(cls, value) -> Union[str, Exception]:
        """Value validation method."""

        value: str = value.strip().replace(' ', '+')
        if REGEX_FOR_CHECK_PHRASE.match(value):
            return value
        else:
            raise ValueError('Bad operands or operators')


class BodyPhrase(BaseModel):
    phrase: str

    @validator('phrase')
    def check_body_phrase(cls, value) -> Union[str, Exception]:
        if REGEX_FOR_CHECK_PHRASE.match(value):
            return value
        else:
            raise ValueError('Bad operands or operators')
