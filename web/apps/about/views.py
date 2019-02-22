from django.views import generic
from .models import AboutContent


class AboutView(generic.TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_info = AboutContent.objects.order_by('pk')
        context['about_infos'] = about_info
        return context
