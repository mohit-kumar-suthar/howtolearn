from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.six import text_type

class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

generate_token = ActivationTokenGenerator()

class ResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp)+text_type(user.last_login))

reset_token = ResetTokenGenerator()

