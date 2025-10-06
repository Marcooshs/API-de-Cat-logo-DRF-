from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from catalog.views import CategoryViewSet, ProductViewSet
from orders.views import OrderViewSet

def healthz(_request):
    return JsonResponse({"status": "ok"})


# Catálogo — com barra final (ex.: /api/catalog/products/)
router_catalog = DefaultRouter()  # trailing slash ON (default)
router_catalog.register(r'catalog/categories', CategoryViewSet, basename= 'category')
router_catalog.register(r'catalog/products', ProductViewSet, basename= 'product')

# Pedidos — sem barra final (ex.: /api/orders/me/cart/add-item)
router_orders = DefaultRouter(trailing_slash= False)  # trailing slash OFF
router_orders.register(r'orders', OrderViewSet, basename= 'order')

urlpatterns = [
    path('api/', include(router_catalog.urls)),
    path('api/', include(router_orders.urls)),

    # Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),

    # Admin
    path('admin/', admin.site.urls),
    path("healthz/", healthz),

    # Docs
    path('api/schema/', SpectacularAPIView.as_view(), name= 'schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name= 'schema'), name= 'swagger-ui'),

    path("healthz/", lambda r: JsonResponse({"status": "ok"})),
]
