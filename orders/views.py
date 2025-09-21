from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Order, OrderItem
from .serializers import OrderSerializer, AdminOrderSerializer
from .permissions import IsOwnerOrAdmin
from catalog.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Admin pode alterar/destruir; demais ações exigem usuário autenticado e dono
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user= self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff and self.action in ['update', 'partial_update']:
            return AdminOrderSerializer
        return OrderSerializer

    # ===== Carrinho =====
    @staticmethod
    def _get_or_create_cart(user):
        cart, _ = Order.objects.get_or_create(user= user, status= Order.Status.CART)
        return cart

    @action(detail=False, methods=['get'], url_path= 'me/cart')
    def my_cart(self, request):
        cart = self._get_or_create_cart(request.user)
        return Response(OrderSerializer(cart).data)

    @action(detail=False, methods=['post'], url_path= 'me/cart/add-item')
    def add_item(self, request):
        product_id = request.data.get('product_id')
        qty = int(request.data.get('quantity', 1))
        if not product_id or qty <= 0:
            return Response({'detail': 'product_id e quantity (>0) são obrigatórios.'}, status= 400)

        cart = self._get_or_create_cart(request.user)
        product = get_object_or_404(Product, pk= product_id, is_active= True)

        item, created = OrderItem.objects.get_or_create(
            order=cart, product=product, defaults={'quantity': qty, 'unit_price': product.price}
        )
        if not created:
            item.quantity += qty
            item.save(update_fields=['quantity'])

        cart.recalc_total()
        return Response(OrderSerializer(cart).data, status= status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path= 'me/cart/set-item')
    def set_item(self, request):
        product_id = request.data.get('product_id')
        qty = int(request.data.get('quantity', 0))
        if not product_id:
            return Response({'detail': 'product_id é obrigatório.'}, status= 400)

        cart = self._get_or_create_cart(request.user)
        item = OrderItem.objects.filter(order= cart, product_id= product_id).first()

        if qty <= 0:
            if item:
                item.delete()
                cart.recalc_total()
            return Response(OrderSerializer(cart).data)

        product = get_object_or_404(Product, pk= product_id, is_active= True)
        if item:
            item.quantity = qty
            item.save(update_fields=['quantity'])
        else:
            OrderItem.objects.create(order= cart, product= product, quantity= qty, unit_price= product.price)

        cart.recalc_total()
        return Response(OrderSerializer(cart).data)

    @action(detail= False, methods=['post'], url_path= 'me/cart/remove-item')
    def remove_item(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'detail': 'product_id é obrigatório.'}, status= 400)

        cart = self._get_or_create_cart(request.user)
        deleted, _ = OrderItem.objects.filter(order= cart, product_id= product_id).delete()
        cart.recalc_total()
        return Response({'removed': bool(deleted), 'cart': OrderSerializer(cart).data})

    @action(detail= False, methods=['post'], url_path= 'me/cart/checkout')
    def checkout(self, request):
        address = (request.data.get('shipping_address') or '').strip()
        if not address:
            return Response({'detail': 'shipping_address é obrigatório.'}, status= 400)

        cart = self._get_or_create_cart(request.user)
        if cart.items.count() == 0:
            return Response({'detail': 'Carrinho vazio.'}, status= 400)

        with transaction.atomic():
            product_ids = list(cart.items.values_list('product_id', flat= True))
            products = {p.id: p for p in Product.objects.select_for_update().filter(id__in= product_ids)}

            for item in cart.items.select_related('product'):
                prod = products[item.product_id]
                if item.quantity > prod.stock:
                    return Response(
                        {'detail': f'Estoque insuficiente para {prod.name}. Disponível: {prod.stock}.'},
                        status=400,
                    )

            for item in cart.items.all():
                prod = products[item.product_id]
                prod.stock -= item.quantity
                prod.save(update_fields=['stock'])

            cart.shipping_address = address
            cart.status = Order.Status.PENDING
            cart.recalc_total(save= False)
            cart.save(update_fields=['shipping_address', 'status', 'total_amount', 'updated_at'])

        return Response(OrderSerializer(cart).data, status= 200)
