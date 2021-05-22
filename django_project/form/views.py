from django.shortcuts import render, redirect, get_object_or_404
from .forms import userRegister
from django.contrib import messages
from .models import Form
from .forms import *

# Create your views here.


def manage_children(request, parent_id):
    """Edit children and their addresses for a single parent."""

    parent = get_object_or_404(models.Parent, id=parent_id)

    if request.method == 'POST':
        formset = forms.ChildrenFormset(request.POST, instance=parent)
        if formset.is_valid():
            formset.save()
            return redirect('parent_view', parent_id=parent.id)
    else:
        formset = forms.ChildrenFormset(instance=parent)

    return render(request, 'manage_children.html', {
                  'parent':parent,
                  'children_formset':formset})

def home(request):
	if request.method == 'POST':
		form=userRegister(request.POST)
		if form.is_valid():
			userid=form.cleaned_data['userid']
			first_name=form.cleaned_data['first_name']
			print(userid, first_name)
			return redirect('blog-home')
	else:
		form=userRegister()

	return render(request, 'form/register.html', {'form':form})
