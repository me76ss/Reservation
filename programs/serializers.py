from rest_framework import serializers

from .models import Program, ProgramSlot, ProgramSlotType


class ProgramSlotSerializer(serializers.ModelSerializer):
    reserve = serializers.SerializerMethodField()
    waiting = serializers.SerializerMethodField()

    def get_reserve(self, instance):
        return instance.records.filter(type=ProgramSlotType.RESERVE).count()

    def get_waiting(self, instance):
        return instance.records.filter(type=ProgramSlotType.WAITING).count()

    class Meta:
        model = ProgramSlot
        fields = ["id", "starts_at", "ends_at", "capacity", "reserve", "waiting"]


class ProgramDetailSerializer(serializers.ModelSerializer):
    slots = ProgramSlotSerializer(many=True)

    class Meta:
        model = Program
        fields = ["id", "name", "starts_at", "ends_at", "notify_at", "queueable", "cancel_threshold", "slots"]


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "name", "starts_at", "ends_at", "notify_at", "queueable", "cancel_threshold"]
