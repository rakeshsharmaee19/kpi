from django.contrib import admin
from .models import (
    Employee,
    Project,
    KPI,
    KPIProject,
    KPIRating,
    Workforce,
    Roles,
    AggregateRating,
    Sprint,
    SystemRole

)

# Register your models here.


admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(KPI)
admin.site.register(KPIProject)
admin.site.register(KPIRating)
admin.site.register(Workforce)
admin.site.register(Roles)
admin.site.register(AggregateRating)
admin.site.register(Sprint)
admin.site.register(SystemRole)

