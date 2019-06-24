# views.py
class ChangePasswordView(UpdateAPIView):
    model = CustomUser
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"status": "Password is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                MinimumLengthValidator().validate(serializer.data.get("new_password"))
                CommonPasswordValidator().validate(serializer.data.get("new_password"))
                NumericPasswordValidator().validate(serializer.data.get("new_password"))
            except ValidationError as e:
                return Response({"status": e}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"status": "Success."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# serializers.py
class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# urls.py
urlpatterns += [
    path(r'change-password/', ChangePasswordView.as_view())
]

