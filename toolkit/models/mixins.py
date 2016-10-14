

class ModelPermissionsMixin(object):
    """
    Defines the permissions methods that most models need,

    :raises NotImplementedError: if they have not been overridden.
    """
    @classmethod
    def can_create(cls, user_obj):
        """
        CreateView needs permissions at class (table) level.
        We'll try it at instance level for a while and see how it goes.
        """
        raise NotImplementedError

    @classmethod
    def can_view_list(cls, user_obj):
        """
        ListView needs permissions at class (table) level.
        We'll try it at instance level for a while and see how it goes.
        """
        raise NotImplementedError

    def can_update(self, user_obj):
        """
        UpdateView needs permissions at instance (row) level.
        """
        raise NotImplementedError

    def can_view(self, user_obj):
        """
        DetailView needs permissions at instance (row) level.
        """
        raise NotImplementedError

    def can_delete(self, user_obj):
        """
        DeleteView needs permissions at instance (row) level.
        """
        raise NotImplementedError
