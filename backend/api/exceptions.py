from rest_framework.views import exception_handler
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return JsonResponse(
            {
                "success": False,
                "status": 500,
                "error": {
                    "message": "Internal server error."
                }
            },
            status=500
        )

    details = response.data
    if isinstance(details, dict) and "detail" in details:
        message = str(details["detail"])
        details = None if len(details) == 1 else {
            key: value for key, value in details.items() if key != "detail"
        }
    else:
        message = "Request failed."

    error = {"message": message}
    if details:
        error["details"] = details

    return JsonResponse(
        {
            "success": False,
            "status": response.status_code,
            "error": error,
        },
        status=response.status_code
    )