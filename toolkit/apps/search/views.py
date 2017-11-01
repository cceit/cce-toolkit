from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from .models import SearchFilter
from rest_framework import generics, serializers, permissions
from rest_framework.exceptions import ValidationError


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

    def get_queryset(self):
        return SearchFilter.objects.filter(view=self.request.GET['view_name']).filter(
            Q(user=self.request.user) | Q(visibility=SearchFilter.PUBLIC))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            if isinstance(exc.detail, (list, dict)):
                data = exc.detail
            else:
                data = {'detail': exc.detail}
            return JsonResponse(data)
        self.perform_create(serializer)
        # Instead of returning DRF's Response here, just reload the page
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class SearchFilterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SearchFilter.objects.all()
    serializer_class = SearchFilterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrPublic)
