class GetObjectMixin[T]:
    def get_object(self, pk):
        try:
            return T.objects.get(pk=pk)
        except T.DoesNotExist:
            return None
