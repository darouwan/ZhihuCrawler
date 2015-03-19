# Create your views here.
import time

from django.shortcuts import render

from input_user.models import Candidates, Users


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'input_user/input.html')


def record(request):
    input_name = request.POST['name']

    candidate = Candidates.objects.filter(name=input_name)
    print(candidate)
    if len(candidate) == 0:

        candidate = Candidates(name=input_name)
        candidate.save()
    else:
        print(input_name, ' is not none')

    context = {'condidate': candidate}
    # return render(request, 'input_user/complete.html', context)
    return showall(request)


def show(request, user_name):
    # print(user_name)
    user_entry_list = Users.objects.filter(user_id=user_name)
    followers_list = []
    upvotes_list = []
    thanks_list = []
    # i = 0
    # Get the user name in zhihu
    if len(user_entry_list) > 0:
        name = user_entry_list[0].name
    else:
        name = user_name
    for user_entry in user_entry_list:
        utc_time = int(time.mktime(user_entry.time.timetuple()) * 1000)
        followers_list.append((utc_time, user_entry.followers))
        upvotes_list.append((utc_time, user_entry.upvotes))
        thanks_list.append((utc_time, user_entry.thanks))
    context = {'name': name, 'followers_list': followers_list[-50:], 'upvotes_list': upvotes_list[-50:],
               'thanks_list': thanks_list[-50:]}
    return render(request, 'input_user/display.html', context)


def showall(request):
    candidates_result = Candidates.objects.all()
    candidates_list = []
    for entry in candidates_result:
        # print(type(entry))
        candidates_list.append(entry.name)
    # print(candidates_list)
    context = {"candidates_list": candidates_list, "name": "test"}
    return render(request, 'input_user/showall.html', context)


def delete(request, user_name):
    Candidates.objects.filter(name=user_name).delete()
    return showall(request)