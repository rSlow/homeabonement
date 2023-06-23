from pathlib import Path
from typing import Any

from django.http import HttpResponse
from django.views.generic import TemplateView

from apps.pages.services.email_renderer import EmailRenderer, PremailerRenderer


class PrerenderTemplateView(TemplateView):
    scss_filepaths: list[Path] = []
    premailer_kwargs: dict[str, Any] = {}
    use_premailer: bool = True

    def render_to_response(self,
                           context,
                           **response_kwargs):
        if self.use_premailer:
            compiled_template = PremailerRenderer.render(
                template_name=self.template_name,
                context=context,
                using=self.template_engine,
                request=self.request,
                **self.premailer_kwargs,
            )
        else:
            compiled_template = EmailRenderer.compile_template(
                template_name=self.template_name,
                context=context,
                using=self.template_engine,
                request=self.request,
                scss_filepaths=self.scss_filepaths,
            )
        response_kwargs.setdefault("content_type", self.content_type)
        response = HttpResponse(
            content=compiled_template,
            **response_kwargs,
        )
        response._request = self.request
        return response
