from carparts.models import Part
from django.views.generic import ListView
from django.db.models import Q


class SearchResultsListView(ListView):
    model = Part
    context_object_name = 'part_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Part.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query) | Q(category__name__icontains=query))
    
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView,
        self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context