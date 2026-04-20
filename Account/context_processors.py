from Vendor.models import Vendor




def get_vendor(request):
    vendor = None
    if request.user.is_authenticated:
        try:
            vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            vendor = None
        except Vendor.MultipleObjectsReturned:
            vendor = Vendor.objects.filter(user=request.user).first()
    return {'vendor': vendor}
    return dict(vendor=vendor)