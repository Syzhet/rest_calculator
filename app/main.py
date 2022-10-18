from typing import Dict, Union

from fastapi import Depends, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

from .models import BodyPhrase, QueryPhrase

app: FastAPI = FastAPI()


@app.exception_handler(ValueError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request, exc: Union[ValueError, RequestValidationError]
) -> Union[JSONResponse, PlainTextResponse]:
    """Exception handler for data validation."""

    if request.scope['method'] == 'POST':
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': str(exc).split('\n')[-1]}
        )
    return PlainTextResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=str(exc).split('\n')[-1].strip()
    )


@app.get('/')
@app.get('/index')
async def index() -> PlainTextResponse:
    """Handler of the get request to the main page."""

    return PlainTextResponse(
        content='Hello world!',
        status_code=status.HTTP_200_OK)


@app.get('/eval', status_code=status.HTTP_200_OK)
async def get_calc(
    phrase: QueryPhrase = Depends(QueryPhrase)
) -> PlainTextResponse:
    """Get request handler with string parameter."""

    expression: Dict[str:str] = phrase.dict()
    try:
        expression['result'] = eval(expression['phrase'])
    except Exception:
        return PlainTextResponse(
            content='Bad operands or operators',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    result_text: str = '{phrase} = {result}'
    return PlainTextResponse(
        content=result_text.format(**expression),
    )


@app.post('/eval')
async def calculator(phrase: BodyPhrase) -> JSONResponse:
    """Post request handler with body parameter."""

    expression: Dict[str:str] = phrase.dict()
    try:
        expression['result'] = eval(expression['phrase'])
    except Exception:
        return JSONResponse(
            content={'error': 'Bad operands or operators'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    result_text: str = '{phrase} = {result}'

    return JSONResponse(
        content={'result': result_text.format(**expression)},
        status_code=status.HTTP_201_CREATED
    )
