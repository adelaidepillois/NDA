import requests
from nda import get_patient_data
from json import dumps

TOKEN = 'C4A5D3539A66E2091056BAA2DD9DC6E2'
URL = 'https://ihuredcap.chu-bordeaux.fr/api/'


def get_nda_list():
    data = {
        'token': TOKEN,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'fields': 'nda,record_id,patient_complete',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    r = requests.post(URL, data)
    r.raise_for_status()

    return r.json()


def update_data(input_data):
    data = {
        'token': TOKEN,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'overwriteBehavior': 'overwrite',
        'forceAutoNumber': 'false',
        'data': dumps(input_data),
        'returnContent': 'count',
        'returnFormat': 'json',
    }
    r = requests.post(URL, data)
    r.raise_for_status()

    return r.json()


def update_all_data():
    nda_list = get_nda_list()
    all_patient_data = []
    for record in nda_list:
        if record['patient_complete'] != '0':
            continue
        # Get the patient data
        patient_data = get_patient_data(record['nda'])
        f_patient_data = {
            'record_id': record['record_id'],
            'nda': patient_data['nda'],
            'nip': patient_data['nip'],
            'nom': patient_data['nom'],
            'prenom': patient_data['prenom'],
            'nom_naissance': patient_data['patronyme'],
            'ddn': patient_data['dateNaissance'],
            'sexe': patient_data['sexe'],
            'patient_complete': '1'
        }
        all_patient_data.append(f_patient_data)

    # Overwrite the database
    update_data(all_patient_data)


if __name__ == '__main__':
    update_all_data()
