from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect

from core.forms import UserCreationForm


@csrf_protect
def register_view(request):
    """Register using core.forms.UserCreationForm.

    core.forms.UserCreationForm already includes the extra fields:
    branch, semester, college (since it subclasses the custom core.User).
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

