from .models import Student, Section, Enrollment, Enrollment1
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import NameForm, SearchForm, RegForm, SubAdd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def list(request):
	check = Section.objects.all()
	if check.exists():
		return render(request, 'exer3/login_view.html', {})
	else:
		soft = Section.objects.create(name='Software')
		hard = Section.objects.create(name='Hardware')
		net = Section.objects.create(name='Networking')
		return render(request, 'exer3/login_view.html', {})

#user authentication
def login_view(request):
    if request.POST:
        username = request.POST['user']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return render(request, 'exer3/login_view.html', {})
        else:
            return render(request, 'exer3/login_view.html', {'error_message':"Invalid email or password! Please try again."})
        
def logout_view(request):
    logout(request)
    return render(request, 'exer3/login_view.html', {})

def create(request):
	if request.POST:
		username = request.POST['user']
		password = request.POST['pass']
		email = request.POST['mail']
		first_name = request.POST['fname']
		last_name = request.POST['lname']
		user = User.objects.create_user(username, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				auth_login(request, user)
				first = Student.objects.filter(section__name='Hardware')
				return render(request, 'exer3/login_view.html', {'first': first})

def signup(request):
    return render(request, 'exer3/LoginPage.html', {})

#listing page
def profile(request):   
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		return render(request, 'exer3/profile.html', {})

def software(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		first = Student.objects.all()
		return render(request, 'exer3/software.html', {'first':first})

def subject(request, pk):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		post = get_object_or_404(Section, pk=pk)
		if post.name == "Software":
			first = Student.objects.filter(section__name='Software')
			return render(request, 'exer3/software.html', {'first': first})
		elif post.name == "Hardware":
			first = Student.objects.filter(section__name='Hardware')
			return render(request, 'exer3/software.html', {'first': first})
		else:
			first = Student.objects.filter(section__name='Networking')
			return render(request, 'exer3/software.html', {'first': first})

def student(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		stud = Student.objects.all()
		sect = Enrollment.objects.all()
		form = SearchForm()
		return render(request, 'exer3/student.html', {'stud': stud , 'sect': sect})

#add,delete,edit,search    
def remove(request, pk):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		try:
			post2 = get_object_or_404(Enrollment, pk=pk)
			post2.delete()
			sect = Enrollment.objects.all()
			form = SearchForm()
			return render(request, 'exer3/student.html', {'sect': sect})
		except:
			sect = Enrollment.objects.all()
			form = SearchForm()
			return render(request, 'exer3/student.html', {'sect': sect, 'error_message':"Error, Object missing or already deleted."})

def remove1(request, pk):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		try:
			post = get_object_or_404(Student, pk=pk)
			post.delete()
			first = Student.objects.all()
			form = SearchForm()
			return render(request, 'exer3/software.html', {'first': first, 'form': form})
		except:
			first = Student.objects.all()
			form = SearchForm()
			return render(request, 'exer3/software.html', {'first': first, 'error_message':"Error, Object missing or already deleted."})

def search(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
	    if request.POST:
	        search = request.POST['srch']
	        sect = Enrollment.objects.filter(student__name__icontains=search)
	        if sect.exists():
	        	form = SearchForm()
	       		return render(request, 'exer3/student.html', {'sect': sect, 'form': form})

	        else:
	        	sect = Enrollment.objects.filter(section__name__icontains=search)
	        	form = SearchForm()
	        	return render(request, 'exer3/student.html', {'sect': sect,'form': form})

def search1(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
	    if request.POST:
	        search = request.POST['srch']
	        first = Student.objects.filter(name__icontains=search)
	        form = SearchForm()
	        return render(request, 'exer3/software.html', {'first': first}, {'form': form})

def add(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
	    if request.POST:
	        form = RegForm()
	        return render(request, 'exer3/add.html', {'form': form})

def add1(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		if request.method == 'POST':
			form = RegForm(request.POST)
			if form.is_valid():
				name = form['name'].value()
				subject = form['subject_list'].value()
				new1 = get_object_or_404(Section, name=subject)
				check = Enrollment.objects.filter(student__name=name, section__name=subject)
				if check.exists():
					stud = Student.objects.all()
					sect = Enrollment.objects.all()
					form = SearchForm()
					return render(request, 'exer3/student.html', {'stud': stud , 'sect': sect, 'error_message': "Error, This data is already existing"})
				else:		
					check1 = Student.objects.filter(name=name)
					if check1.exists():
						new = Student.objects.get(name=name)
						new1 = Enrollment(student=new, section= new1)
						new1.save()
						sect = Enrollment.objects.all()
						form = SearchForm()
						return render(request, 'exer3/student.html', {'sect': sect})
					else:
						new = Student.objects.create(name=name)
						new1 = Enrollment.objects.create(student=new, section= new1)
						new1.save()
						sect = Enrollment.objects.all()
						form = SearchForm()
						return render(request, 'exer3/student.html', {'sect': sect})

def add2(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
	    if request.POST:
	        form = SubAdd()
	        return render(request, 'exer3/add2.html', {'form': form})

def add3(request):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
	    if request.method == 'POST':
	        form = SubAdd(request.POST)
	        if form.is_valid():
	            name = form['name'].value()
	            new = Student.objects.create(name=name)
	            new.save()
	            first = Student.objects.all()
	            form = SearchForm()
	            return render(request, 'exer3/software.html', {'first': first, 'form': form})

def edit(request, pk):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		form = RegForm()
		try:
			edit1 = get_object_or_404(Enrollment, pk=pk) 
			edit = Student.objects.filter(name=edit1.student)
			return render(request, 'exer3/edit.html', {'edit1': edit1, 'edit': edit, 'form': form})
		except:
			sect = Enrollment.objects.all()
			form = SearchForm()
			return render(request, 'exer3/student.html', {'sect': sect, 'error_message':"Error, Object missing or already deleted."})

def edit1(request, pk):
	if not request.user.is_authenticated:
		return render(request, 'exer3/login_view.html', {'error_message':"Please Login to access this page"})
	else:
		try:
			edit1 = get_object_or_404(Enrollment, pk=pk) 
			edit = Student.objects.filter(name=edit1.student)
			if request.method == 'POST':
				form = RegForm(request.POST)
				if form.is_valid():            
					name1 = form['name'].value()
					subject = form['subject_list'].value()
					new1 = get_object_or_404(Section, name=subject)  
					#new.name = name1
					#new.save()
					#edit1.delete()
					#new1 = Enrollment.objects.create(student=edit.name, section= new1)
					#new1.save()
					check = Enrollment.objects.filter(student__name=name1, section__name=subject)
					if check.exists():
						#sect = Enrollment.objects.filter(section__name=subject)
						#if sect.exists():
						stud = Student.objects.all()
						sect = Enrollment.objects.all()
						form = SearchForm()
						return render(request, 'exer3/student.html', {'stud': stud , 'sect': sect, 'error_message': "Error, This data is already existing"})
					else:
						Student.objects.filter(name=edit1.student).update(name=name1)
						new = Student.objects.get(name=name1)
						edit1.delete()
						new1 = Enrollment.objects.create(student=new, section= new1)
						stud = Student.objects.all()
						sect = Enrollment.objects.all()
						form = SearchForm()
						return render(request, 'exer3/student.html', {'stud': stud , 'sect': sect})
					#else:
						#Student.objects.filter(name=edit1.student).update(name=name1)
						#new = Student.objects.get(name=name1)
						#edit1.delete()
						#new1 = Enrollment.objects.create(student=new, section= new1)
						#stud = Student.objects.all()
						#sect = Enrollment.objects.all()
						#form = SearchForm()
						#return render(request, 'exer3/student.html', {'stud': stud , 'sect': sect})
		except:
			sect = Enrollment.objects.all()
			form = SearchForm()
			return render(request, 'exer3/student.html', {'sect': sect , 'error_message':"Error, Object missing or already deleted."})

@login_required
def new(request):
    form = NameForm()
    return render(request, 'exer3/new.html', {'form': form})


#def server_error(request):
#    return render(request, 'errors/500.html')
 
#def not_found(request):
#    return render(request, 'errors/404.html')
 
#def permission_denied(request):
#    return render(request, 'errors/403.html')
 
#def bad_request(request):
#    return render(request, 'errors/400.html')