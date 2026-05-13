
from django.shortcuts import render, redirect
from django.contrib.auth import login
from core.forms import UserCreationForm
from core.models import Branch


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            # handle extra fields from POST (branch, semester, college)
            branch_code = request.POST.get('branch')
            if branch_code:
                try:
                    user.branch = Branch.objects.get(code=branch_code)
                except Branch.DoesNotExist:
                    pass
            semester = request.POST.get('semester')
            if semester:
                user.semester = int(semester)
            user.college = request.POST.get('college', '')
            user.save()
            login(request, user)
            return redirect('/')
        # if form invalid, fall through to re-render with errors
    else:
        form = UserCreationForm()
    
    # Render the same login.html template (which contains both login and register forms)
    return render(request, 'login.html', {'form': form})