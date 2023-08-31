from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Cart

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        max_length=16, min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入帳號'}),
        error_messages={
            'required': '帳號為必填項目。',
            'min_length': '帳號至少需要包含4個字元。',
            'unique': '此帳號已被註冊。',
        }
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '請輸入電子郵件'}),
        error_messages={
            'required': '電子郵件為必填項目。',
            'invalid': '電子郵件格式不正確。',
        }
    )
    password1 = forms.CharField(
        label="密碼",
        max_length=20, min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請輸入密碼'}),
        error_messages={
            'required': '密碼為必填項目。',
            'min_length': '密碼至少需要包含8個字元。',
        }
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請輸入密碼確認'}),
        error_messages={
            'required': '密碼確認為必填項目。',
            'password_mismatch': '兩次輸入的密碼不相符。',
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("此電子郵件已被註冊。")
        return email
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs=
                               {'class': 'form-control',
                                'placeholder': '請輸入帳號'})
    )

    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '請輸入密碼'},)
    )

class ChangePasswordForm(forms.Form):
    username = forms.CharField(
        label="帳號", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入帳號'})
    )
    email = forms.EmailField(
        label="電子郵件", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '請輸入電子郵件'})
    )
    password1 = forms.CharField(
        label="密碼", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請輸入新密碼'})
    )
    password2 = forms.CharField(
        label="密碼確認", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請輸入新密碼確認'})
    )
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError("密碼必須至少包含8個字符")
        
        if password1.isdigit():
            raise forms.ValidationError("密碼不能完全由數字組成")
        
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError("兩次輸入的密碼不相符")
        
        return password2
        
        
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CommentForm(forms.ModelForm):
    star_num = forms.IntegerField(widget=forms.HiddenInput())  # 新增 star_num 欄位

    class Meta:
        model = Comment
        fields = ['text', 'star_num']  

    # user = forms.ModelChoiceField(queryset=User.objects.all())

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'style_color', 'style_capacity', 'volume']

