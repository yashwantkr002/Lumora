from django.http import JsonResponse
from django.shortcuts import redirect


def websocket_info(request):
    """
    Provide a lightweight chat transport endpoint that mirrors the future WebSocket contract.
    """

    if request.method == "POST":
        payload = {
            "status": "ready",
            "transport": "http",
            "message": "Realtime chat can be connected through this endpoint.",
        }
        return JsonResponse(payload)

    return redirect("conversations")