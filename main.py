import subprocess, os, json
from datetime import datetime
import clickup_api_call, json_reader


def get_final_path(path):
    ultima_subpasta = path
    final_path = 0
    last_path = None

    for root, dirs, files in os.walk(path):
        # Calcula o nível de profundidade atual
        actual_path = root[len(path):].count(os.sep)

        # Atualiza a última subpasta se a profundidade atual for maior
        if actual_path > final_path:
            final_path = actual_path
            last_path = root

    return last_path


def translate_status(status_str):
    dict_status = {
        'Fail': 'Fail',
        'Skipped': 'Skip',
        'Open': 'Open',
        'Success': 'Pass'
    }
    if dict_status[status_str]:
        return dict_status[status_str]
    else:
        return 'Open'


def init_test_process(json_export_path):
    print(f'--------------------------------\nStart Unreal Functional Tests\n--------------------------------')
    # Chamada para início dos testes
    unreal_exe_path = r'C:/Program Files/Epic Games/UE_5.2/Engine/Binaries/Win64/UnrealEditor.exe'
    project_path = r'D:/Cybersims/cybersimsue5'

    # Remove os dados de testes antigos
    if os.path.isfile(project_path):
        os.remove(project_path)

    subprocess.call(f'"{unreal_exe_path}" "{project_path}/CyberSims.uproject" -ResolvingFutureDeprecations -EditPackages=Packages=Location:^"{project_path}/Content/_Core/Blueprints/Test/Test_UI.umap" -ExecCmds="Automation RunTests Functional; Quit" -ReportOutputPath="{json_export_path}" -log -command="stat StartFile=teste"')


def add_attachment_result(project_path, task_id, test_name):
    evidence_path = project_path + '/Saved/Automation/Reports/Test_UI'

    for folder in os.listdir(evidence_path):
        if test_name == folder:
            files_path = get_final_path(f'{evidence_path}/{folder}')

            # Faz o Upload de todas as imagens da pasta
            if files_path + '/Approved.png':
                clickup_api_call.include_attachment(task_id, files_path + '/Approved.png', test_name + ': Approved')
            if files_path + '/Delta.png':
                clickup_api_call.include_attachment(task_id, files_path + '/Delta.png', test_name + ': Delta')
            if files_path + '/Incoming.png':
                clickup_api_call.include_attachment(task_id, files_path + '/Incoming.png', test_name + ': Incoming')


def clickup_task_creator(json_export_path, project_path):
    print(f'--------------------------------\nStarting ClickUp Task Creation\n--------------------------------')
    str_datetime = datetime.today()
    main_test_name = 'Cyber Sims Unreal Automated Tests - ' + str_datetime.strftime("%Y/%m/%d - %H:%M")
    test_result = json_reader.read_test_json_data(json_export_path)['tests']

    # Criação da task principal
    main_task = json.loads(clickup_api_call.create_task_call(main_test_name,
                                                  'Testes automatizados via Unreal Driver Automation',
                                                  None, 'Testing'))
    main_task_id = main_task['id']
    for test in test_result:
        test_display_name = test['testDisplayName']
        test_status = translate_status(test['state'])
        test_duration = test['duration']
        test_message_type = test['entries'][0]['event']['type']
        test_message = test['entries'][0]['event']['message']

        # Criação da Subtask
        subtask_response = json.loads(clickup_api_call.create_task_call(test_display_name, f'Test status: {test_status}\nTest message: {test_message}\nTest duration: {test_duration}', main_task_id, test_status))

        # Adiciona as evidências de teste
        add_attachment_result(project_path, subtask_response['id'], test_display_name)

        # Mostra o status dos testes executados
        print(f'name: {test_display_name}\nstatus: {test_status}\nduration: {test_duration}\nmessageType: {test_message_type}\nmessage: {test_message}\n---------------------------')


if __name__ == '__main__':
    project_path = r'D:/Cybersims/cybersimsue5'
    init_test_process(r'D:/temp')
    clickup_task_creator(r'D:/temp/index.json', project_path)
