from __future__ import absolute_import

from brake.decorators import ratelimit
from brake import ALL, UNSAFE

"""
This is taken from the django-ratelimit project. Which is apache licenced. 

Many thanks to James Socol.

"""

__all__ = ['RatelimitMixin']


class RatelimitMixin(object):
    """
    Mixin for usage in Class Based Views
    configured with the decorator ``ratelimit`` defaults.
    Configure the class-attributes prefixed with ``ratelimit_``
    for customization of the ratelimit process.
    Example::
        class ContactView(RatelimitMixin, FormView):
            form_class = ContactForm
            template_name = "contact.html"
            # Limit contact form by remote address.
            ratelimit_key = 'ip'
            ratelimit_block = True
            def form_valid(self, form):
                # Whatever validation.
                return super(ContactView, self).form_valid(form)
    """
    ratelimit_ip = True
    ratelimit_use_request_path = False
    ratelimit_rate = '5/m'
    ratelimit_block = False
    ratelimit_field = None
    ratelimit_increment = None
    ratelimit_method = ALL

    ALL = ALL
    UNSAFE = UNSAFE

    def get_ratelimit_config(self):
        return dict(
            (k[len("ratelimit_"):], v)
            for k, v in vars(self.__class__).items()
            if k.startswith("ratelimit")
        )

    def dispatch(self, *args, **kwargs):
        return ratelimit(
            **self.get_ratelimit_config()
        )(super(RatelimitMixin, self).dispatch)(*args, **kwargs)