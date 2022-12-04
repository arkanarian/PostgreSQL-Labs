from rest_framework import routers

from web import views

router = routers.SimpleRouter()
router.register(r'base', views.QueriesViewSet)
router.register(r'base', views.QueriesViewSetListCreate)
urlpatterns = router.urls