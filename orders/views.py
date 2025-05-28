from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Offer
from .forms import OrderForm
from django.db.models import Q

# Для регистрации компаний — при необходимости:
# from .forms import CompanySignupForm

# 1. Клиент: создать заказ
@login_required
def create_order(request):
    if hasattr(request.user, 'company_profile'):
        messages.warning(request, "Companies can't create orders!")
        return redirect('orders:company_order_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user  # <-- вот здесь!
            order.status = 'offers'  # Новый заказ, ждем офферы
            order.save()
            messages.success(request, "Order created! Companies will send you offers soon.")
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})

# 2. Клиент: мои заказы
@login_required
def my_orders(request):
    if hasattr(request.user, 'company_profile'):
        messages.warning(request, "Companies don't have personal orders!")
        return redirect('orders:company_order_list')
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

# 3. Клиент: детали заказа (и офферы)
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

# 4. Клиент: принять оффер (выбрать исполнителя)
@login_required
def accept_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    order = offer.order

    if order.customer != request.user:
        messages.error(request, "You can only accept offers for your orders.")
        return redirect('orders:my_orders')

    if request.method == 'POST':
        order.chosen_offer = offer
        order.status = 'offer_selected'
        order.save()
        offer.status = 'accepted'
        offer.save()
        # Отклонить остальные офферы
        Offer.objects.filter(order=order).exclude(pk=offer.pk).update(status='declined')
        messages.success(request, f"You have selected offer from {offer.company.name}.")
        return redirect('orders:order_detail', order_id=order.id)
    return redirect('orders:order_detail', order_id=order.id)

# 5. Компания: список всех заказов без их оффера (новые заявки)
@login_required
def company_order_list(request):
    if not hasattr(request.user, 'company_profile'):
        messages.warning(request, "Only company users can view this page.")
        return redirect('orders:my_orders')
    company = request.user.company_profile
    offered_orders = Offer.objects.filter(company=company).values_list('order_id', flat=True)
    orders = Order.objects.filter(
        chosen_offer__isnull=True
    ).exclude(
        pk__in=offered_orders
    ).order_by('-created_at')
    return render(request, 'orders/company_order_list.html', {'orders': orders})


# 6. Компания: детали заказа + форма подачи оффера
@login_required
def company_order_detail(request, order_id):
    if not hasattr(request.user, 'company_profile'):
        messages.warning(request, "Only company users can view this page.")
        return redirect('orders:my_orders')
    company = request.user.company_profile
    order = get_object_or_404(Order, pk=order_id)
    already_offered = Offer.objects.filter(order=order, company=company).exists()

    if request.method == 'POST' and not already_offered:
        price = request.POST.get('price')
        message = request.POST.get('message', '')
        if price:
            Offer.objects.create(order=order, company=company, price=price, message=message)
            messages.success(request, "Offer sent!")
            return redirect('orders:company_order_list')
        else:
            messages.error(request, "Price is required.")

    return render(request, 'orders/company_order_detail.html', {
        'order': order,
        'already_offered': already_offered
    })

# 7. Компания: мои офферы (история)
@login_required
def company_my_offers(request):
    if not hasattr(request.user, 'company_profile'):
        messages.warning(request, "Only company users can view this page.")
        return redirect('orders:my_orders')
    company = request.user.company_profile
    offers = Offer.objects.filter(company=company).select_related('order').order_by('-created_at')
    return render(request, 'orders/company_my_offers.html', {'offers': offers})

# Staff dashboard (при необходимости)
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def staff_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/staff_order_list.html', {'orders': orders})

@staff_member_required
def staff_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/staff_order_detail.html', {'order': order})

@staff_member_required
def staff_change_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f'Status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status!')
        return redirect('orders:staff_order_detail', order_id=order.id)
    return redirect('orders:staff_order_detail', order_id=order.id)
