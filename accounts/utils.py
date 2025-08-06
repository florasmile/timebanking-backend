from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = user.pk
    verify_url = request.build_absolute_uri(
        reverse('verify-email') + f"?uid={uid}&token={token}"
    )
    send_mail(
        subject='Verify your email',
        message=f'Click the link to verify your email: {verify_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )