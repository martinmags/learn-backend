from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F  # help prevent race conditions
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """Return the last five published questions."""
    res = set()

    # Filter by date, top 5
    question = Question.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

    # Filter out questions with no choices
    for q in question:
      if len( q.choice_set.all() ) > 0:
        res.add(q)
    
    return res
      
      
# OLD index view
# def index(request):
#   latest_question_list = Question.objects.order_by('-pub_date')[:5]
#   context = {
#     'latest_question_list': latest_question_list
#   }
#   return render(request, 'polls/index.html', context)


class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/detail.html'
# OLD detail view
# def detail(request, question_id):
#   question = get_object_or_404(Question, pk=question_id)
#   context = {'question': question, 'question_id': question_id}
#   return render(request, 'polls/detail.html', context)

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'
# OLD results view
# def results(request, question_id):
#   question = get_object_or_404(Question, pk=question_id)
#   return render(request, 'polls/results.html', {"question": question})


def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    selected_choice.votes = F('votes') + 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a 
    # user hits the Back button
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
  except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
    