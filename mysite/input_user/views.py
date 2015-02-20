# Create your views here.
from django.shortcuts import render

from input_user.models import Candidates, Users


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'input_user/input.html')


def record(request):
    input_name = request.POST['name']
    candidate = Candidates(name=input_name)
    candidate.save()
    context = {'condidate': candidate}
    return render(request, 'input_user/complete.html', context)


def show(request, user_name):
    print(user_name)
    user_entry_list = Users.objects.filter(user_id=user_name)
    return render(request, 'input_user/display.html')