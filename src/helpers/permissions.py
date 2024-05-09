def is_participant(user_id, thread):
    return user_id in thread.participants.values_list("id", flat=True)
