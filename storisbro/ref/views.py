from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Referral

@login_required
def referral_view(request, referral_number):

    try:
        referral_user = User.objects.get(pk=referral_number)

    except User.DoesNotExist:

        return render(request, 'error.html', {'message': 'Referral user not found'})

    return render(request, 'referral_view.html', {'referral_user': referral_user})

@login_required
def register_referral(request):

    if request.method == 'POST':
        referral_number = request.POST.get('referral_number')
        referrer = request.user  

        try:
            referral_user = User.objects.get(pk=referral_number)
        except User.DoesNotExist:

            return render(request, 'error.html', {'message': 'Referral user not found'})

        Referral.objects.create(referrer=referrer, referral=referral_user)
        return redirect('home')  

    return render(request, 'register_referral.html')