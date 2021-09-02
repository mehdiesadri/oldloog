def is_session_invalid(session):
    in_session = session.chatsessionuser_set.all()
    in_session_count = in_session.count()
    return not (in_session_count == 0 or in_session_count >= 3 or session.is_expired or (in_session_count == 1 and not session.is_open_for_first_join))

def is_user_in_session(user, session):
    return session.chatsessionuser_set.filter(user=user).exists()
