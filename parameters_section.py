from utils import add_model_table

def add_parameters_and_configurations_section(document, swagger_data, parameters_index, models_index, github_link, config):
    document.add_heading(f'{parameters_index}. Parameters and Configurations', level=1)
    document.add_heading(f'{parameters_index}.1 General Configuration', level=2)
    add_subsection(document, f'{parameters_index}.1.1 Github Repository', github_link)
    
    base_url = github_link
    last_word = github_link.rsplit('-', 1)[-1]
    last_word = last_word.split('/')[-1] 
    swagger_model_link = f"{base_url}/blob/master/src/main/resources/servergen/{last_word}.json"
    
    add_subsection(document, f'{parameters_index}.1.2 Swagger Model', swagger_model_link)
    add_subsection(document, f'{parameters_index}.1.3 Postman Collection', 'Insert Postman Collection file here')
    
    document.add_heading(f'{parameters_index}.2 Models Definition', level=2)
    definitions = swagger_data.get('definitions', {})
    model_sub_index = 1
    for model_name, model_details in definitions.items():
        models_index = add_model_table(document, model_name, model_details, f'{parameters_index}.2', model_sub_index)
        model_sub_index += 1
    return parameters_index + 1, models_index  

def add_subsection(document, title, content):
    document.add_heading(title, level=3)
    document.add_paragraph(content)
