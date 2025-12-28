# chatbot_app/views.py
from __future__ import annotations

import json
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
# from .rag_system import chatbot_system



def chat_view(request):
    """
    Renders the chat UI template.
    """
    # ensure a session_key exists for per-session memory
    if not request.session.session_key:
        request.session.save()
    return render(request, "chatbot/chatbot.html")



def chat_handler(request):
    """
    SSE endpoint.
    GET ?message=...  or  POST {"message": "..."}
    Streams tokens as:  data: {"token": "..."}\n\n
    Ends with:         event: end\n data: \n\n
    """
    if not request.session.session_key:
        request.session.save()

    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
            question = payload.get("message", "")
        except Exception:
            question = ""
    else:
        question = request.GET.get("message", "")

    if not question:
        return JsonResponse({"error": "empty message"}, status=400)

    user = request.user
    session_id = request.session.session_key

    def event_stream():
        try:
            for token in chatbot_system.stream_response(user, session_id, question):
                yield f"data: {json.dumps({'token': token})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            yield "event: end\ndata: \n\n"

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
