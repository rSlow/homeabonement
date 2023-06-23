from django.conf import settings


def env_ctx_processor(request):
    context = {}

    if domain := settings.ENV.str("DOMAIN"):
        context["domain"] = domain
        context["abs_url"] = domain + request.path

    if support_email := settings.ENV.str("EMAIL_SUPPORT"):
        context["support_email"] = support_email

    return context
