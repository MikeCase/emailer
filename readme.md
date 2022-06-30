# Email wrapper around smtplib.

This code creates a context manager for smtplib allowing you to create and send an HTML emails that are built with markdown or jinja templates.

```py
from emailer import Emailer

template_type = 'markdown' # markdown or jinja
template_file = 'templates/template.md' # location of your template file, markdown or jinja file
host = 'smtp.host.com' # SMTP server
port = 587 # SMTP port
user = 'username' # SMTP username
password = 'password' # SMTP password

subject = 'Subject of email'
email_list = [] # List of email address(es) to send the email to.

with Emailer(host, port, user, password) as emailer:
        message = emailer.gen_html_file(template_type, template_file)
        email = emailer.build_message(subject, email_list, message, msg_type='html')
        emailer.send_email(email_list, email)
```

Thats a basic script.

Jinja templates will default to finding the template file in the templates directory, so, you're going to need to create a templates directory