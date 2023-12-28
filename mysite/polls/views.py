from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Choice, Question
from django.views import generic
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Flaw 1, Injection, rows 17-21
        """user_input = self.request.GET.get('user_input', '')
        query = "SELECT * FROM polls_question WHERE question_text LIKE '%" + user_input + "%' ORDER BY pub_date DESC LIMIT 5"
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()"""
        # Fix to flaw 1, rows 23-24
        user_input = self.request.GET.get('user_input', '')
        return Question.objects.filter(question_text__icontains=user_input).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@csrf_exempt                        # Flaw 3, Cross-Site Request Forgery (CSRF). Fix to flaw 3, remove @csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Part of Flaw 2, row 54 (saving user with unhashed password)
            """form.save()
            return redirect(reverse('polls:index'))"""
            # Fix to flaw 2, rows 57-60
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hashing the password
            user.save()
            return redirect(reverse('polls:index'))
    else:
        form = UserRegistrationForm()   
    return render(request, 'polls/register.html', {'form': form})