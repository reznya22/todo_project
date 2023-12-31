from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, UserLogin, RegisterPage
from django.contrib.auth.views import LogoutView

app_name = "base"


urlpatterns = [
    path('', TaskList.as_view(), name="task"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task/<int:pk>/', TaskDetail.as_view(), name="task-detail"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='base:login'), name="logout"),
    path('register/', RegisterPage.as_view(), name="register"),

]
