from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Tests, Answers

def required_authentication_decorator(func):

    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect('login')

    return wrapper

@required_authentication_decorator
def tests_view(request):
    queryset = Tests.objects.all()
    context = {
        'tests': queryset
    }
    return render(request, 'tests.html', context=context)

@required_authentication_decorator
def test_detail_view(request, test_id):

    obj = get_object_or_404(Tests, pk=test_id)
    context = {
        'test': obj
    }
    return render(request, 'test_detail.html', context=context)

@required_authentication_decorator
def testing_view(request, test_id, question_number):
    if request.POST:
        current_question = int(request.POST['current_question'])
        if 'answer' not in request.POST:
            raise Http404('Вы не ответили на вопросс')
        elif 'last_question' in request.POST:
            obj = get_object_or_404(Answers, pk=request.POST['answer'])
            obj.votes += 1
            obj.save()
            obj = get_object_or_404(Tests, pk=test_id)
            context = {
                'test': obj
            }
            return render(request, 'finish_test.html', context=context)
        else:
            obj = get_object_or_404(Answers, pk=request.POST['answer'])
            obj.votes += 1
            obj.save()
    else:
        current_question = 1
    if current_question == question_number:
        obj = get_object_or_404(Tests, pk=test_id)
        questions = list(obj.questions_set.all())
        question_count = len(questions)
        question = questions[question_number - 1]
        answers = question.answers_set.all()
        context = {
            'test': obj,
            'question': question,
            'question_count': question_count,
            'answers': answers,
            'question_number': question_number
        }
        return render(request, 'testing.html', context=context)
    else:
        raise Http404('Тесты нужно проходить по порядку!')
