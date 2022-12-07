from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class ActivateAccountTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash(self, user, timestamp):

        return (
                six.text_type(user.pk)+
                six.text_type(timestamp)+
                six.text_type(user.is_active)
                )


activate_account_token = ActivateAccountTokenGenerator()
