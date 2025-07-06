from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving, creating, updating,
    deleting and liking/unliking posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # Read‑only for anonymous; owner only for edits
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Hook to set the post's owner to the current user.
        """
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='like',
        url_name='Like Post'
    )
    def toggle_like(self, request, pk=None):
        """
        POST /posts/{pk}/like/
        - If not liked yet: creates a Like and returns 201 + the like data
        - If already liked: deletes the Like and returns 204 No Content
        """
        post = self.get_object()
        like, created = Like.objects.get_or_create(author=request.user, post=post)

        if not created:
            # already liked → unlike
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # newly liked → return the like record
        serializer = LikeSerializer(like, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
