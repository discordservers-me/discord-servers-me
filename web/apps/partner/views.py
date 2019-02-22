from django.views import generic
from .models import PartnerInformation


class PartnersView(generic.TemplateView):
    template_name = 'partner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ps_infos = PartnerInformation.objects.order_by('pk')
        context['partner_infos'] = ps_infos
        return context
