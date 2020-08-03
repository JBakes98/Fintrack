from django import template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.template import Context


class EmailTemplate(models.Model):
    """
    Email templates that are stored in the database so admins can change them on
    the fly without code having to be changed
    """
    subject = models.CharField(max_length=255, null=True, blank=True)
    to_email = models.CharField(max_length=255, null=True, blank=True)
    from_email = models.CharField(max_length=255, null=True, blank=True)
    html_template = models.TextField(null=True, blank=True)
    plain_text = models.TextField(null=True, blank=True)

    template_key = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'
        ordering = ['subject', ]

    def __str__(self):
        return "<{}> {}".format(self.template_key, self.subject)

    def get_rendered_template(self, tpl, context):
        return self.get_template(tpl).render(context)

    def get_template(self, tpl):
        return template.Template(tpl)

    def get_subject(self, subject, context):
        return subject or self.get_rendered_template(self.subject, context)

    def get_body(self, body, context):
        return body or self.get_rendered_template(self._get_body(), context)

    def get_sender(self):
        return self.from_email or settings.DEFAULT_FROM_EMAIL

    def get_recipient(self, emails, context):
        return emails or [self.get_rendered_template(self.to_email, context)]

    @staticmethod
    def send(*args, **kwargs):
        EmailTemplate._send(*args, **kwargs)

    @staticmethod
    def _send(template_key, context, subject=None, body=None, sender=None,
              emails=None, bcc=None, attachments=None):
        mail_template = EmailTemplate.objects.get(template_key=template_key)
        context = Context(context)

        subject = mail_template.get_subject(subject, context)
        body = mail_template.get_body(body, context)
        sender = sender or mail_template.get_sender()
        emails = mail_template.get_recipient(emails, context)

        if not mail_template.html_template:
            return send_mail(subject, body, sender, emails, fail_silently=not
            settings.DEBUG)

        msg = EmailMultiAlternatives(subject, body, sender, emails,
                                     alternatives=((body, 'text/html'),),
                                     bcc=bcc
                                     )
        if attachments:
            for name, content, mimetype in attachments:
                msg.attach(name, content, mimetype)
        return msg.send(fail_silently=not (settings.DEBUG or settings.TEST))

    def _get_body(self):
        if not self.html_template:
            return self.plain_text

        return self.html_template
