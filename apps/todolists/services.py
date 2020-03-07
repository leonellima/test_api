from .models import TodoTask
from .validators import TaskValidator


class TaskService:
    model = TodoTask

    def get_object(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def update_object(self, pk, data):
        self.model.objects.filter(pk=pk).update(**data)
        return self.model.objects.filter(pk=pk).first()

    def create(self, data):
        validator = TaskValidator(data)
        if validator.validate():
            return self.model.objects.create(**data)
        raise Exception("Invalid data")

    def list(self):
        return self.model.objects.all()

    def retrieve(self, pk):
        task = self.get_object(pk)

        if task is None:
            raise self.model.DoesNotExist("Object doesn't exist")

        return task

    def update(self, pk, data):
        task = self.get_object(pk)
        if task is None:
            raise self.model.DoesNotExist("Object doesn't exist")
        return self.update_object(pk, data)

    def delete(self, pk):
        task = self.get_object(pk)

        if task is None:
            raise self.model.DoesNotExist("Object doesn't exist")

        task.delete()
