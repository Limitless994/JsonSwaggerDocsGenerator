def add_general_section(document, swagger_data, index):
    try:
        if not swagger_data.get('info'):
            print("No 'info' section in swagger_data")
            return index
        document.add_heading(f'{index}. General', level=1)
        description = swagger_data.get('info', {}).get('description', 'Not specified')
        document.add_heading(f'{index}.1 Description', level=2)
        document.add_paragraph(description)
        return index + 1
    except Exception as e:
        print(f"Error in add_general_section: {e}")
        return index
