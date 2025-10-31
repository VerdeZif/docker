from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.mail import send_mail
from .models import ContactMessage, NotificationLog   # <-- IMPORTANTE
from .serializers import ContactMessageSerializer
from .tasks import send_email_task

class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = ContactMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        send_mail(
            "Nuevo mensaje de contacto",
            message.message,
            message.email,
            ["admin@mysite.com"],
            fail_silently=True
        )

        return Response({"status": "queued"}, status=status.HTTP_201_CREATED)


class NotifyViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data

        # Guardar registro en DB
        NotificationLog.objects.create(**data)

        # Enviar email en background
        send_email_task.delay(
            subject=data["subject"],
            body=data["body"],
            to=data["to"]
        )

        return Response({"status": "queued"})
