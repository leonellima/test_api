import datetime
import json

from django.urls import reverse

from django_mock_queries.query import MockSet
import pytest
from rest_framework.exceptions import ValidationError

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

        # Sustituye el metodo list de TaskService
        mocker.patch.object(
            TaskService, 'list', return_value=queryset)
        response = TodoTaskView.as_view({'get': 'list'})(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2

    # @pytest.mark.urls('todolists.urls')
    # def test_create(self, rf, mocker):
    #     url = reverse('tasks-list')

    #     data = {
    #         'description': 'Arreglar la cama',
    #         'is_finished': False,
    #         'finished_at': None
    #     }

    #     request = rf.post(url,
    #                       content_type='application/json',
    #                       data=json.dumps(data))

    #     mocker.patch.object(TodoTask, 'save')
    #     # Renderizamos la vista con nuestro request.
    #     response = TodoTaskView.as_view({'post': 'create'})(request).render()

    #     assert response.status_code == 201
    #     assert json.loads(response.content).get('description') == 'Arreglar la cama'
    #     # Verificamos si efectivamente se llamo el metodo save
    #     assert TodoTask.save.called
