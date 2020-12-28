from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from django.http import HttpResponse, request


# Create your views here.
#
# def confirm(request):
#     if request.method == "POST":
#         meeting_date = request.POST.get('meeting_date')
#
#     return render(request, 'slots/confirm.html')


class confirm(TemplateView):
    template_name = "slots/confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get id from request url
        selected_date = self.kwargs['pro_id']
        print("Selected Date---->", selected_date)
        # filter product by id
        context = {
            'selected_date': selected_date,
        }
        return context


def select(request):
    return render(request, 'slots/select.html', {'title': 'Select'})

