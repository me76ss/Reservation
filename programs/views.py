from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Program, ProgramSlot, ProgramSlotRecord, ProgramSlotType
from .serializers import ProgramSerializer, ProgramDetailSerializer, ProgramSlotRecordSerializer


class ProgramList(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        programs = Program.objects.filter(ends_at__gte=timezone.now())
        return Response(ProgramSerializer(programs, many=True).data)


class ProgramDetail(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk):
        program = Program.objects.filter(pk=pk).prefetch_related('slots__records').get()
        return Response(ProgramDetailSerializer(program).data)


class ProgramSlotDetail(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request, pg_pk, sl_pk):
        if ProgramSlotRecord.objects.filter(user=request.user, slot__program_id=pg_pk).exists():
            return Response(data={'message': 'Already reserved a slot in this program'},
                            status=status.HTTP_417_EXPECTATION_FAILED)

        # TODO: check capacity of the slot
        record = ProgramSlotRecord.objects.create(type=ProgramSlotType.RESERVE.name, participated=False,
                                                  slot_id=sl_pk, user=request.user)
        return Response(ProgramSlotRecordSerializer(record).data)


class UserReserveList(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        records = ProgramSlotRecord.objects.filter(user=request.user).prefetch_related('slot__program')

        return Response(ProgramSlotRecordSerializer(records, many=True).data)
