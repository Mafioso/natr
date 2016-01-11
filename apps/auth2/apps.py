from django.apps import AppConfig


class Auth2Config(AppConfig):
    name = 'auth2'

    def ready(self):
        NatrUser = self.get_model('NatrUser')
        NatrUser.test_cascade()  # check that cascade is working
        # watson.register(Product.objects.exclude(productimage=None))