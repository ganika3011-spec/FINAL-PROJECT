from urllib.parse import uses_relative
from accounts.models import UserProfile
from vendor.models import Vendor
from django.conf import settings

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)



def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}


def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}


def get_vendor_notifications(request):
    if request.user.is_authenticated and request.user.role == 1:
        try:
            from vendor.models import Vendor
            from orders.models import Order
            vendor = Vendor.objects.get(user=request.user)
            vendor_new_orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True, status='New').order_by('-created_at')
            return {
                'new_orders_count': vendor_new_orders.count(),
                'new_orders_list': vendor_new_orders[:5],
            }
        except Exception as e:
            pass
    return {
        'new_orders_count': 0,
        'new_orders_list': [],
    }


def get_customer_notifications(request):
    if request.user.is_authenticated and request.user.role == 2:
        try:
            from orders.models import Order
            print(f"DEBUG: User {request.user.email} is authenticated. Role: {request.user.role}")
            active_orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-updated_at')
            print(f"DEBUG: Active orders count for user: {active_orders.count()}")
            accepted_orders_count = active_orders.filter(status='Accepted').count()
            return {
                'customer_active_orders': active_orders[:5],
                'customer_notifications_count': accepted_orders_count,
            }
        except Exception as e:
            print("DEBUG: Exception in get_customer_notifications:", e)
    return {
        'customer_active_orders': [],
        'customer_notifications_count': 0,
    }