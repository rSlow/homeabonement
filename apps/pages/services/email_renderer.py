from pathlib import Path
from typing import Any

import sass
from css_inline import css_inline
from django.conf import settings
from django.template.loader import render_to_string
from premailer import Premailer


class EmailRenderer:
    @classmethod
    def compile_template(cls,
                         template_name: str,
                         context: Any | None = None,
                         using: Any | None = None,
                         request: Any | None = None,
                         scss_filepaths: list[Path] | None = None):
        response_string = render_to_string(
            template_name=template_name,
            request=request,
            context=context,
            using=using
        )
        compiled_css = cls.compile_scss(scss_filepaths=scss_filepaths)
        inlined_response_string = cls.inline_css_in_response(
            response=response_string,
            extra_css=compiled_css
        )
        return inlined_response_string

    @staticmethod
    def compile_scss(scss_filepaths: list[Path]):
        return "".join([sass.compile(filename=scss_filepath.as_posix()) for scss_filepath in scss_filepaths])

    @staticmethod
    def inline_css_in_response(response: str,
                               extra_css: str | None = None):
        return css_inline.inline(
            html=response,
            load_remote_stylesheets=False,
            extra_css=extra_css
        )


class PremailerRenderer:
    premailer = Premailer(
        base_url=settings.PREMAILER_DOMAIN,
        allow_network=True,
        allow_loading_external_files=True,
    )

    @classmethod
    def render(cls,
               template_name: str,
               context: Any = None,
               request: Any = None,
               using: Any = None,
               **premailer_kwargs: dict[str, Any] | None):
        pre_rendered_response = render_to_string(
            template_name=template_name,
            context=context,
            request=request,
            using=using
        )
        rendered_response = cls.premailer.transform(
            html=pre_rendered_response,
            **premailer_kwargs
        )
        return rendered_response
