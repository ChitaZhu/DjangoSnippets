from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from news.models import Reporter, Article
from news.serializer import ReporterSerializer, ArticleSerializer


class ReporterViewSet(generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = Reporter.objects.all()
    serializer_class = ReporterSerializer
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save()

    def put(self, request, *args, **kwargs):
        setattr(self, 'kwargs', request.data)
        return self.update(request, *args, **kwargs)


class ArticleViewSet(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super(ArticleViewSet, self).get_serializer(*args, **kwargs)