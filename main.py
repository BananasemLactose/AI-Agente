import os, json
from openai import OpenAI
print("Hello World with AI!! 1.2")
debug = False
verbose = False
sair = False
reasoning_effort="minimal"

#CORES Ui Ui Ui
CINZA = "\033[90m"
NEGRITO = "\033[1m"
ITALICO = "\033[3m"
RESET = "\033[0m"


modelo = "muse-spark-1.3-contributor"
#ferramentas codigo-------------
def clima(cidade):#dá o clima
    if debug:
        print(f"{CINZA}{ITALICO}Debug: tool clima usada{RESET}")
        print(f"{CINZA}{ITALICO}Debug: O modelo deu como cidade:{cidade}{RESET}")
    return {'Cidade': cidade, 'Clima': 'Chuvoso'}

def posicao():
    if debug:
        print(f"{CINZA}{ITALICO}Debug: tool posicao usada{RESET}")
    return {'Cidade': 'Campo Mourão'}

def temperatura(cidade):
    if debug:
        print(f"{CINZA}{ITALICO}Debug: tool temperatura usada{RESET}")
        print(f"{CINZA}{ITALICO}Debug: O modelo deu como cidade:{cidade}{RESET}")
    return {'Cidade': cidade, 'Temperatura':'22 ºC'}
#ferramentas descrição------------
tools=[
        {
            "type": "function", 
            "name": "clima", 
            "description": "Retorna o clma de uma cidade", 
            "parameters": {
                "type": "object",
                "properties": {"cidade":{"type": "string", "description": "Nome da cidade, exemplo: New_York"}},
                "required": ["cidade"]
            }
        },
        {
            "type": "function",
            "name": "posicao",
            "description": "Retorna a cidade do usuario",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "type": "function",
            "name": "temperatura",
            "description": "Retorna a temperatura de uma cidade neste momento",
            "parameters": {"type": "object", "properties":{"cidade":{"type": "string", "description":"Nome da cidade, exemplo New_York"}},"required":["cidade"]}
        }
    ]

#Dicionario com comandos (UAUUUU!!!!!)
funcoes = {
    "clima": clima,
    "posicao": posicao,
    "temperatura":temperatura
}
#cliente = Para quem mandar a mensagem?
client = OpenAI(
    api_key = os.environ["MODEL_API_KEY"],
    base_url="https://api.meta.ai/v1",
    )

#loop PRINCIPAL
while True:
    entrada = input("Entrada: ")
    #comandos---
    if entrada.startswith("/"):
        if entrada == "/": print("Comandos:\n/sair\n/debug\n/verbose\n/reasoning"); continue
        elif entrada == "/sair":sair = True; break
        elif entrada == "/debug": print("/debug True\n/debug False"); continue
        elif entrada == "/debug True": debug = True; continue
        elif entrada == "/debug False": debug = False; continue
        elif entrada == "/verbose": print("/verbose True\n/verbose False"); continue
        elif entrada == "/verbose True": verbose = True; continue
        elif entrada == "/verbose False": verbose = False; continue
        elif entrada == "/reasoning": print("/reasoning minimal (defalt)\n/reasoning low\n/reasoning medium\n/reasoning high\n/reasoning xhigh")
        elif entrada == "/reasoning minimal": reasoning_effort = "minimal"; continue
        elif entrada == "/reasoning low": reasoning_effort = "low"; continue
        elif entrada == "/reasoning medium": reasoning_effort = "medium"; continue
        elif entrada == "/reasoning high": reasoning_effort = "high"; continue
        elif entrada == "/reasoning xhigh": reasoning_effort = "xhigh"; continue
        else: print("Comando não encontrado"); continue
        

    #mandar para a AI-------------------
    if debug: print(f"{CINZA}{ITALICO}Debug: API request{RESET}")
    response = client.responses.create(
        model=modelo,
        input=entrada,
        tools=tools,
    )

    #vê se a AI pediu uma ferramenta
    while True:
        resultados_tools =[]

        for item in response.output:
            if item.type == "function_call":

                if item.name in funcoes:
                    args = json.loads(item.arguments)
                    funcao = funcoes[item.name]
                    result = funcao(**args)

                else: result = {'erro': "Ferramenta não encontrada"}

                resultados_tools.append(
                    {
                        "type":"function_call_output",
                        "call_id":item.call_id,
                        "output":json.dumps(result)
                    }
                )
        if not resultados_tools: break

        #manda para AI os resultados das tools
        if debug: print(f"{CINZA}{ITALICO}Debug: API request{RESET}")
        response = client.responses.create(
        model=modelo,
        input = resultados_tools,
        previous_response_id=response.id,
        tools=tools,
        reasoning_effort=reasoning_effort
        )
    print(response.output_text)
    if verbose:
        print(f'''
{CINZA}verbose:
Model: {response.model}
reasoning: {reasoning_effort}
input tokens: {response.usage.input_tokens}
output tokens: {response.usage.output_tokens}{RESET}''')

print("Progama finalizado")