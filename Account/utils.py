
def detect_user_role(user):
    if user.is_authenticated:
        if user.Role == 'Customer':
            return 'customerdashboard'
        elif user.Role == 'Restaurant':
            return 'restaurantdashboard'
        elif user.is_superadmin:
            return 'admin:index'
    # Default redirect if no role or invalid role
    return 'customerdashboard'