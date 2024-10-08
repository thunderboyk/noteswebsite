from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm,	 AuthenticationForm
#this a dgango form for signup page 
from django.contrib.auth.models import User
# Create your views here.
from django.db import IntegrityError
from  django.contrib.auth import login , logout, authenticate
from .forms import TodoForm
from .models import Todo

from django.utils import timezone
from  django.contrib.auth.decorators import login_required #for only logged in users to use the pages

def home(request):
	return render(request,'todo/home.html')




def signupuser(request):
	if request.method =='GET':
		
			return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
		

		#creating a dictonary and giving a key to the form 

	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.create_user(request.POST['username'], password =request.POST['password1'])
				user.save()
				login(request,user)
				return redirect('currenttodos')


			except IntegrityError:
				return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'User name exits allready'})
			
		else:
			return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'passwords did not match '})










def loginusers(request,):
	if request.method =='GET':
		return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
		if user is None:
			return render(request,'todo/loginuser.html',{'form':AuthenticationForm(), 'error':'Username and Password did not match '})
		else:
			login(request,user)
			return redirect('currenttodos')


@login_required
def logoutuser(request):
	if request.method == 'POST':
		logout(request)
		return redirect("home")


@login_required
def createtodo(request):
	if request.method =='GET':
		return render(request,'todo/createtodo.html',{'form':TodoForm()})
		


	else:
		try:
			form = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request,'todo/createtodo.html',{'form':TodoForm(), 'error':'not so valid data my g '})



@login_required
def currenttodos(request):
	todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
	return render(request,'todo/currenttodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method =="GET":
		form = TodoForm(instance=todo)
		return render(request,'todo/viewtodos.html',{'todo':todo,'form':form})
	else:
		try:
			form = TodoForm(request.POST,instance=todo)
			form.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request,'todo/viewtodos.html',{'todo':todo,'form':form,'error':'info not so intelectual'})


@login_required
def completetodo(request,todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method =="POST":
		todo.datecompleted = timezone.now()
		todo.save()
		return redirect('currenttodos')

@login_required
def tododelete(request,todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method =="POST":
		
		todo.delete()
		return redirect('currenttodos')		

@login_required
def completedtodo(request):
	todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('datecompleted')
	return render(request,'todo/completedtodo.html', {'todos':todos})
