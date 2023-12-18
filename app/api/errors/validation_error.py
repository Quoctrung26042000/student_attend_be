from typing import Union

from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from collections import defaultdict
from fastapi.encoders import jsonable_encoder
from fastapi_validation_i18n import Translator  
from fastapi_validation_i18n._helpers import translate_errors

# async def http422_error_handler(
#     _: Request,
#     exc: Union[RequestValidationError, ValidationError],
# ) -> JSONResponse:
    
#     reformatted_message = defaultdict(list)
#     for pydantic_error in exc.errors():
#         loc, msg = pydantic_error["loc"], pydantic_error["msg"]
#         filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
#         field_string = ".".join(filtered_loc)  # nested fields with dot-notation
#         reformatted_message[field_string].append(msg)
    
#     return JSONResponse(
#         status_code=400,
#         content=jsonable_encoder(
#             {"error": reformatted_message}
#         ),
#     )


def http422_error_handler(
    i18n_exception_handler
) -> JSONResponse:
    
    async def func(_: Request,
        exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
            t = Translator("zh-TW", locale_path="app/resources/lang")
            print(exc.errors())
            errors = translate_errors(t, exc.errors())
            reformatted_message = defaultdict(list)
            for pydantic_error in errors:
                loc, msg = pydantic_error["loc"], pydantic_error["msg"]
                filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
                field_string = ".".join(str(filtered_loc))  # nested fields with dot-notation
                print("msggg", msg)
                print("field_string", field_string)
                reformatted_message[field_string].append(msg)
        
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(
                    {"error": reformatted_message}
                ),
            )

    return func

validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}
