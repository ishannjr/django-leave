from django import forms
from .models import CASUAL, DAYS, LEAVE_TYPE, Leave, SICK
import datetime
from django.core.mail import send_mail
from django.urls import reverse

from django.http import HttpResponseRedirect, HttpResponse

class LeaveCreationForm(forms.ModelForm):
	reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
	class Meta:
		model = Leave
		exclude = ['user','defaultdays','hrcomments','status','is_approved','updated','created']



	def clean_enddate(self):
		enddate = self.cleaned_data['enddate']
		startdate = self.cleaned_data['startdate']
		today_date = datetime.date.today()
		dates=enddate-startdate
		print(LEAVE_TYPE[0][0])
		print(LEAVE_TYPE[1][0])
		
		if (startdate or enddate) < today_date:# both dates must not be in the past
			raise forms.ValidationError("Selected dates are incorrect,please select again")

		elif startdate >= enddate:# TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
			raise forms.ValidationError("Selected dates are wrong")

		elif(dates.days>10):
			raise forms.ValidationError("Cannot select these many days")
		
		
		elif LEAVE_TYPE[0][0]=='sick'and dates.days>7 :
		 	raise forms.ValidationError("Cannot select these many days")

		elif LEAVE_TYPE[1][0]=='casual'and dates.days>7 :
			raise forms.ValidationError("Cannot select these many days")
		
		elif LEAVE_TYPE[2][0]=='emergency'and dates.days>7 :
			raise forms.ValidationError("Cannot select these many days")

		elif LEAVE_TYPE[3][0]=='study'and dates.days>7 :
		 	raise forms.ValidationError("Cannot select these many days")


		
		return enddate

	