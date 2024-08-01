# polls/views.py

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Question, Choice
from .forms import RegistrationForm

# Get questions and display them
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

# Show specific question and choices
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Vote for a question choice
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with an error message.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after dealing with POST data.
        # This prevents data from being posted twice if the user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# Register a new user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('polls:login')  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'polls/register.html', {'form': form})

# Login an existing user
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('polls:index')  # Redirect to polls index or any other page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'polls/login.html')

# Logout the current user
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('polls:login')  # Redirect to login page after logout
# polls/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
  # Import requests library to make HTTP requests

def external_data_view(request):
    try:
        # URL of the external API
        url = "https://jsonplaceholder.typicode.com/posts"
        
        # Make a GET request to the external API
        response = request.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Implement pagination
            paginator = Paginator(data, 10)  # 10 items per page
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            
            return render(request, 'polls/external_data.html', {
                'page_obj': page_obj,  # Pass the paginator object to the template
            })
        else:
            return JsonResponse({'error': 'Failed to retrieve data'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
