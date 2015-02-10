from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _

from forms_builder.forms.views import FormDetailMixin
from forms_builder.contrib.cmsplugin_forms_builder.models import Forms


@plugin_pool.register_plugin
class FormPlugin(CMSPluginBase, FormDetailMixin):
    module = _('Forms')
    model = Forms
    name = _('Forms plugin')
    render_template = 'forms/form_detail.html'
    text_enabled = False
    allow_children = False
    cache = False

    def render(self, context, instance, placeholder):
        """
        Display a built form and handle submission.
        """
        request = context['request']

        context.update({
            'form': instance.form,
        })

        if request.method == "POST":
            is_ajax, form, extra_context = self.form_post(request, instance.form.slug)
            context.update(extra_context)
            if not is_ajax:
                self.render_template = 'forms/form_sent.html'
        else:
            allowed, bits = self.form_get(request, context)
            if not allowed:
                context['form'] = None

        return context
