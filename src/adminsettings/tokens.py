from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from datetime import datetime


class SettingsChangeTokenGenerator(PasswordResetTokenGenerator):
    def make_token(self, user):
        time = datetime.now()
        timestamp = int(str(time.year) + str(time.month) + str(time.day) + str(time.hour) + str(time.minute))
        return self._make_token_with_timestamp(user, timestamp)

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.password)
        )


settings_change_token = SettingsChangeTokenGenerator()
