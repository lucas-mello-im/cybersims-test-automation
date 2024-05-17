import time
import requests
import json


def create_task_call(task_title, task_description, subtask_parent, test_status):
    url = r"https://api.clickup.com/api/v2/list/901303466063/task"
    date_time = time.time_ns()

    payload = json.dumps({
      "name": task_title,
      "description": task_description,
      "status": test_status,
      "due_date": None,
      "due_date_time": False,
      "start_date": date_time,
      "start_date_time": True,
      "notify_all": True,
      "parent": subtask_parent,
      "links_to": None,
      "custom_fields": [
          {
              "id": "455117d3-1e73-4eed-aa26-4d5878f6f2ef",
              "value": 0
          },
          {
              "id": "d8cc81da-8411-46a1-a3bc-a983a3324daa",
              "value": 21
          }
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'pk_72864112_7QTNGFNSDVA77FOAPXS8COXWIVMQBIX8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def include_attachment(task_id, attachment_path, image_name):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/attachment"

    payload = {}
    files=[('attachment',(f'{image_name}.png',open(f'{attachment_path}','rb'),'image/png'))]
    headers = {
      'Authorization': 'pk_72864112_7QTNGFNSDVA77FOAPXS8COXWIVMQBIX8'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.text
