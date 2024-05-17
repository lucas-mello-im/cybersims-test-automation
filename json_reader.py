import json


def read_test_json_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Verifica se o arquivo está vazio
            if not content.strip():
                raise ValueError("O arquivo JSON está vazio.")

            # Remove a BOM se estiver presente
            if content.startswith('\ufeff'):
                content = content[1:]
            data = json.loads(content)
        return data

    except FileNotFoundError:
        print(f"Arquivo não encontrado no caminho especificado: {path}")
    except ValueError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Um erro ocorreu: {e}")