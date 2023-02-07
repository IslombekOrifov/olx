

def upload_avatar_path(instance, avatar):
    return f"users/{instance.USERNAME_FIELD}/avatar/{avatar}"


def upload_resume_path(instance, resume):
    return f"users/{instance.USERNAME_FIELD}/resume/{resume}"