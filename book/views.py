from django import views
from django.http import HttpResponseRedirect, request
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Data
from .forms import AddData
from django.views import View
from django.views.generic.base import RedirectView, TemplateView

# Create your views here.


class UpdateData(View):
    template_name = 'update.html'

    def post(self, request, id):
        update_object = Data.objects.get(pk=id)
        fm = AddData(request.POST, instance = update_object)
        if fm.is_valid():
            fm.save()
        return HttpResponseRedirect('/')    

    def get(self, request, id):
        update_object = Data.objects.get(pk=id)
        fm = AddData(instance=update_object)
        return render(request, self.template_name, {'form':fm})


class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        fm = AddData()
        displayData = Data.objects.all()
        context = {'form':fm, 'alldata': displayData}
        return context
    
    def post(self,request):
        fm = AddData(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            lm = fm.cleaned_data['lastname']
            lc = fm.cleaned_data['locality']
            ct = fm.cleaned_data['city']
            mb = fm.cleaned_data['mobile']
            em = fm.cleaned_data['email']
            alldata = Data(name=nm, lastname=lm, locality=lc, city=ct, mobile=mb, email=em)
            alldata.save()
            return HttpResponseRedirect('/')
        

class DeleteData(RedirectView):
    url = '/'
    def get_redirect_url(self, *args, **kwargs):
        del_id = kwargs['id']
        # print(del_id)
        Data.objects.get(pk=del_id).delete()
        return super().get_redirect_url(*args, **kwargs)


class Test(View):
    def get(self, request):
        fm =AddData()
        return render(request, 'rough.html', {'form':fm})