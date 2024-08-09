from django.urls import path
from .views import SignUpView, SignInView, ResetPasswordView, InviteMemberView, DeleteMemberView, UpdateMemberRoleView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('invite-member/', InviteMemberView.as_view(), name='invite-member'),
    path('delete-member/', DeleteMemberView.as_view(), name='delete-member'),
    path('update-member-role/', UpdateMemberRoleView.as_view(), name='update-member-role'),
]
