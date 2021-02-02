from django.urls import path

from .views import tests_view, test_detail_view, testing_view

urlpatterns = [
    path('<int:test_id>/testing/<int:question_number>', testing_view, name='testing'),
    path('<int:test_id>/', test_detail_view, name='test_detail'),
    path('', tests_view, name='tests')
]
