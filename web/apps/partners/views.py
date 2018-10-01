from django.views import generic
from .models import PartnersInformation


class PartnersView(generic.TemplateView):
    template_name = 'partners.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ga_infos = PartnersInformation.objects.order_by('pk')
        context['partners_infos'] = ga_infos
        return context
