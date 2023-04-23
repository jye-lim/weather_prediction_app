import base64

def get_download_link(file, file_name, text):
    if file_name.split('.')[-1] == 'csv':
        file = file.to_csv(index=False)
    b64 = base64.b64encode(file.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{text}</a>'
