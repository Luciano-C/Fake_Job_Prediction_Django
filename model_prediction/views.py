import pandas as pd
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def prediction(request):
    
    form_input_data = pd.read_pickle('model/form_input_data.pickle')
    possible_locations = sorted(form_input_data['possible_locations'])
    possible_employment_types = form_input_data['possible_employment_types']
    possible_required_experience = form_input_data['possible_required_experience']
    possible_required_education = form_input_data['possible_required_education']

    model = pd.read_pickle('model/prediction_model')
    feature_extracion = pd.read_pickle('model/feature_extraction.pickle')
    


    if request.method == 'GET':
        return render(request, 'prediction.html', {
            'possible_locations': possible_locations,
            'possible_employment_types': possible_employment_types,
            'possible_required_experience': possible_required_experience,
            'possible_required_education': possible_required_education
        })
    
    else:
        print(request.POST)
        return render(request, 'prediction.html', {
            'value_title': request.POST['title'],
            'value_location': request.POST['location'],
            'value_company_profile': request.POST['company_profile'],
            'value_description': request.POST['description'],
            'value_requirements': request.POST['requirements'],
            'value_benefits': request.POST['benefits'],
            'value_has_questions': request.POST['has_questions'],
            'value_employment_type': request.POST['employment_type'],
            'value_required_experience': request.POST['required_experience'],
            'value_required_education': request.POST['required_education'],
            'possible_locations': possible_locations,
            'possible_employment_types': possible_employment_types,
            'possible_required_experience': possible_required_experience,
            'possible_required_education': possible_required_education
        })