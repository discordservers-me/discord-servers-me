from django.views.generic import TemplateView
from web.apps.servers.models import DiscordServer, ServerTag
from django.db.models import Q


class HomeView(TemplateView):
    template_name = 'home.html'
    context_object_name = 'servers'  # Default: object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servers = DiscordServer.objects.exclude(Q(invite_link='') | Q(shown=False))
        tier_1_servers = servers.filter(premium_tier=1).order_by('-bumped_at')[:4]
        tier_2_servers = servers.filter(premium_tier=2).order_by('-bumped_at')[:7]

        server_qs = list(tier_2_servers) + list(tier_1_servers)
        tier_0_servers = servers.order_by('-member_count')[:11 - len(server_qs)]
        server_qs += list(tier_0_servers)
        tags = ServerTag.objects.all().order_by('name')

        context['servers'] = server_qs
        context['tags'] = tags
        return context
