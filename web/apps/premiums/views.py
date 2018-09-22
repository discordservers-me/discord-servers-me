from django.views import generic
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import reverse
from django.utils.html import format_html
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings

from web.apps.servers.models import DiscordServer
from .forms import UserServersForm
from .models import PremiumFeature


class CustomPaypalButton(PayPalPaymentsForm):

    def __init__(self, *args, **kwargs):
        if 'form_id' in kwargs:
            self.custom_form_id = kwargs.pop('form_id')
        else:
            self.custom_form_id = ''
        super().__init__(*args, **kwargs)

    def render(self):
        form_tag_open = f'<form action="{self.get_endpoint()}" id="{self.custom_form_id}" method="post">'
        form_fields = self.as_p()
        form_button = '<button type="submit" class="btn-large waves-effect waves-light indigo white-text">Paypal Checkout</button>'
        form_tag_end = '</form>'
        return format_html(form_tag_open + form_fields + form_button + form_tag_end)


class PremiumView(generic.TemplateView):
    template_name = 'premium_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tier0_features = PremiumFeature.objects.filter(tier__tier=0).order_by('ordering')
        tier1_features = PremiumFeature.objects.filter(tier__tier=1).order_by('ordering')
        tier2_features = PremiumFeature.objects.filter(tier__tier=2).order_by('ordering')

        context['tier0_features'] = tier0_features
        context['tier1_features'] = tier1_features
        context['tier2_features'] = tier2_features

        # if tier1_features.count() % 2 != 0:
        #     context['tier1_odd'] = True

        # if tier2_features.count() % 2 != 0:
        #     context['tier2_odd'] = True

        return context


class PremiumPaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'premium_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # What you want the button to do.
        paypal_info = {
            "business": settings.PAYPAL_EMAIL_ACCOUNT,
            "amount": "",
            "item_name": "",
            # "invoice": "unique-invoice-id",
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return": self.request.build_absolute_uri(reverse('premium:success')),
            "cancel_return": self.request.build_absolute_uri(reverse('premium:canceled')),
            "custom": "",
        }

        paypal_form = CustomPaypalButton(initial=paypal_info, form_id='paypal_checkout')
        context['paypal_form'] = paypal_form

        server_choice = UserServersForm(user=self.request.user)
        # print(dir(server_choice.fields['server']))
        # print(server_choice.fields['server'].choices)
        context['server_choice'] = server_choice
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            sid = request.GET.get('sid', None)
            if sid:
                try:
                    server_obj = DiscordServer.objects.get(pk=sid, managers__manager_id=request.user.user_id)
                    template = 'premium_payment_partial_premium_info.html'
                    html_result = render_to_string(template, {'server': server_obj}, request=request)
                    return JsonResponse({'html_result': html_result})
                except DiscordServer.DoesNotExist:
                    return JsonResponse({'error': 'Unable to find the server.'})
            else:
                return JsonResponse({'error': 'No server ID provided.'})
        else:
            return super().get(request, *args, **kwargs)


class PaypalReturnView(generic.TemplateView):
    template_name = 'premium_paypal_return.html'


class PaypalCanceledReturnView(generic.TemplateView):
    template_name = 'premium_paypal_canceled_return.html'


# class PaypalNotifyView(generic.TemplateView):
#     template_name = 'premium_paypal_notify.html'

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         return response
