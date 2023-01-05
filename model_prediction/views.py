import pandas as pd
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')

def prediction(request):
    
    # Get dictionary from picke file which will be used to populate the options on select elements in prediction.html
    form_input_data = pd.read_pickle('model/form_input_data.pickle')
    
    # Store the dictionary data in different variables
    possible_locations = sorted(form_input_data['possible_locations'])
    possible_employment_types = form_input_data['possible_employment_types']
    possible_required_experience = form_input_data['possible_required_experience']
    possible_required_education = form_input_data['possible_required_education']

    # Get logistic regression model from pickle file
    model = pd.read_pickle('model/prediction_model.pickle')
    # Get TfidfVectorizer instance from pickle file
    feature_extraction = pd.read_pickle('model/feature_extraction.pickle')
    


    if request.method == 'GET':
        return render(request, 'prediction.html', {
            'possible_locations': possible_locations,
            'possible_employment_types': possible_employment_types,
            'possible_required_experience': possible_required_experience,
            'possible_required_education': possible_required_education
        })
    
    else:
        # Remove the white spaces at the start and end from each input
        # Select/option have some optiones named UNKNOWN or UNKNOWN/OTHER replacing empty strings in the original dataframe, if those options are being selected, an empty string is being assigned so is consistent with the model
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

        
        # The input is concatenated in the same way the model was generated
        text = title + ' - ' + location + ' - ' + company_profile + ' - ' + description + ' - ' + requirements +  ' - ' + benefits + ' - ' + has_questions + ' - ' + employment_type + ' - ' + required_experience + ' - ' + required_education

        # This concatenated text is storaged in a dataframe with the same structure that the one used to adjust the model, one column named 'text'
        df_to_process = pd.DataFrame(data={'text': [text]})
        # The column is transformed using the TfidfVectorizer instance
        prediction_features = feature_extraction.transform(df_to_process['text'])
        # The transformed column is used to generate a prediction
        prediction = model.predict(prediction_features)

        # A message to the user is generated depending on the prediction. The messages framework is used and sent as a flash alert
        if prediction[0] == 0:
            message_to_user = 'The offer is most likely true.'
            messages.success(request, message_to_user)
        else:
            message_to_user = 'The offer is most likely fake.'
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