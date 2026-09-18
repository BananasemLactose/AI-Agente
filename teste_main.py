import os, json 
from openai import OpenAI
print("Hello World with AI!! 1.3")

#Variaveis
debug = False
verbose = False
sair = False
reasoning_effort="minimal"
modelo = "muse-spark-1.3-contributor"

#Memorias funções
def read_chat():
    with open("chat.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    
def read_mem():
    with open("mem.txt", "r", encoding="utf-8") as arquivo:
        return arquivo.read()
    
def add_chat(role, text):
    with open("chat.json", "r", encoding="utf-8") as arquivo:
        h = json.load(arquivo)
    h.append(
        {"role":role, "content": [{"type":("output_text" if role == "assistant" else "input_text"),"text":text}]}
    )
    with open("chat.json", "w", encoding="utf-8") as arquivo:
        json.dump(h, arquivo, ensure_ascii=False, indent=4)

def write_mem(text):
    with open("mem.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(text)

#CORES Ui Ui Ui
CINZA = "\033[90m"
NEGRITO = "\033[1m"
ITALICO = "\033[3m"
RESET = "\033[0m"

#ferramentas codigo-------------
def c_arquivo(content, name):
    with open("Agent-work/"+name, "w",encoding="utf-8") as arquivo:
        arquivo.write(content)
    return{"status": "sucess", "name": name}
    
#ferramentas descrição------------
tools=[
        {
            "type": "function",
            "name": "c_arquivo",
            "description": "Cria um arquivo contendo texto dentro, podendo ser scrips como arquivo.py por exemplo",
            "parameters": {"type": "object", "properties":{"content":{"type": "string", "description": "O texto dentro do arquivo"}, "name": {"type": "string", "description": "o nome do arquivo, por exemmplo: main.py ou documento.txt"}}, "required": ["name", "content"]}
        }
    ]

#Dicionario com comandos (UAUUUU!!!!!)
funcoes = {
    "c_arquivo":c_arquivo
}
#cliente = Para quem mandar a mensagem?
client = OpenAI(
    api_key = os.environ["MODEL_API_KEY"],
    base_url="https://api.meta.ai/v1",
    )

#loop PRINCIPAL
while True:
    entrada = input("Entrada: ")

#comandos --<==================>--
    if entrada.startswith("/"):
        if entrada == "/": print("Comandos:\n/sair\n/debug\n/verbose\n/reasoning"); continue
        elif entrada == "/sair":sair = True; break
        elif entrada == "/debug": print("/debug True\n/debug False"); continue
        elif entrada == "/debug True": debug = True; continue
        elif entrada == "/debug False": debug = False; continue
        elif entrada == "/verbose": print("/verbose True\n/verbose False"); continue
        elif entrada == "/verbose True": verbose = True; continue
        elif entrada == "/verbose False": verbose = False; continue
        elif entrada == "/reasoning": print("/reasoning minimal (defalt)\n/reasoning low\n/reasoning medium\n/reasoning high\n/reasoning xhigh"); continue
        elif entrada == "/reasoning minimal": reasoning_effort = "minimal"; continue
        elif entrada == "/reasoning low": reasoning_effort = "low"; continue
        elif entrada == "/reasoning medium": reasoning_effort = "medium"; continue
        elif entrada == "/reasoning high": reasoning_effort = "high"; continue
        elif entrada == "/reasoning xhigh": reasoning_effort = "xhigh"; continue
        else: print("Comando não encontrado"); continue
    #salvar no chat
    add_chat("user", entrada)
    #mandar para a AI-------------------
    if debug: print(f"{CINZA}{ITALICO}Debug: API request{RESET}")
    response = client.responses.create(
        model=modelo,
        reasoning = {"effort": reasoning_effort},
        input=read_chat(),
        tools=tools
    )
    #salva no chat
    add_chat("assistant", response.output_text)

    #vê se a AI pediu uma ferramenta
    while True:
        resultados_tools =[]

        for item in response.output:
            if item.type == "function_call":

                if item.name in funcoes:
                    args = json.loads(item.arguments)
                    funcao =  funcoes[item.name]
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
        reasoning = {"effort": reasoning_effort},
        input = resultados_tools,
        previous_response_id=response.id,
        tools=tools,
        )
    print(response.output_text)
    if verbose:
        print(f'''
{CINZA}verbose:
Model: {response.model}
reasoning: {reasoning}
input tokens: {response.usage.input_tokens}
output tokens: {response.usage.output_tokens}{RESET}''')

print("Progama finalizado.")