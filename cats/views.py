from rest_framework import viewsets, status
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer
from rest_framework.response import Response

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Mission.objects.filter(cat=instance).exists():
            return Response({"error": "Cannot delete cat assigned to an active mission."}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def update(self, request, *args, **kwargs):
            instance = self.get_object()

            if Mission.objects.filter(cat=instance).exists():
                return Response({"error": "Cannot update cat assigned to an active mission."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.complete:
            return Response({"error": "Cannot update completed mission."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)