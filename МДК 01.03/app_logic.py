class CurrentUser:
    def __init__(self):
        self.id = None
        self.username = None
        self.email = None
        self.phone = None
        self.experience = None
        self.user_type = 'job_seeker'
        self.is_logged_in = False

current_user = CurrentUser()