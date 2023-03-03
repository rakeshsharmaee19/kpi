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
from django.urls import path,include
from . import views

urlpatterns = [
  path('assignWorkForce/', views.AssignWorkForce.as_view(), name='AssignWorkForce'),
  path('getWorkForce/<int:project_id>/', views.AssignWorkForce.as_view(), name='GetWorkForce'),
  path('getManager/', views.GetManager.as_view(), name='GetManager'),
  path('getOtherEmployee/<int:project_id>/', views.GetOtherEmployee.as_view(), name='GetOtherEmployee'),
  path('GetOtherKPI/<int:project_id>/', views.GetOtherKPI.as_view(), name='GetOtherKPI'),
  path('removeEmployee/<int:project_id>/<int:emp_id>/', views.AssignWorkForce.as_view(), name='RemoveEmployee'),
  path('project/<int:pk>/', views.AddProject.as_view(), name='assignManager'),
  path('project', views.AddProject.as_view(), name='addProject'),
  path('singleProject/<int:pk>/', views.SingleProject.as_view(), name='SingleProject'),
  path('assignKpi/', views.AssignKpi.as_view(), name='AssignKpi'),
  path('getAllKpi/', views.GetAllKpi.as_view(), name='GetAllKpi'),
  path('rolesList/', views.RolesList.as_view(), name='RolesList'),
  path('leadProject/<int:pk>/', views.LeadProject.as_view(), name='leadProject'),
  path('removeKpiProject/<int:project_id>/<int:kpi_id>/', views.AssignKpi.as_view(), name='RemoveKpiProject'),
  path('getsprintdetails/<int:project_id>/', views.GetSprintDetails.as_view(), name='GetSprintDetails'),
  path('kpis/<int:project_id>/', views.ProjectKPIList.as_view(), name='project_kpis'),
  path('getemployesundermanager/<int:project_manager_id>/', views.GetEmployeesUnderManager.as_view(), name='GetEmployeesUnderManager'),
  path('sprint_isactive/<int:sprint_id>/', views.sprint_isactive.as_view(), name='sprint_isactive'),

]
