from django.core.mail import EmailMessage
from django.template.loader import get_template

def sender(action,email,name,activate_link):
    subject=''
    if action == 'register_user':
        subject = 'Activate your account'
     
    if action == 'reset_password':
        subject = 'Reset you account password'
        

    message=get_template('email.html').render({
        'name':name,
        'subject':subject,
        'activate_link':activate_link  })

    email = EmailMessage(
        subject,
        message,
        'teamfirecode.project@gmail.com',
        [email],
    )
    email.content_subtype='html'
    return email
