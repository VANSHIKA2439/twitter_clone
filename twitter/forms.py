from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

 
class ProfileImageForm(forms.ModelForm):
    profile_image=forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Profile Bio'}), max_length=500, required=False)
    homepage_link = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Homepage Link'}), max_length=200, required=False)
    facebook_link= forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Facebook Link'}), max_length=200, required=False)
    instagram_link= forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Instagram Link'}), max_length=200, required=False)
    linkeldn_link=  forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Linkeldn Link'}), max_length=200, required=False)


    class Meta:
        model = Profile
        fields=('profile_image','profile_bio','homepage_link','facebook_link','instagram_link','linkeldn_link',)

class TweetsForm(forms.ModelForm):
    body = forms.CharField(required=True,widget=forms.widgets.Textarea(
        attrs={
            "placeholder":"Enter Yout tweet!",
            "class":"form-control"
        }
    ),
    label="")
    class Meta:
        model = Tweet
        exclude = ("user","likes")



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    first_name = forms.CharField(label="",max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(label="",max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password1','password2')

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['username'].label=''
        #self.fields['username'].help_text='<span class="form-text text-muted"><small>Required. 150 characters limit</small><br></span><input type="text" class="form-control" name="username">'

        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['placeholder']='Password'
        self.fields['password1'].label=''
        #self.fields['password1'].help_text='<input type="password" class="form-control" name="password1">'

        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['placeholder']='Password'
        self.fields['password2'].label=''
        #self.fields['password2'].label='<span class="form-text text-muted"><small>Confirm Password</small></span><br><input type="password" class="form-control" name="password2">'


    

    