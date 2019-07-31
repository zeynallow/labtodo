from django.shortcuts import render,redirect, get_object_or_404
from .models import TodoList, TodoListShare
from django.contrib.auth.models import User
from django.http import JsonResponse

#Index
def index(request):
    todos = TodoList.objects.filter(user = request.user).order_by('created')
    shared_todos = TodoListShare.objects.filter(shared_user = request.user)
    return render(request, "home.html", {"todos": todos,"shared_todos": shared_todos})

#View Task
def view(request, pk=None):

    try:
        check_share = TodoListShare.objects.filter(shared_user = request.user).get(task_id = int(pk))
    except TodoListShare.DoesNotExist:
        check_share = None

    comments = None
    show_comment = False

    if check_share:
        todo = check_share.task

        #check comment access
        if check_share.share_type == 1:
            comments = todo.comments.all
            show_comment=True

    else:
        todo = get_object_or_404(TodoList,pk = int(pk),user = request.user)
        comments = todo.comments.all
        show_comment=True

    return render(request, "task.html", {"todo": todo,"comments": comments,"show_comment": show_comment})

#Create new task
def create(request):
    if request.POST:
        title = request.POST["title"]
        description = request.POST["description"]
        due_date = str(request.POST["due_date"])
        user = request.user
        Todo = TodoList(title=title, description=description, due_date=due_date, user=user)
        Todo.save()
    return redirect("/")


#Change Status
def changeStatus(request):
    if request.POST:
        task_id = request.POST["task_id"]
        status = request.POST["status"]

        todo = TodoList.objects.filter(id=int(task_id), user = request.user).update(complete=status)
        if(todo):
            return JsonResponse({'message':'success'})
        else:
            return JsonResponse({'message':'error'})


#Share task
def share(request):

    if request.POST:

        share_type = request.POST["share_type"]
        _shared_user = request.POST["shared_user"]

        if '@' in _shared_user:
            kwargs = {'email': _shared_user}
        else:
            kwargs = {'username': _shared_user}

        try:
            shared_user = User.objects.get(**kwargs)
        except User.DoesNotExist:
            shared_user = None
            return JsonResponse({'message':'İstifadəçi tapılmadı'})

        #check :)
        if(shared_user == request.user):
            return JsonResponse({'message':'Özünüzlə paylaşa bilməzsiniz'})


        if shared_user:
            try:
                task = TodoList.objects.get(id = request.POST["task_id"])
            except TodoList.DoesNotExist:
                task = None
                return JsonResponse({'message':'Tapşırıq tapılmadı'})

        if task:
            TodoListShare.objects.get_or_create(task=task, shared_user=shared_user, share_type=share_type)
            return JsonResponse({'message':'Uğurla paylaşıldı'})
