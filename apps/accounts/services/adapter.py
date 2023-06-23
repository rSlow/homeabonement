from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_str

from apps.pages.services.email_renderer import PremailerRenderer


class PrerenderAccountAdapter(DefaultAccountAdapter):
    TEMPLATE_BASE_DIR = "email_templates/"
    SIGNUP = "_signup"
    TEMPLATE_SUB_DIRS = {
        "account_already_exists": "account_already_exists/",
        "email_confirmation": "email_confirmation/",
        "password_reset_key": "password_reset_key/",
        "unknown_account": "unknown_account/",
    }

    def get_template_alias(self, template_name: str):
        template_alias = template_name.split("/")[-1]

        if template_alias.endswith(self.SIGNUP):
            template_alias = template_alias[:-len(self.SIGNUP)]

        try:
            template_dir = self.TEMPLATE_SUB_DIRS[template_alias]
        except (KeyError, AttributeError):
            template_dir = ""

        full_template_alias = self.TEMPLATE_BASE_DIR + template_dir + template_alias
        return full_template_alias

    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email

        subject_alias = self.get_template_alias(template_prefix)
        # -- change ext file to .html
        subject = render_to_string("{0}_subject.html".format(subject_alias), context)

        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                # -- alias template to custom directory
                template_alias = self.get_template_alias(template_prefix)
                template_name = "{0}_message.{1}".format(template_alias, ext)
                # -- render with premailer renderer
                bodies[ext] = PremailerRenderer.render(
                    template_name,
                    context,
                    self.request
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, headers=headers
            )
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(subject, bodies["html"], from_email, to, headers=headers)
            msg.content_subtype = "html"  # Main content is now text/html
        return msg

    def format_email_subject(self, subject):
        prefix = f" - ДОМАШНИЙ АБОНЕМЕНТ"
        return force_str(subject) + prefix
