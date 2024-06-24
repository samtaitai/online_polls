from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

"""
Generic views abstract common patterns to the point where you dont even need to write Python code to write an app. For example, the ListView and DetailView generic views abstract the concepts of “display a list of objects” and “display a detail page for a particular type of object”
"""
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    # override the default context_object_name(question_list)
    context_object_name = "latest_question_list"
    # "latest_question_list"
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:6]


class DetailView(generic.DetailView):
    # Each generic view needs to know what model it will be acting upon
    model = Question
    # override the default template_name(polls/question_detail.html)
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "polls/results.html"

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # update is_most_voted field before rendering
    Choice.most_voted(question.id) 
    return render(request, 'polls/results.html', {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # test the exception to occur
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
    # if there is no exception then execute this block     
    else:
        # F("votes") + 1 instructs the database to increase the vote count by 1
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # this reverse() call will return a string like "/polls/3/results/", not "/polls/results/3/"
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def create_poll(request):
    if request.method == 'POST':
        # request.POST is a dictionary-like object that contains all the data submitted in the form.
        # Each form field's data is retrieved by its name attribute
        question_text = request.POST['question_text']
        pub_date = request.POST['pub_date']
        end_date = request.POST['end_date']
        # how many choices user chose
        num_of_choice = int(request.POST['num_of_choice'])
        
        # Create the Question object
        question = Question(question_text=question_text, pub_date=pub_date, end_date=end_date)
        question.save()
        
        # Create Choice objects
        # question.choice_set.create(choice_text=choice_1) creates and saves a Choice object
        # choice_set is a related manager provided by Django for reverse relations (from Question to Choice).
        # By default, the related manager is named <model>_set

        # create as many choices as user chose 
        for i in range(1, num_of_choice + 1):
            choice_text = request.POST[f'choice_{i}']
            if choice_text:
                question.choice_set.create(choice_text=choice_text)
        
        # redirect to index page
        return redirect('polls:index')
    
    # If the request method is not POST (typically a GET request), this line renders the form template.
    # return render(request, 'polls/create_poll.html', 
    # {'num_of_choice': int(request.POST['num_of_choice'])+1})
    return render(request, 'polls/create_poll.html')
