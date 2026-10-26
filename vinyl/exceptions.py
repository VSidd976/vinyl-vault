from rest_framework.response import Response
from rest_framework import status

def error_response(message, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "error": {
                "message": message,
                "details": details or {}
            }
        },
        status=status_code
    )
