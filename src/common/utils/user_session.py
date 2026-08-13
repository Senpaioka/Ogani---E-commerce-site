

def _user_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


