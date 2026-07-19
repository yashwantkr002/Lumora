import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.forms.chat.message_form import MessageForm
from app.models.message import Message
from .detail import DetailConversationService

logger = logging.getLogger(__name__)


class MessageService:
    """
    Handles message operations.
    """

    @staticmethod
    def send_message(conversation, sender, content):
        """
        Create a new text message.
        """

        return Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content,
            message_type=Message.TEXT,
        )

    @staticmethod
    def get_messages(conversation):
        """
        Return messages for a conversation.
        """

        return (
            Message.objects.filter(
                conversation=conversation,
            )
            .select_related("sender")
            .order_by("created_at")
        )


@login_required
def messages_view(request, conversation_id):
    """
    Display and send messages.
    """

    try:

        conversation = (
            DetailConversationService.get_conversation(
                conversation_id,
            )
        )

    except Exception:

        messages.error(
            request,
            "Conversation not found.",
        )

        return redirect(
            "conversations",
        )

    if request.method == "POST":

        form = MessageForm(
            request.POST,
        )

        if form.is_valid():

            try:

                MessageService.send_message(
                    conversation=conversation,
                    sender=request.user,
                    content=form.cleaned_data["content"],
                )

                messages.success(
                    request,
                    "Message sent.",
                )

                return redirect(
                    "messages",
                    conversation_id=conversation.id,
                )

            except Exception:

                logger.exception(
                    "Failed to send message.",
                    extra={
                        "conversation_id": conversation.id,
                        "user_id": request.user.id,
                    },
                )

                messages.error(
                    request,
                    "Unable to send message.",
                )

    else:

        form = MessageForm()

    chat_messages = (
        MessageService.get_messages(
            conversation,
        )
    )

    return render(
        request,
        "chat/messages.html",
        {
            "conversation": conversation,
            "messages": chat_messages,
            "form": form,
        },
    )