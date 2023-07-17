from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from catalog.auth import AuthMixin
from catalog.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order


class OrderCreateView(AuthMixin, View):
    required_perms = ['BOOKS_SHOP']
    forbidden_url = reverse_lazy('login')

    def post(self, request):
        cart = Cart(request)

        if len(cart) == 0:
            return redirect('books')

        form = OrderCreateForm(
            request.POST,
            instance=Order(
                user=self.auth.user
            )
        )
        if form.is_valid():
            order = form.save()
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item['book'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect('order_list')

    def get(self, request):
        cart = Cart(request)

        if len(cart) == 0:
            return redirect('books')

        user = self.auth.user
        user_name = user.name.split(' ')
        if len(user_name) < 2:
            user_name.append('')

        form = OrderCreateForm(initial={
            'first_name': user_name[0],
            'last_name': user_name[1],
            'email': user.email
        })

        return render(request, 'orders/order/create.html', {
            'cart': cart,
            'form': form,
            **self.get_context_data()
        })


class OrderListView(AuthMixin, View):
    required_perms = ['BOOKS_SHOP']
    forbidden_url = reverse_lazy('login')

    def get(self, request):
        user_orders = self.auth.user.orders.all()
        return render(request, 'orders/order_list.html', {
            'orders': user_orders,
            **self.get_context_data()
        })

