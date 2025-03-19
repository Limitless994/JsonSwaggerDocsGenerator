import json

def add_status_codes(document, responses, index, sub_index, sub_sub_index, swagger_data):
    sub_sub_sub_index = 1
    for status_code, response_details in responses.items():
        document.add_heading(f'{index}.{sub_index}.{sub_sub_index}.{sub_sub_sub_index} Status Code {status_code}', level=4)
        example_json = response_details.get('examples', {}).get('application/json', None)
        if not example_json:
            schema = response_details.get('schema', {})
            if schema.get('type') == 'array' and 'items' in schema:
                schema_ref = schema['items'].get('$ref', '')
            else:
                schema_ref = schema.get('$ref', '')
            if schema_ref:
                schema_name = schema_ref.split('/')[-1]
                example_json = generate_example_from_schema(swagger_data.get('definitions', {}).get(schema_name, {}), swagger_data.get('definitions', {}))
                if schema.get('type') == 'array':
                    example_json = [example_json]  
        if example_json:
            document.add_paragraph(json.dumps(example_json, indent=2))
        else:
            description = response_details.get('description', 'No description provided')
            document.add_paragraph(description)
        sub_sub_sub_index += 1
    return sub_sub_index

def add_response_example(document, method_details, swagger_data, index, sub_index, sub_sub_index):
    document.add_heading(f'{index}.{sub_index}.{sub_sub_index} Response Example', level=3)
    responses = method_details.get('responses', {})
    sub_sub_index = add_status_codes(document, responses, index, sub_index, sub_sub_index, swagger_data)
    return sub_sub_index + 1

def generate_example_from_schema(schema, definitions):
    if 'properties' not in schema:
        return {}
    example = {}
    for prop, details in schema['properties'].items():
        if 'type' in details:
            if details['type'] == 'string':
                example[prop] = 'string'
            elif details['type'] == 'integer':
                example[prop] = 123  
            elif details['type'] == 'boolean':
                example[prop] = True
            elif details['type'] == 'array':
                if 'items' in details and 'type' in details['items']:
                    if details['items']['type'] == 'string':
                        example[prop] = ['string']
                    elif details['items']['type'] == 'integer':
                        example[prop] = [123]
                    elif details['items']['type'] == 'boolean':
                        example[prop] = [True]
                    elif details['items']['type'] == 'object':
                        example[prop] = [generate_example_from_schema(details['items'], definitions)]
                elif 'items' in details and '$ref' in details['items']:
                    ref_name = details['items']['$ref'].split('/')[-1]
                    example[prop] = [generate_example_from_schema(definitions.get(ref_name, {}), definitions)]
            elif details['type'] == 'object':
                example[prop] = generate_example_from_schema(details, definitions)
        elif '$ref' in details:
            ref_name = details['$ref'].split('/')[-1]
            example[prop] = generate_example_from_schema(definitions.get(ref_name, {}), definitions)
    return example
