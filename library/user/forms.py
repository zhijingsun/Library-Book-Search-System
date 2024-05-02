
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class BookSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search')
    search_type = forms.ChoiceField(choices=[
        ('all', 'All fields'),
        ('title', 'Book Name'),
        ('author', 'Author'),
        ('isbn', 'ISBN')
    ], required=False, label='Search in')
    start_year = forms.ChoiceField(
        choices=[(str(year), year) for year in range(1900, 2025)],
        required=False,
        label='Start Year',
        widget=forms.Select()
    )

    end_year = forms.ChoiceField(
        choices=[(str(year), year) for year in range(1900, 2025)],
        required=False,
        label='End Year',
        widget=forms.Select()
    )
    order_by = forms.ChoiceField(choices=[
        ('', '--- Select an option ---'),
        ('publication_year', 'Year'),
        ('title', 'Book Name'),
        ('author', 'Author Name')
    ], required=False, label='Order by', initial='title')
    order_direction = forms.ChoiceField(choices=[
        ('asc', 'Ascending'),
        ('desc', 'Descending')
    ], required=False, label='Order Direction', initial='asc')

class AddToListForm(forms.Form):
    # 这里可以定义表单需要提交的数据，比如隐藏字段
    book_id = forms.IntegerField(widget=forms.HiddenInput())

