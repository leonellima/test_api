from rest_framework import routers

from apps.todolists.views import TodoTaskView

router = routers.DefaultRouter()
router.register(r'tasks', TodoTaskView, basename='tasks')

urlpatterns = router.urls
