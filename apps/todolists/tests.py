import datetime
import json

from django.urls import reverse

from django_mock_queries.query import MockSet
import pytest
from rest_framework import status

from apps.todolists.models import TodoTask
from apps.todolists.serializers import TaskSerializer
from apps.todolists.services import TaskService
from apps.todolists.views import TodoTaskView


class TestTaskSerializer:
    def test_expected_serialized_json(self):
        expected_results = {
            'id': 1,
            'description': 'Sacar Basura',
            'created_at': str(datetime.datetime.now()),
            'is_finished': False,
            'finished_at': None
        }

        task = TodoTask(**expected_results)
        results = TaskSerializer(task).data
        assert results == expected_results


class TestViewSet:
    @pytest.mark.urls('todolists.urls')
    def test_list(self, rf, mocker):
        url = reverse('tasks-list')
        request = rf.get(url)

        # Crear un Mock de nuestro queryset y omitir el acceso a BD
        queryset = MockSet(
            TodoTask(
                id=1,
                description='Pasear el perro',
                is_finished=False,
                created_at=datetime.datetime.now()),
            TodoTask(
                id=2,
                description='Dar de comer al gato',
                is_finished=True,
                created_at=datetime.datetime.now())
        )

        # Sustituye el metodo list de TaskService.
        # Solo se prueba el metodo list de ViewSet
        mocker.patch.object(
            TaskService, 'list', return_value=queryset)
        response = TodoTaskView.as_view({'get': 'list'})(request).render()

        # Verifica que existen 2 resultados
        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 2

    @pytest.mark.urls('todolists.urls')
    def test_create(self, rf, mocker):
        url = reverse('tasks-list')

        data = {
            'id': 1,
            'description': 'Arreglar la cama',
            'is_finished': False,
            'finished_at': None
        }

        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(data))

        mocker.patch.object(TodoTask, 'save')
        response = TodoTaskView.as_view({'post': 'create'})(request).render()

        # Verificado que se ha creado el objeto
        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.content).get('description') == 'Arreglar la cama'
        # Verificamos si efectivamente se llamo el metodo save
        assert TodoTask.save.called

    # @pytest.mark.urls('todolists.urls')
    # def test_update(self, rf, mocker):
    #     url = reverse('tasks-detail', kwargs={'pk': 1})
    #     request = rf.patch(
    #         url,
    #         content_type='application/json',
    #         data=json.dumps({'description': 'Mejor cambiar fundas'}))

    #     task = TodoTask(
    #         description='Cambiar sabanas',
    #         id=1,
    #         is_finished=True,
    #         created_at=datetime.datetime.now())

    #     # Patch al metodo get_object de nuestro ViewSet para
    #     # para omitir el acceso a BD
    #     # Lo mismo para el motodo save() de nuestro modelo Car
    #     mocker.patch.object(TaskService, 'get_object', return_value=task)
    #     mocker.patch.object(TodoTask, 'save')

    #     response = TodoTaskView.as_view({'patch': 'partial_update'})(request).render()

    #     assert response.status_code == 200
    #     assert json.loads(response.content).get('description') == 'Mejor cambiar fundas'
    #     assert TodoTask.save.called

    @pytest.mark.urls('todolists.urls')
    def test_delete(self, rf, mocker):
        url = reverse('tasks-detail', kwargs={'pk': 1})
        request = rf.delete(url)

        task = TodoTask(
            id=1,
            description='Reparar mueble',
            created_at=datetime.datetime.now(),
            is_finished=False)

        # De nuevo hacemos patch al metodo get_object
        # y tambien al delete del objeto.
        mocker.patch.object(TaskService, 'get_object', return_value=task)
        mocker.patch.object(TodoTask, 'delete')

        response = TodoTaskView.as_view({'delete': 'destroy'})(request).render()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert TodoTask.delete.called
