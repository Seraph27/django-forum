# version 1

class QuickForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        reverse_url = kwargs('reverse_url', None)
        super().__init__(*args, **kwargs) 
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        if reverse_url:
            self.helper.form_action = reverse_url
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-warning')) 

class DirectMessageForm(QuickForm): 
    class Meta:
        model = DirectMessage
        fields = ['to_user', 'text']

DirectMessageForm(reverse_url=reverse('direct_message_create'))

# version 2

class QuickForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-warning')) 

class DirectMessageForm(QuickForm): 
    class Meta:
        model = DirectMessage
        fields = ['to_user', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.helper.form_action = reverse('direct_message_create')

DirectMessageForm()