from functools import wraps
import traceback
from app.errors import AppError, app_error_dumper

from app.errors.docker import ContainerNotFound, ErrorInContainer

def handler_exception(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        error_response, error_code = None,None
        try:
            return func(*args,**kwargs)      
        except ErrorInContainer as e:
            error_response = AppError(e.msg)
            error_code = 409
        except ContainerNotFound as e:
            error_response = AppError(e.msg)
            error_code = 404
        except Exception as e:
            print(traceback.format_exc())
            error_response = AppError("Unhandle error")
            error_code = 500
        return app_error_dumper(error_response), error_code
    
    return wrapper
