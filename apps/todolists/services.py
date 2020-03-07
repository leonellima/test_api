from .models import TodoTask
from .validators import TaskValidator


class TaskService:
    model = TodoTask

    def create(self, data):
        validator = TaskValidator(data)
        if validator.validate():
            return self.model.objects.create(**data)
        raise Exception("Invalid data")

    def list(self):
        return self.model.objects.all()

    def retrieve(self, pk):
        task = self.model.objects.filter(pk=pk).first()

        if task is None:
            raise self.model.DoesNotExist("Object doesn't exist")

        return task

    def update(self, pk, data):
        validator = TaskValidator(data)
        if validator.validate():
            task = self.model.objects.filter(pk=pk).first()
            if task is None:
                raise self.model.DoesNotExist("Object doesn't exist")
            self.model.objects.filter(pk=pk).update(**data)
            task.refresh_from_db()
            return task
        raise Exception("Invalid data")

    def delete(self, pk):
        task = self.model.objects.filter(pk=pk).first()

        if task is None:
            raise self.model.DoesNotExist("Object doesn't exist")

        task.delete()
