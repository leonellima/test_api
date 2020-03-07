from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import TaskSerializer
from .services import TaskService


class TodoTaskView(GenericViewSet):

    def create(self, request):
        service = TaskService()
        try:
            task_created = service.create(request.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(
            TaskSerializer(task_created, many=False).data,
            status=status.HTTP_201_CREATED
        )

    def list(self, request):
        service = TaskService()
        try:
            data = service.list()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(
            TaskSerializer(data, many=True).data,
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        service = TaskService()
        try:
            task = service.retrieve(pk)
        except TaskService.model.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(
            TaskSerializer(task, many=False).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        service = TaskService()
        try:
            task_updated = service.update(pk, request.data)
        except TaskService.model.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(
            TaskSerializer(task_updated, many=False).data,
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        service = TaskService()
        try:
            service.delete(pk)
        except TaskService.model.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response("Task Deleted", status=status.HTTP_204_NO_CONTENT)
