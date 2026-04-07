from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Conversation, Message
from visits.tasks import send_new_message_email

User = get_user_model()

@login_required
def inbox(request):
    """List all conversations"""
    conversations = request.user.conversations.prefetch_related(
        'participants', 'messages', 'listing'
    )
    
    for conversation in conversations:
        conversation.other_user = conversation.get_other_user(request.user)
        
    return render(request, 'messaging/inbox.html', {
        'conversations': conversations,
    })
@login_required
def conversation_detail(request, pk):
    """View a conversation and send messages"""
    conversation = get_object_or_404(
        Conversation,
        pk           = pk,
        participants = request.user
    )

    # Mark messages as read
    conversation.messages.exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                conversation = conversation,
                sender       = request.user,
                content      = content,
            )
            conversation.save()
            send_new_message_email.delay(message.id)

            # If htmx req return only the new message
            if request.htmx:
                return render(request, 'messaging/partials/message.html', {
                    'message': message,
                })

        return redirect('messaging:conversation', pk=pk)

    messages_qs = conversation.messages.select_related('sender')
    return render(request, 'messaging/conversation.html', {
        'conversation': conversation,
        'messages'    : messages_qs,
        'other_user'  : conversation.get_other_user(request.user),
    })

@login_required
def start_conversation(request, user_pk):
    """Start or get existing conversation with a user"""
    other_user = get_object_or_404(User, pk=user_pk)
    listing_pk = request.GET.get('listing')

    existing = Conversation.objects.filter(
        participants = request.user
    ).filter(
        participants = other_user
    ).first()

    if existing:
        return redirect('messaging:conversation', pk=existing.pk)

    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)

    if listing_pk:
        from listings.models import Listing
        try:
            conversation.listing = Listing.objects.get(pk=listing_pk)
            conversation.save()
            send_new_message_email.delay(message.id)
        except Listing.DoesNotExist:
            pass

    return redirect('messaging:conversation', pk=conversation.pk)

@login_required
def unread_count(request):
    """Return unread messages count — used by HTMX polling"""
    count = Message.objects.filter(
        conversation__participants = request.user,
        is_read                   = False,
    ).exclude(sender=request.user).count()

    return HttpResponse(str(count) if count > 0 else '')