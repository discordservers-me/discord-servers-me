from django.views import generic
from .models import GiveawayInformation


class GiveAwayView(generic.TemplateView):
    template_name = 'giveaway.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ga_infos = GiveawayInformation.objects.exclude(ended=True).order_by('pk')
        context['ga_infos'] = ga_infos
        return context
