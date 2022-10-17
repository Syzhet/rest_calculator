from typing import Dict, Union

from fastapi import FastAPI, Depends, status
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

from models import QueryPhrase, BodyPhrase


app: FastAPI = FastAPI()


@app.exception_handler(ValueError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request, exc: Union[ValueError, RequestValidationError]
) -> Union[JSONResponse, PlainTextResponse]:
    """Exception handler for data validation."""

    if request.scope['method'] == 'POST':
        print('------------------')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            # content=str(exc)
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
    except ZeroDivisionError:
        return PlainTextResponse(
            content='Division by zero is not possible',
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
    except ZeroDivisionError:
        return JSONResponse(
            content={'error': 'Division by zero is not possible'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    result_text: str = '{phrase} = {result}'

    return JSONResponse(
        content={'result': result_text.format(**expression)},
        status_code=status.HTTP_201_CREATED
    )
