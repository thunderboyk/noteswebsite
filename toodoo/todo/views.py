from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
#this a dgango form for signup page 

# Create your views here.
def signupuser(request):
	
	return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
	#creating a dictonary and giving a key to the form 