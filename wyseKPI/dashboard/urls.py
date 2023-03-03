"""WyseKPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from dashboard import views


urlpatterns = [
    path("getEmployeeRating/<int:emp_id>/<int:project_id>/", views.EmployeeRating.as_view(), name='employee_rating'),
    path(
        "getEmployeeRating/<int:emp_id>/<int:project_id>/<int:from_sprint>/<int:to_sprint>/",
        views.EmployeeRating.as_view(),
        name='employee_rating_filter'
    ),
    path("getEmployeeAggRating/<int:emp_id>/<int:project_id>/", views.EmployeeAggregateRating.as_view(), name='employee_agg_rating'),
    path(
        "getEmployeeAggRating/<int:emp_id>/<int:project_id>/<int:from_sprint>/<int:to_sprint>/",
        views.EmployeeAggregateRating.as_view(),
        name='employee_agg_rating_filter'
    ),
    path("getMultiEmployeeAggRating/<int:project_id>/", views.MultipleEmployeesAggregateRating.as_view(), name='multi_employee_agg_rating'),
    path(
        "getMultiEmployeeAggRating/<int:project_id>/<int:from_sprint>/<int:to_sprint>/",
        views.MultipleEmployeesAggregateRating.as_view(),
        name='multi_employee_agg_rating_filter'
    ),
    path("getEmployeeSelfRating/<int:emp_id>/<int:project_id>/", views.EmployeeSelfRating.as_view(), name='employee_self_rating'),
    path(
        "getEmployeeSelfRating/<int:emp_id>/<int:project_id>/<int:from_sprint>/<int:to_sprint>/",
        views.EmployeeSelfRating.as_view(),
        name='employee_self_rating_filter'
    ),
    path("getEmployeeSelfAggRating/<int:emp_id>/<int:project_id>/", views.EmployeeSelfAggregateRating.as_view(), name='employee_self_agg_rating'),
    path(
        "getEmployeeSelfAggRating/<int:emp_id>/<int:project_id>/<int:from_sprint>/<int:to_sprint>/",
        views.EmployeeSelfAggregateRating.as_view(),
        name='employee_self_agg_rating_filter'
    ),
    path("getemployeesdetails/<int:emp_id>/", views.EmployeeDetails.as_view()),
    # path("saveemployeenotes/",SaveEmployeeNotes.as_view()),
    path("getprojectslist/", views.ProjectsList.as_view()),
    # path("getkpiprojectrating/<int:emp_id>/<int:project_id>/",KpiRatings.as_view()),
    path("getprojectsundermanager/<int:project_manager_id>/", views.ProjectsUnderManager.as_view()),
    path("getprojectforemployee/<int:emp_id>/", views.ProjectToEmployee.as_view()),
    # path("weightedrating/<int:project_id>/<int:emp_id>/",WeightedRating.as_view()),
    path("getallemployees/", views.AllEmployees.as_view()),
    path("getCompletedSprints/<int:project_id>/", views.CompletedSprintList.as_view()),
]
