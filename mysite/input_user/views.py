# Create your views here.
import time

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
    followers_list = []
    upvotes_list = []
    thanks_list = []
    for user_entry in user_entry_list:
        utc_time = int(time.mktime(user_entry.time.timetuple()) * 1000)
        followers_list.append((utc_time, user_entry.followers))
        upvotes_list.append((utc_time, user_entry.upvotes))
        thanks_list.append((utc_time, user_entry.thanks))
    context = {'followers_list': followers_list, 'upvotes_list': upvotes_list, 'thanks_list': thanks_list}
    return render(request, 'input_user/display.html', context)