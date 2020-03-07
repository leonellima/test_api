import serpy


class TaskSerializer(serpy.Serializer):
    id = serpy.IntField()
    description = serpy.Field()
    created_at = serpy.Field()
    finished_at = serpy.Field()
    is_finished = serpy.BoolField()

