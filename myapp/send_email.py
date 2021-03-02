from django.core.mail import EmailMessage
from django.template.loader import get_template

def sender(email,name,activate_link):
    subject = 'Activate your account'

    message=get_template('email.html').render({
        'name':name,
        'activate_link':activate_link  })

    email = EmailMessage(
        subject,
        message,
        'teamfirecode.project@gmail.com',
        [email],
    )
    email.content_subtype='html'
    return email
