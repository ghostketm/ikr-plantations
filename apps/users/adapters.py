from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse_lazy
from allauth.account.utils import user_email

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to override default allauth behavior.
    """

    def get_login_redirect_url(self, request):
        """
        Redirect users to the appropriate dashboard after login.
        """
        if request.user.is_superuser:
            return reverse_lazy('agents:agent_dashboard')
        
        # The related_name from the Agent model to User is 'agent'.
        if hasattr(request.user, 'agent') and request.user.agent.verification_status == 'verified':
             return reverse_lazy('agents:agent_dashboard')

        return '/'

    def populate_username(self, request, user):
        """
        Populates the username with the user's email address to ensure uniqueness.
        """
        email = user_email(user)
        if email:
            user.username = email