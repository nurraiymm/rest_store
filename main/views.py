from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, viewsets
from main.models import Product, Comment, Like
from .serializers import ProductDetailsSerializer, CommentSerializer, LikeSerializer
from .permisssions import ProductPermission, IsCommentAuthor


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super(CustomSearchFilter, self).get_search_fields(view, request)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    filterset_class = ProductFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [ProductPermission, ]
        return [permission() for permission in permissions]

    @action(detail=True, methods=['POST'])
    def like(self, request, *args, **kwargs):
        product = self.get_object()
        like_obj, _ = Like.objects.get_or_create(product=product, user=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})




class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ProductPermission, ]
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsCommentAuthor, ]
        return [permission() for permission in permissions]

# class AddStarRatingView(APIView):
#     "добавление рейтинга продукту"
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)

