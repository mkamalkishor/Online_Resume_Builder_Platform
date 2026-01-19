from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ REQUIRED
    path('', include('resume_builder.urls')),
]
