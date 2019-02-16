from paypal.standard.models import ST_PP_COMPLETED
from django.conf import settings
from web.apps.servers.models import DiscordServer
from django.utils import timezone
from datetime import timedelta


def process_payment(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:

        if ipn_obj.receiver_email != settings.PAYPAL_EMAIL_ACCOUNT:
            print('Not a valid payment.')
            return

        try:
            tier, sid = ipn_obj.custom.split('_')
            tier, sid = int(tier), int(sid)

        except ValueError:
            print('Custom field tampered.')
            return

        if tier == 1:
            price = 9.99
        elif tier == 2:
            price = 14.99
        else:
            print(f'Custom field tampered (no such tier [{tier}]).')
            return

        try:
            server_obj = DiscordServer.objects.get(pk=sid)
        except DiscordServer.DoesNotExist:
            print(f'Custom field tampered (no such server with id [{sid}]).')
            return

        if ipn_obj.mc_gross != price and ipn_obj.mc_currency == 'USD':
            print('Price tampered.')
            return

        server_tier = server_obj.check_premium()
        now = timezone.now()
        subscription = timedelta(days=31)

        # no tier bought or expired
        if server_tier == 0:
            server_obj.premium_tier = tier
            if tier == 1:
                server_obj.premium_1_from = now
                server_obj.premium_1_until = now + subscription
                server_obj.save()
                print('Premium Tier 1 delivered.')
            elif tier == 2:
                server_obj.premium_2_from = now
                server_obj.premium_2_until = now + subscription
                server_obj.save()
                print('Premium Tier 2 delivered.')
        # server currently has Tier 1
        elif server_tier == 1:
            if tier == 1:
                print(server_obj.premium_1_until)
                server_obj.premium_1_until += subscription
                print(server_obj.premium_1_until)
                server_obj.save()
                print('Premium Tier 1 extended.')
            # at Tier 1, so Tier 2 should never be bought, or expired
            elif tier == 2:
                time_left = server_obj.premium_1_until - now
                server_obj.premium_tier = 2
                # push premium 1 duration to the amount of subscription + time left
                # so it will continue as tier 1 when tier 2 expires
                server_obj.premium_2_from = now
                server_obj.premium_2_until = now + subscription
                server_obj.premium_1_from = server_obj.premium_2_until
                server_obj.premium_1_until = server_obj.premium_2_until + time_left
                server_obj.save()
                print('Premium Tier 1 pushed, Premium Tier 2 delivered.')
        # server currently has Tier 2, Tier 1 may have time left, or expired, or never been bought
        elif server_tier == 2:

            if tier == 1:
                if server_obj.tier_1_expired():
                    server_obj.premium_1_from = server_obj.premium_2_until
                    server_obj.premium_1_until = server_obj.premium_2_until + subscription
                    server_obj.save()
                    print('Premium Tier 1 delivered, Premium Tier 2 unchanged.')
                else:
                    server_obj.premium_1_from = server_obj.premium_2_until
                    server_obj.premium_1_until += subscription
                    server_obj.save()
                    print('Premium Tier 1 extended, Premium Tier 2 unchanged.')

            elif tier == 2:

                if server_obj.tier_1_expired():
                    server_obj.premium_2_until += subscription
                    server_obj.save()
                    print('Premium Tier 2 extended. No Tier 1.')
                else:
                    time_left = server_obj.premium_1_until - server_obj.premium_1_from
                    server_obj.premium_2_until += subscription
                    server_obj.premium_1_from = server_obj.premium_2_until
                    server_obj.premium_1_until = server_obj.premium_2_until + time_left
                    server_obj.save()
                    print('Premium Tier 2 extended. Tier 1 changed.')

        else:
            print('Unable to parse Current Tier and Buying Tier.')

    else:
        print('Incomplete Payment.')
        return
