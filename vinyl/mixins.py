class GetObjectMixin[T]:
    model: type[T]

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None
