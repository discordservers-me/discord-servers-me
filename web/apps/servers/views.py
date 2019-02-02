from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
# from django.conf import settings

from .models import DiscordServer, ServerTag
from .forms import UpdateServerForm
from random import choices, randint


class ServerUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'server_update.html'
    form_class = UpdateServerForm
    context_object_name = 'server'
    model = DiscordServer

    def get_object(self):
        obj = get_object_or_404(
            DiscordServer,
            server_id=self.kwargs['server_id'],
            managers__manager_id=self.request.user.user_id)
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Server information updated successfully.')
        return reverse('server:detail', kwargs={'server_id': self.object.server_id})

    def form_valid(self, form):
        if 'tags' in form.cleaned_data:
            tags_obj = form.cleaned_data['tags']
            server = self.get_object()
            server.tags.add(*tags_obj)
        return super().form_valid(form)


class ServerDetailView(generic.DetailView):
    template_name = 'server_detail.html'
    model = DiscordServer
    context_object_name = 'server'

    def get_object(self):
        obj = get_object_or_404(
            DiscordServer,
            server_id=self.kwargs['server_id'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animated_emojis = context['server'].emojis.filter(animated=True)
        static_emojis = context['server'].emojis.filter(animated=False)
        context['animated_emojis'] = animated_emojis
        context['static_emojis'] = static_emojis
        return context


class ServerTop100ListView(generic.ListView):
    template_name = 'server_list_top_100.html'
    model = DiscordServer
    context_object_name = 'servers'
    paginate_by = 10
    # queryset = DiscordServer.objects.exclude(invite_link='', shown=False)
    # ordering = 'premium_tier', '-member_count'

    def get_queryset(self):
        top_100 = DiscordServer.objects.exclude(Q(invite_link='') | Q(shown=False)).order_by('-member_count')[:100]
        return top_100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tier_servers = DiscordServer.objects.filter(premium_tier__in=[1, 2]).exclude(Q(invite_link='') | Q(shown=False))
        if tier_servers.exists():
            tier_1_count = 0
            tier_2_count = 0
            for server in tier_servers:
                if server.premium_tier == 1:
                    tier_1_count += 1
                elif server.premium_tier == 2:
                    tier_2_count += 1

            rate = []
            for server in tier_servers:
                if server.premium_tier == 1:
                    rate.append((4 / 11) / tier_1_count)
                elif server.premium_tier == 2:
                    rate.append((7 / 11) / tier_2_count)

            server_count = context['servers'].count()
            while True:
                result = choices(tier_servers, rate, k=2)
                if len(list(set(result))) == 2 or len(rate) <= 2:
                    for sv in result:
                        server_qs = DiscordServer.objects.filter(server_id=sv.server_id)
                        new_qs = list(context['servers'])
                        premium_server = list(server_qs)[0]
                        if (premium_server in new_qs) and (new_qs[0] == premium_server):
                            random_pos = randint(1, server_count)
                            new_qs.remove(premium_server)
                        if premium_server not in new_qs:
                            random_pos = randint(1, server_count)
                            new_qs.insert(random_pos, list(server_qs)[0])
                        context['servers'] = new_qs
                    break

        return context


class ServerTagListView(generic.ListView):
    template_name = 'server_list_tag.html'
    model = DiscordServer
    context_object_name = 'servers'
    paginate_by = 11
    # queryset = DiscordServer.objects.exclude(invite_link='', shown=False)
    # ordering = 'premium_tier', '-member_count'

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        servers = DiscordServer.objects.exclude(Q(invite_link='') | Q(shown=False)).order_by('-member_count')
        servers_by_tag = servers.filter(tags__name__iexact=tag)
        if not servers_by_tag.exists():
            self.tag_does_not_exist = True
            return servers
        else:
            self.tag_does_not_exist = False
            return servers_by_tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tier_servers = DiscordServer.objects.exclude(Q(invite_link='') | Q(shown=False)).filter(premium_tier__in=[1, 2])
        if tier_servers.exists():
            tier_1_count = 0
            tier_2_count = 0
            for server in tier_servers:
                if server.premium_tier == 1:
                    tier_1_count += 1
                elif server.premium_tier == 2:
                    tier_2_count += 1

            rate = []
            for server in tier_servers:
                if server.premium_tier == 1:
                    rate.append((4 / 11) / tier_1_count)
                elif server.premium_tier == 2:
                    rate.append((7 / 11) / tier_2_count)

            server_count = context['servers'].count()
            while True:

                result = choices(tier_servers, rate, k=2)
                if len(list(set(result))) == 2 or len(rate) <= 2:
                    for sv in result:
                        server_qs = DiscordServer.objects.filter(server_id=sv.server_id)
                        new_qs = list(context['servers'])
                        premium_server = list(server_qs)[0]
                        if (premium_server in new_qs) and (new_qs[0] == premium_server):
                            random_pos = randint(1, server_count)
                            new_qs.remove(premium_server)
                        if premium_server not in new_qs:
                            random_pos = randint(1, server_count)
                            new_qs.insert(random_pos, list(server_qs)[0])
                        context['servers'] = new_qs
                    break
        if self.tag_does_not_exist:
            context['tag_does_not_exist'] = True
        context['tag'] = self.kwargs.get('tag', None)
        context['tags'] = ServerTag.objects.order_by('name')
        return context


class ServerSearchListView(generic.ListView):
    template_name = 'server_list_search.html'
    context_object_name = 'servers'
    paginate_by = 10
    vector = SearchVector('name') + SearchVector('short_description') + SearchVector('description')

    def get_queryset(self):
        search_term = self.request.GET.get('term', None)
        print(search_term)
        server_qs = DiscordServer.objects.exclude(Q(invite_link='') | Q(shown=False))
        if search_term:
            query = SearchQuery(search_term)
            rank = SearchRank(self.vector, query)
            server_qs = server_qs.annotate(rank=rank).order_by('-rank')
        else:
            server_qs = server_qs.order_by('-member_count')[:100]
        return server_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tier_servers = DiscordServer.objects.filter(premium_tier__in=[1, 2]).exclude(Q(invite_link='') | Q(shown=False))
        if tier_servers.exists():
            tier_1_count = 0
            tier_2_count = 0
            for server in tier_servers:
                if server.premium_tier == 1:
                    tier_1_count += 1
                elif server.premium_tier == 2:
                    tier_2_count += 1

            rate = []
            for server in tier_servers:
                if server.premium_tier == 1:
                    rate.append((4 / 11) / tier_1_count)
                elif server.premium_tier == 2:
                    rate.append((7 / 11) / tier_2_count)

            server_count = context['servers'].count()
            while True:

                result = choices(tier_servers, rate, k=2)
                if len(list(set(result))) == 2 or len(rate) <= 2:
                    for sv in result:
                        server_qs = DiscordServer.objects.filter(server_id=sv.server_id)
                        new_qs = list(context['servers'])
                        premium_server = list(server_qs)[0]
                        if (premium_server in new_qs) and (new_qs[0] == premium_server):
                            random_pos = randint(1, server_count)
                            new_qs.remove(premium_server)
                        if premium_server not in new_qs:
                            random_pos = randint(1, server_count)
                            new_qs.insert(random_pos, list(server_qs)[0])
                        context['servers'] = new_qs
                    break

        return context
