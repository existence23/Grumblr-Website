from django.shortcuts import render
from django.template import RequestContext


class operation:
    def plus(self, str1, str2):
        return int(str1) + int(str2)

    def minus(self, str1, str2):
        return int(str1) - int(str2)

    def multiply(self, str1, str2):
        return int(str1) * int(str2)

    def divide(self,str1, str2):
        if str2 == "0":
            return "Error! You cannot divide by 0!"
        else:
            return int(str1) // int(str2)


def calculate(request):

    context = {}
    context['forward_value'] = "0"
    context['operation_value'] = "0"
    context['current_value'] = "0"
    context['result_value'] = "0"
    operator = operation()

    if request.method == 'POST':
        print(True)
        return render(request, 'calculatorTemplates.html', context)

    else:

        if request.GET.get('forwardshown') is not None:
            forwardshown = request.GET.get('forwardshown')
        else:
            forwardshown = "0"
        if request.GET.get('currentshown') is not None:
            currentshown = request.GET.get('currentshown')
        else:
            currentshown = "0"

        if request.GET.get('operationshown'):
            context['operation_value'] = request.GET.get('operationshown')

        if request.GET.get('digitvalue') is not None:

            if context['operation_value'] == "=":
                context['forward_value'] = "0"
                context['operation_value'] = "0"
                context['current_value'] = request.GET.get('digitvalue')
                context['result_value'] = request.GET.get('digitvalue')
            else:
                context['forward_value'] = request.GET.get('forwardshown')
                if request.GET.get('currentshown') == "0":
                    context['current_value'] = request.GET.get('digitvalue')
                    context['result_value'] = request.GET.get('digitvalue')
                else:
                    context['current_value'] = request.GET.get('currentshown') + request.GET.get('digitvalue')
                    context['result_value'] = request.GET.get('currentshown') + request.GET.get('digitvalue')

        if request.GET.get('operation') is not None:
            if context['operation_value'] == "0":
                context['forward_value'] = request.GET.get('currentshown')
            if context['operation_value'] == "=":
                context['forward_value'] = request.GET.get('forwardshown')
            if context['operation_value'] == "+":
                context['forward_value'] = operator.plus(forwardshown, currentshown)
            if context['operation_value'] == "-":
                context['forward_value'] = operator.minus(forwardshown, currentshown)
            if context['operation_value'] == "×":
                context['forward_value'] = operator.multiply(forwardshown, currentshown)
            if context['operation_value'] == "÷":
                if operator.divide(forwardshown, currentshown) == "Error! You cannot divide by 0!":
                    context['forward_value'] = "0"
                    context['operation_value'] = "0"
                    context['current_value'] = "0"
                    context['result_value'] = "0"
                    context['warning'] = "Error! You cannot divide by 0!"
                    return render(request, 'calculatorTemplates.html', context);
                else:
                    context['forward_value'] = operator.divide(forwardshown, currentshown)

            context['operation_value'] = request.GET.get('operation')
            context['current_value'] = "0"
            context['result_value'] = context['forward_value']

        return render(request, 'calculatorTemplates.html', context)
