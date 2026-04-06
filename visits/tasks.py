from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_visit_request_email(visit_id):
    """Notify owner when seeker sends a visit request"""
    from visits.models import VisitRequest
    visit = VisitRequest.objects.get(id=visit_id)

    send_mail(
        subject = f'New visit request — {visit.listing.title}',
        message = f"""
Hi {visit.listing.owner.username},

{visit.seeker.username} has requested a visit for your listing "{visit.listing.title}".

Date    : {visit.date}
Time    : {visit.time}
Message : {visit.message or 'No message provided'}

Log in to accept or decline this request.
        """,
        from_email     = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [visit.listing.owner.email],
    )
    return f"Visit request email sent for visit #{visit_id}"


@shared_task
def send_visit_accepted_email(visit_id):
    """Notify seeker when owner accepts their visit request"""
    from visits.models import VisitRequest
    visit = VisitRequest.objects.get(id=visit_id)

    send_mail(
        subject = f'Your visit request has been accepted! — {visit.listing.title}',
        message = f"""
Hi {visit.seeker.username},

Great news! Your visit request for "{visit.listing.title}" has been accepted.

Date    : {visit.date}
Time    : {visit.time}
Address : {visit.listing.address}, {visit.listing.city}
Owner   : {visit.listing.owner.username}

See you there!
        """,
        from_email     = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [visit.seeker.email],
    )
    return f"Visit accepted email sent for visit #{visit_id}"


@shared_task
def send_visit_declined_email(visit_id):
    """Notify seeker when owner declines their visit request"""
    from visits.models import VisitRequest
    visit = VisitRequest.objects.get(id=visit_id)

    send_mail(
        subject = f'Your visit request was declined — {visit.listing.title}',
        message = f"""
Hi {visit.seeker.username},

Unfortunately, your visit request for "{visit.listing.title}" has been declined.

You can browse other listings on RoomieMatch and send new requests.
        """,
        from_email     = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [visit.seeker.email],
    )
    return f"Visit declined email sent for visit #{visit_id}"


@shared_task
def send_new_message_email(message_id):
    """Notify recipient when they receive a new message"""
    from messaging.models import Message
    message     = Message.objects.get(id=message_id)
    recipient   = message.conversation.get_other_user(message.sender)

    send_mail(
        subject = f'New message from {message.sender.username}',
        message = f"""
Hi {recipient.username},

You have a new message from {message.sender.username}:

"{message.content}"

Log in to reply.
        """,
        from_email     = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [recipient.email],
    )
    return f"New message email sent for message #{message_id}"


@shared_task
def send_listing_created_email(listing_id):
    """Notify owner when their listing is created"""
    from listings.models import Listing
    listing = Listing.objects.get(id=listing_id)

    send_mail(
        subject = f'Your listing is live — {listing.title}',
        message = f"""
Hi {listing.owner.username},

Your listing "{listing.title}" is now live on RoomieMatch!

City  : {listing.city}
Price : {listing.price}€/month
Size  : {listing.size}m²

Seekers can now find and contact you.
        """,
        from_email     = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [listing.owner.email],
    )
    return f"Listing created email sent for listing #{listing_id}"