from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Program
from .serializers import ProgramSerializer, ProgramDetailSerializer


class ProgramList(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        programs = Program.objects.filter(ends_at__gte=timezone.now())
        return Response(ProgramSerializer(programs, many=True).data)


class ProgramDetail(APIView):
    # permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk):
        programs = Program.objects.filter(pk=pk).prefetch_related('slots__records').get()
        return Response(ProgramDetailSerializer(programs).data)
