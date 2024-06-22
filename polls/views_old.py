from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice

# In our poll application, we’ll have the following four views
# render = HttpResponse with template
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # try to get pk's Question object, if it doesn't exist, raise 404 error
    # get_list_or_404() function, which works just as get_object_or_404() – except using filter() instead of get()
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] returns the ID of the selected choice
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # F("votes") + 1 instructs the database to increase the vote count by 1
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # this reverse() call will return a string like "/polls/3/results/", not "/polls/results/3/"
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))