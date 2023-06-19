from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    pickles_list,
    sweet_list,
    hot_list,
    other_list,
    menu_list,
    AddCouponViewOrderSummary,
    TrueFoodsPayment,
    detail
)

app_name = 'core'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('order-summary/add-coupon/', AddCouponViewOrderSummary.as_view(), name='add-coupon-order-summary'),

    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('sweet_list/',sweet_list,name="sweets"),
    path('hot_list/',hot_list,name="hot"),
    path("other_list",other_list,name="others"),
    path('menu/',menu_list,name="menu"),
    path('pickles/',pickles_list,name='pickles'),
    path('account/payment',TrueFoodsPayment.as_view(),name="truefoodspayment"),
    path('detail/<slug>',detail,name="detail")

]
