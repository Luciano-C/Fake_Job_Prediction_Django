import pandas as pd
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')

def prediction(request):
    
    form_input_data = pd.read_pickle('model/form_input_data.pickle')
    possible_locations = sorted(form_input_data['possible_locations'])
    possible_employment_types = form_input_data['possible_employment_types']
    possible_required_experience = form_input_data['possible_required_experience']
    possible_required_education = form_input_data['possible_required_education']

    model = pd.read_pickle('model/prediction_model.pickle')
    feature_extraction = pd.read_pickle('model/feature_extraction.pickle')
    


    if request.method == 'GET':
        return render(request, 'prediction.html', {
            'possible_locations': possible_locations,
            'possible_employment_types': possible_employment_types,
            'possible_required_experience': possible_required_experience,
            'possible_required_education': possible_required_education
        })
    
    else:

        title = request.POST['title'].strip()
        
        if request.POST['location'] == 'UNKNOWN/OTHER':
            location = ''
        else:
            location = request.POST['location'].strip()
        
        company_profile = request.POST['company_profile'].strip()
        description = request.POST['description'].strip()
        requirements = request.POST['requirements'].strip()
        benefits = request.POST['benefits'].strip()
        has_questions = request.POST['has_questions'].strip()

        if request.POST['employment_type'] == 'UNKNOWN':
            employment_type = ''
        else:
            employment_type = request.POST['employment_type'].strip()

        if request.POST['required_experience'] == 'UNKNOWN/OTHER':
            required_experience = ''
        else:
            required_experience = request.POST['required_experience'].strip()
        
        if request.POST['required_education'] == 'UNKNOWN/OTHER':
            required_education = ''
        else:
            required_education = request.POST['required_education'].strip()

        

        text = title + ' - ' + location + ' - ' + company_profile + ' - ' + description + ' - ' + requirements +  ' - ' + benefits + ' - ' + has_questions + ' - ' + employment_type + ' - ' + required_experience + ' - ' + required_education


        df_to_process = pd.DataFrame(data={'text': [text]})
        prediction_features = feature_extraction.transform(df_to_process['text'])
        prediction = model.predict(prediction_features)

        if prediction[0] == 0:
            message_to_user = 'True job offer'
            messages.success(request, message_to_user)
        else:
            message_to_user = 'Fake job offer'
            messages.error(request, message_to_user)

        
       
        
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
            'possible_required_education': possible_required_education,
        })