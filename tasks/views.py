from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer, TaskMoveSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        selected_date = self.request.query_params.get('date')

        if selected_date:
            queryset = queryset.filter(task_date=selected_date)

        return queryset.order_by('order', 'created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='date',
                description='Filter tasks by selected Kanban board date. Format: YYYY-MM-DD',
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=TaskMoveSerializer,
        responses={200: TaskSerializer},
    )
    @action(detail=True, methods=['patch'])
    def move(self, request, pk=None):
        task = self.get_object()

        serializer = TaskMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task.status = serializer.validated_data['status']
        task.order = serializer.validated_data['order']
        task.save()

        response_serializer = TaskSerializer(task)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )