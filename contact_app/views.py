from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket
from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        try:
            user = request.user if request.user.is_authenticated else None

            # Create the ticket
            Ticket.objects.create(
                user=user,
                full_name=request.POST.get("full_name"),
                email=request.POST.get("email"),
                message=request.POST.get("message"),
            )

            # Add a success message
            messages.success(request, 'پیام شما دریافت شد . به زودی با شما ارتباط برقرا می کنیم')

        except Exception as e:
            # Add an error message in case something goes wrong
            messages.error(request, f'مشکلی به وجود آمد .لطفا دوباره تلاش کنید')

        return render(request, 'contact.html')

    return render(request, 'contact.html')