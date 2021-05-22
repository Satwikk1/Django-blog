from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Form
from . import models


ChildrenFormset = inlineformset_factory(models.Parent, models.Child, fields=['name'], extra=1)
AddressFormset = inlineformset_factory(models.Child, models.Address, fields=['country', 'state', 'address'] ,extra=1)


class BaseChildrenFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseChildrenFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = AddressFormset(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='address-%s-%s' % (
                            form.prefix,
                            AddressFormset.get_default_prefix()),
                        extra=1)

    def is_valid(self):
        result = super(BaseChildrenFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseChildrenFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

ChildrenFormset = inlineformset_factory(models.Parent,
                                        models.Child,
                                        fields=['name'],
                                        formset=BaseChildrenFormset,
                                        extra=1)

class userRegister(forms.ModelForm):

	class Meta:
		model=Form
		fields=['first_name', 'last_name', 'dob', 'userid']

	# first_name=forms.CharField(required=False)
	# last_name=forms.CharField(required=False)
	# dob=forms.DateTimeField(required=False)
	# userid=forms.CharField(required=False)



	# class Meta:
	# 	model=Form
	# 	fields=['first_name', 'last_name', 'dob', 'userid']



