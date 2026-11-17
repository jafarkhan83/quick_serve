from django.http import JsonResponse


def json_error_response(status, message):
    return JsonResponse(
        {
            "success": False,
            "status": status,
            "error": {
                "message": message,
            },
        },
        status=status,
    )


def api_400(request, exception):
    return json_error_response(400, "Bad request.")


def api_403(request, exception):
    return json_error_response(403, "Permission denied.")


def api_404(request, exception):
    return json_error_response(404, "Endpoint not found.")


def api_500(request):
    return json_error_response(500, "Internal server error.")