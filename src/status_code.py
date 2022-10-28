
def statusCode(status_code):
    message = { 
                504: "Error 504 Gateway Timeout",
                503: "Error 503 Service Unavailable",
                500: "Error 500 Internal Server Error",
                404: "Error 404 Not Found",
                403: "Error 403 Forbidden",
                401: "Error 401 Unauthorized",
                400: "Error 400 Bad Request",
                204: "Error 204 No Content",
                200: "OK",
                201: "Created",
                202: "Acceped"
                }
    
    return message[status_code]