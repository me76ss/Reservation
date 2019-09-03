from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Program, ProgramSlotRecord, ProgramSlotType, ProgramSlot
from .serializers import ProgramDetailSerializer, ProgramSlotRecordSerializer


class ProgramList(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        programs = Program.objects.filter(ends_at__gte=timezone.now())
        return Response(ProgramDetailSerializer(programs, many=True).data)


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
            return Response(data={'detail': 'Already reserved a slot in this program'},
                            status=status.HTTP_417_EXPECTATION_FAILED)

        program = get_object_or_404(Program, pk=pg_pk)
        slot = get_object_or_404(ProgramSlot, pk=sl_pk)

        if timezone.now() >= slot.starts_at:
            return Response(data={'detail': 'Slot is for past'}, status=status.HTTP_417_EXPECTATION_FAILED)

        if ProgramSlotRecord.objects.filter(slot_id=sl_pk).count() >= slot.capacity:
            if program.queueable:
                record_type = ProgramSlotType.WAITING.name
            else:
                return Response(data={'detail': 'Slot is full'}, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            record_type = ProgramSlotType.RESERVE.name
        record = ProgramSlotRecord.objects.create(type=record_type, participated=False, slot_id=sl_pk,
                                                  user=request.user)
        return Response(ProgramSlotRecordSerializer(record).data)


class UserReserveList(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        records = ProgramSlotRecord.objects.filter(user=request.user).prefetch_related('slot__program')

        return Response(ProgramSlotRecordSerializer(records, many=True).data)


class UserReserveDetail(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def delete(self, request, pk):
        record = get_object_or_404(ProgramSlotRecord, id=pk)
        slot_id = record.slot_id
        if record.user_id != request.user.id:
            return Response(data={'detail': 'Not your reserve!'}, status=status.HTTP_403_FORBIDDEN)

        if not record.slot.is_allowed_to_cancel():
            return Response(data={'detail': 'Can\'t cancle it now!'}, status=status.HTTP_403_FORBIDDEN)

        record.delete()

        slot = ProgramSlot.objects.filter(pk=slot_id).prefetch_related('records').get()
        if slot.records.count() >= slot.capacity:
            reserve = slot.records.filter(type=ProgramSlotType.WAITING.name).first()
            if reserve is not None:
                reserve.type = ProgramSlotType.RESERVE.name
                reserve.save()

        return Response(data={'detail': 'Deleted'})
