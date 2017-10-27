from django.contrib.auth.models import User
from .models import SearchFilter
from rest_framework import generics, serializers, permissions


class IsOwnerOrPublic(permissions.BasePermission):
    """
    Custom permission to only allow read actions on public or owned objects,
    and to only allow write actions on owned objects.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to the owner of the object or if the object is public.
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user or obj.visibility == SearchFilter.PUBLIC

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class SearchFilterSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SearchFilter
        fields = ('id', 'name', 'user', 'visibility', 'query_string', 'view')


class UserSerializer(serializers.ModelSerializer):
    search_filters = serializers.PrimaryKeyRelatedField(many=True, queryset=SearchFilter.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


class SearchFilterList(generics.ListCreateAPIView):
    queryset = SearchFilter.objects.all()
    serializer_class = SearchFilterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrPublic)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchFilterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SearchFilter.objects.all()
    serializer_class = SearchFilterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrPublic)


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
