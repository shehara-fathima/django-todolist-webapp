from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .forms import *
from .models import *
from .decorators import *
from django.db.models import Count

# Create your views here.
def register(request):
    if  request.method=='POST':  #This fails and render form and when we click submit, method is post
        f=regform(request.POST) #stores data in f after validation
        if f.is_valid():
            n=f.cleaned_data['name']
            e=f.cleaned_data['email']
            p=f.cleaned_data['password']
            cp=f.cleaned_data['cpass']
            if p==cp:
                if regmodel.objects.filter(name=n).exists():
                    return HttpResponse('USERNAME ALREADY EXISTS')
                else:
                    m=regmodel(name=n,email=e,password=p) #to store data
                    m.save()
                    return redirect('login/')
            else:
                return HttpResponse('PASSWORDS DO NOT MATCH')
        else:
            print(f.errors)
            return HttpResponse('RETURN VALID DATA')
    return render(request,'register.html')

def login(request):
    if request.method == "POST":
        n = request.POST.get("name").strip()
        p = request.POST.get("password").strip()
        print(n,p)

        all_users = regmodel.objects.all()
        for u in all_users:
            print(f"Stored User: {u.name}, Stored Password: {u.password}")

        # Directly check if user exists in DB
        user = regmodel.objects.filter(name=n, password=p).first()
        print("User found:", user)

        if user:  # If a matching user is found
            request.session["user_id"] = user.id  # Store user ID in session
            print(user.id)
            return redirect('home')  # Redirect to home page
        else:
            return HttpResponse("USER NOT FOUND")

    return render(request, "login.html")


@custom_login_required
def home(request):
    print(request.session["user_id"])
    if "user_id" not in request.session:
        return redirect("login")
    if request.method == "GET":
        action = request.GET.get("action")
        if action == "tasks":
            return redirect("tasks")
        elif action == "doodle":
            return redirect("doodle")
        elif action == "statistics":
            return redirect("statistics")
        elif action == 'sign up':
            return redirect("register")
        elif action == 'login':
            return redirect("login")
        elif action== 'logout':
            return redirect('logout')
    return render(request, 'home.html')

@custom_login_required
def tasks(request):
    print("DEBUG: Page loaded")

    # Get task_id and action from query parameters
    task_id = request.GET.get("task_id")
    action = request.GET.get("action")
    show_form = request.GET.get("show_form") == "true"  # Control form visibility
    form=TaskForm()

    # Fetch all tasks
    all_tasks = TaskModel.objects.filter(user=request.session['user_id'])
    pending_tasks = all_tasks.filter(status="pending")
    completed_tasks = all_tasks.filter(status="completed")
    num_pending = pending_tasks.count()

    # Find selected task (if any)
    selected_task = None
    if task_id:
        try:
            task_id = int(task_id)
            selected_task = get_object_or_404(TaskModel, id=task_id)
            print(f"DEBUG: Selected Task ID {task_id}")
        except ValueError:
            selected_task = None

    # Determine which form to show (edit/delete)
    show_status_form = action == "edit"
    show_delete_form = action == "delete"

    if request.method == "POST":  # Handle form submission
        print("POST request received:", request.POST)
        action = request.POST.get("action")
        if action=='confirm' or action=='cancel' :
            form = TaskForm(request.POST)
            if form.is_valid():
                print("Valid form data")
                t = form.cleaned_data["title"]
                d = form.cleaned_data["description"]
                c = request.POST.get("category")
                u = regmodel.objects.get(id=request.session["user_id"])
                task = TaskModel.objects.create(user=u, title=t, description=d, category=c)
                task.save()
                task_id = task.id  # Get newly created task ID
                print("New task created with ID:", task_id)

                # Handle action-based redirection
                if action == "confirm":
                    return redirect("mark_as_completed", task_id)
                elif action == "cancel":
                    return redirect("mark_as_pending", task_id)
                else:
                    return redirect("tasks")  # Refresh task list

            else:
                print("Form errors:", form.errors)


        elif action == 'update_status':
            task_id=request.GET.get('task_id')
            if task_id:
                selected_task=TaskModel.objects.get(id=task_id)
            show_status_form=True
            f=status_form(request.POST)
            if f.is_valid():
                status=f.cleaned_data['status']
                if 'pending' in status:
                    return redirect('mark_as_pending',task_id)
                elif 'completed' in status:
                    return  redirect('mark_as_completed',task_id)
                updated=True
                return redirect('tasks')
            else:
                print(f.errors)
        elif action=='delete_task':
            return redirect('delete_task',task_id)
    elif request.method=='GET':
        if action=='home':
            return redirect('home')
    return render(
            request,
            "tasks.html",
            {
                "form": form,
                "tasks": all_tasks,
                "show_form": show_form,
                "pending_tasks": pending_tasks,
                "completed_tasks": completed_tasks,
                "num_pending": num_pending,
                "selected_task": selected_task,
                "show_status_form": show_status_form,
                "show_delete_form": show_delete_form,
                "updated": False
            },
        )
def mark_as_pending(request,task_id):
    task = get_object_or_404(TaskModel, id=task_id)
    task.status = 'pending'
    task.save()
    pending_tasks=TaskModel.objects.filter(status='pending')
    print(pending_tasks)
    num_pending=pending_tasks.count()
    return redirect('tasks')  # Redirect to your tasks page

def mark_as_completed(request,task_id):
    task = get_object_or_404(TaskModel, id=task_id)
    task.status = 'completed'
    task.save()
    completed_tasks=TaskModel.objects.filter(status='completed')
    print(completed_tasks)
    return redirect('tasks')  # Redirect to your tasks page

def delete_task(request, task_id):
    task = get_object_or_404(TaskModel, id=task_id)
    print(request.method)
    if request.method == "GET":
        task.delete()
        return redirect('tasks')  # Redirect after deletion
    return redirect('tasks')

import base64
from base64 import b64decode
from django.core.files.base import ContentFile
from .models import Drawing
from .forms import DrawingForm
@custom_login_required
def doodle(request):
    if request.method=='GET':
        action=request.GET.get('action')
        if action=='home':
            return redirect('home')
    return render(request,'doodle.html')


from django.shortcuts import render
from django.db.models import Count
from .models import TaskModel
@custom_login_required
def statistics(request):
    # Get logged-in user data
    logged_in_user = request.session['user_id']
    logged_in_user_completed_tasks = TaskModel.objects.filter(user=logged_in_user, status='completed').count()
    logged_in_user_pending_tasks = TaskModel.objects.filter(user=logged_in_user, status='pending').count()
    logged_in_user_total_tasks = logged_in_user_completed_tasks + logged_in_user_pending_tasks

    # Get global data (all users)
    total_completed_tasks = TaskModel.objects.filter(status='completed').count()
    total_pending_tasks = TaskModel.objects.filter(status='pending').count()
    total_tasks = total_completed_tasks + total_pending_tasks
    category_distribution=TaskModel.objects.values('category').annotate(count=Count('category')).order_by('category')

    # Calculate the ratios for comparison
    user_completion_ratio = logged_in_user_completed_tasks / logged_in_user_total_tasks if logged_in_user_total_tasks > 0 else 0
    global_completion_ratio = total_completed_tasks / total_tasks if total_tasks > 0 else 0

    # Suggestion logic based on comparison
    if user_completion_ratio > global_completion_ratio:
        suggestion = "Great job! You're completing more tasks than most users."
    elif user_completion_ratio < global_completion_ratio:
        suggestion = "You might want to focus on completing more tasks to match the average."
    else:
        suggestion = "You're on track! Keep up the good work."

    context = {
        'logged_in_user_completed_tasks': logged_in_user_completed_tasks,
        'logged_in_user_pending_tasks': logged_in_user_pending_tasks,
        'logged_in_user_total_tasks': logged_in_user_total_tasks,
        'total_completed_tasks': total_completed_tasks,
        'total_pending_tasks': total_pending_tasks,
        'category_distribution':category_distribution,
        'total_tasks': total_tasks,
        'suggestion': suggestion,
    }

    if request.method=='GET':
        action=request.GET.get('action')
        if action=='home':
            return redirect('home')
    return render(request, "statistics.html", context)

def logout(request):
    request.session.flush()
    return redirect('login')