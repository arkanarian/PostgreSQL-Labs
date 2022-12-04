from rest_framework import mixins
from rest_framework import viewsets

from web.serializers import ListQuerySerializer
from web.models import Queries

class QueriesViewSetListCreate(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    serializer_class = ListQuerySerializer
    queryset = Queries.objects.all()

class QueriesViewSet(
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):

    serializer_classes = {
        'retrieve': ListQuerySerializer,
        # 'partial_update': UpdatePageSerializer,
    }
    queryset = Queries.objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes.get(self.action)
        return ListQuerySerializer

    # def retrieve(self, request, *args, **kwargs):
    #     pass