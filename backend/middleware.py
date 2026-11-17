from .errors import json_error_response


class JsonErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception:
            return json_error_response(500, "Internal server error.")

        if response.status_code < 400:
            return response

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return response

        messages = {
            400: "Bad request.",
            401: "Authentication required.",
            403: "Permission denied.",
            404: "Endpoint not found.",
            405: "Method not allowed.",
            408: "Request timeout.",
            409: "Conflict.",
            429: "Too many requests.",
        }
        message = messages.get(
            response.status_code,
            "Request failed." if response.status_code < 500 else "Internal server error.",
        )
        return json_error_response(response.status_code, message)