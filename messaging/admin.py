from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model   = Message
    extra   = 0
    readonly_fields = ['sender', 'content', 'created_at', 'is_read']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'listing', 'updated_at']
    inlines      = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'content', 'is_read', 'created_at']
    list_filter  = ['is_read']