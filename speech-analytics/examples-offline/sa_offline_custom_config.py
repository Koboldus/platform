from configparser import ConfigParser
import requests
import time
import os
import json
import re
dir_path = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser()
config.read(os.path.join(dir_path, 'config.ini'))

conf = config['DEFAULT']['CONFIG']
jwt = config[conf]['JWT']
url = config[conf]['PROTOCOL'] + '://' + config[conf]['HOSTPORT'] + '/' + config[conf]['URLSUFFIX']
file_name = re.sub("[^A-Za-z0-9]+", "-", config['DEFAULT']['INPUTFILE'])
audio = os.path.join(dir_path, config['DEFAULT']['INPUTFILE'])
max_polls = int(config['DEFAULT']['MAX_POLLS'])
sleep_time = int(config['DEFAULT']['SLEEP_TIME'])


sa_config_body = {
    "name": 'sa_config_name_1',
    "sentiment": True,
    "summary": False,
    "wordCloud": False,
    "gender": True,
    "age": False,
    "profanity": True,    
    "overtalkTotalPercentageThreshold": 1.0,
    "overtalkSingleDurationMaximumThreshold": 1,
    "silenceTotalPercentageThreshold": 10.0,
    "silenceSingleDurationMaximumThreshold": 3,
    "moods": [
        "anger"
    ],
    "entities": [
        "ADDRESS",
        "PHONE",
        "PERSON",
        "MONEY",
        "DATE",
        "TIME"
    ],
    "keywords": [
        {
            "tag": "CANCEL",
            "examples": [
                {
                    "phrase": "cancel",
                    # "usage": null
                }
            ],
            "expand": False,
            "hide": False
        },
        {
            "tag": "EXPENSIVE",
            "examples": [
                {"phrase": "expensive"}, {"phrase": "pricey"}, {"phrase": "costs a lot"}
            ],
            "expand": False,
            "hide": False
        }
    ],
    "phrases": [
        {
            "tag": "AGENT_GREETING",
            "builtIn": False,
            "examples": [
                {
                    "sentence": "hello, good morning my name is Jane",
                    "sensitivity": 0.4
                },
                {
                    "sentence": "well, good morning my name is John",
                    "sensitivity": 0.4
                },
                {
                    "sentence": "good morning my name is Anne, I'll be happy",
                    "sensitivity": 0.4
                }
            ],
            "slots" : {
              "entities" : [
                {
                  "entity" : "PERSON",
                  "required" : True
                }
              ]
            },
             "location" : {
               "channel" : "agent",
               "time" : 20
            },
            "hideIfGroup": False
        },         
        {
            "tag": "ACCOUNT_VERIFY",
            "builtIn": False,
            "examples": [
                {
                    "sentence": "can you please verify your phone number for me",
                    "sensitivity": 0.75
                }
            ],
            "hideIfGroup": False
        },
        {
            "tag": "ANYTHING_ELSE_HELP",
            "builtIn": False,
            "examples": [
                {
                    "sentence": "is there anything else I can help you with",
                    "sensitivity": 0.75
                }
            ],
            "hideIfGroup": False
        },
        {
            "tag": "NOT_FUNCTIONING",
            "builtIn": False,
            "examples": [
                {
                    "sentence": "my radio quit working",
                    "sensitivity": 0.4
                },
                {
                    "sentence": "receiver doesn't work anymore",
                    "sensitivity": 0.6
                },     
                {
                    "sentence": "it is completely dead",
                    "sensitivity": 0.4
                },  
                {
                    "sentence": "it does not power on at all",
                    "sensitivity": 0.4
                }                  
            ],
            "hideIfGroup": False
        },
    ]
}
sa_config_id = None


audio_body = {
    'file': (file_name, open(audio, 'rb').read(), 'audio/wav'),
    'objectdata': (
        None,
        json.dumps({
            'name': file_name,
            'description' : file_name,
            'contentType' : 'audio/wav',
        }),
        'application/json'
    ),
}
audio_id = None


sa_session_body = {
    'label': 'test_sa_session',
    'saConfig': sa_config_id,
    'settings': {
        'asr': {
            'languages': ['en-us'],
            'sensitivity': 0.5,
            'speedVsAccuracy': 0.5,
        },
    },
    'tags': ['testing'],
    'audio': [{
        'source': {
            'dataObjectUuid': audio_id,
        },
    }],
}
sa_session_id = None

# Modify this to get the data you want. True means the data is returned, False means it is not.
sa_data_params = {
    'words': True,
    'audio': True,
    'meta': True,
    'wordcloud': True,
    'summary': True,
    'keywords': True,
    'entities': True,
    'phrases': True,
}

# Delete functions to clean up after the test
def delete_sa_config(id):
    delete_sa_config = requests.delete(
        url + '/sa/config/' + id,
        headers={'Authorization': jwt},
    )
    print('SA Config Deletion...')
    print(f'Status code: {delete_sa_config.status_code}')
    if delete_sa_config.status_code != 200:
        print(f'Info: {delete_sa_config.json()}')

def delete_audio(id):
    delete_audio = requests.delete(
        url + '/data/' + id,
        headers={'Authorization': jwt},
    )
    print('File Deletion...')
    print(f'Status code: {delete_audio.status_code}')
    if delete_audio.status_code != 200:
        print(f'Info: {delete_audio.json()}')

def delete_sa_session(id):
    while True:
        delete_sa_session = requests.delete(
            url + '/sa/offline/' + id,
            headers={'Authorization': jwt},
        )
        print('SA Session Deletion...')
        print(f'Status code: {delete_sa_session.status_code}')
        if delete_sa_session.status_code != 200:
            print(f'Info: {delete_sa_session.json()}')
            print('Sleeping for 10 seconds...')
            time.sleep(10)
        else:
            break


# Test function
def test(sa_config, audio, sa_session, sa_data):
    # 1. Create SA config
    create_sa_config = requests.post(
        url + '/sa/config',
        headers={'Authorization': jwt},
        json=sa_config,
    )

    print('SA Config Creation...')
    print(f'Status code: {create_sa_config.status_code}')

    if create_sa_config.status_code != 200:
        exit()
    
    print(f'Config ID: {create_sa_config.json()["saConfId"]}')
    sa_config_id = create_sa_config.json()['saConfId']

    # 2. Upload audio to datastore
    upload_audio = requests.post(
        url + '/data/file',
        headers={'Authorization': jwt},
        files=audio,
    )

    print('File Upload...')
    print(f'Status code: {upload_audio.status_code}')

    if upload_audio.status_code != 200:
        print(f'Info: {upload_audio.json()}')
        delete_sa_config(sa_config_id)
        exit()
        
    audio_id = upload_audio.json()['objectId']
    print(f'Audio ID: {audio_id}')

    # 3. Create SA session
    sa_session["audio"][0]["source"]["dataObjectUuid"] = audio_id

    create_sa_session = requests.post(
        url + '/sa/offline',
        headers={'Authorization': jwt},
        json=sa_session,
    )

    print('SA Session Creation...')
    print(f'Status code: {create_sa_session.status_code}')

    if create_sa_session.status_code != 200:
        print(f'Info: {create_sa_session.json()}')
        delete_sa_config(sa_config_id)
        delete_audio(audio_id)
        exit()

    print(f'SA Session ID: {create_sa_session.json()["saSessionId"]}')
    sa_session_id = create_sa_session.json()['saSessionId']

    # 4. Poll for SA session status until done or error
    print('Polling for SA session status...')
    polls = 0
    while True:
        polls += 1
        get_sa_session = requests.get(
            url + '/sa/offline/' + sa_session_id,
            headers={'Authorization': jwt},
        )

        if get_sa_session.status_code == 200:
            if get_sa_session.json()['progress']['phase'] == 'DONE':
                print('SA Session Done!')
                print(f'Status code: {get_sa_session.status_code}')
                #print(f'Info: {get_sa_session.json()}')
                break
            elif get_sa_session.json()['progress']['phase'] == 'ERROR':
                print('Error while processing SA session:')
                print(f'Status code: {get_sa_session.status_code}')
                print(f'Info: {get_sa_session.json()}')
                break
            else:
                print('SA Session still processing...')
                print(f'Status code: {get_sa_session.status_code}')
                #print(f'Info: {get_sa_session.json()}')
                print('Sleeping for 10 seconds...')
        else:
            print('Error getting SA session:')
            print(f'Status code: {get_sa_session.status_code}')
            print(f'Info: {get_sa_session.json()}')
            break

        if polls >= max_polls:
            print('Max number of polls reached. Deleting SA session...')
            delete_sa_session(sa_session_id)
            delete_audio(audio_id)
            delete_sa_config(sa_config_id)
            exit()
        
        time.sleep(sleep_time)

    # 5. Get SA session Data:
    if get_sa_session.status_code == 200:
        get_sa_session_data = requests.get(
            url + '/sa/offline/' + sa_session_id + '/data',
            headers={'Authorization': jwt},
            params=sa_data
        )

        print('Getting SA session data...')
        print(f'Status code: {get_sa_session_data.status_code}')
        print(f'Info: {get_sa_session_data.json()}')

    # 6. Final cleanup
    delete_sa_session(sa_session_id)
    delete_audio(audio_id)
    delete_sa_config(sa_config_id)
    print('Test complete!')

test(sa_config_body, audio_body, sa_session_body, sa_data_params)