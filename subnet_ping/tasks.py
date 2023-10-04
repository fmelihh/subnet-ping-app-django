from netaddr import IPNetwork
from celery import shared_task
from django.core.cache import cache

from .utils import ping
from .models import SubnetPingInfo


@shared_task
def ping_task(ip: str, subnet_mask: int):
    ip_subnet_mask = f"{ip}/{subnet_mask}"

    responses = []

    for sub_ip in IPNetwork(ip_subnet_mask):

        responses.append(
            {
                "requested_ip": str(sub_ip),
                "destination": ip_subnet_mask,
                "type": "IPv4" if sub_ip.info["IPv4"] else "IPv6",
                "status": ping(ip_addr=str(sub_ip)),
            }
        )

    cache.set(ip_subnet_mask, responses, 60*60*2)
    SubnetPingInfo.objects.bulk_create(
        [SubnetPingInfo(**response) for response in responses]
    )
