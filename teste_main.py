import os, json, requests, tools
from openai import OpenAI
print("Hello World with AI!! 0.8")

#Variaveis
debug = False
verbose = False
sair = False
reasoning_effort="minimal"
modelo = "muse-spark-1.3-contributor"

#Contador tokens
def cont_token(text):
    tokens = requests.post(
        "https://api.meta.ai/v1/responses/input_tokens",
        headers={
            "Authorization": f"Bearer[{os.environ['MODEL_API_KEY']}]",
            "Content-Type": "application/json",
        },
        json={
            "model": modelo,
            "input": text
        }
    )
    tokens.raise_for_status()
    return (tokens.json()["input_tokens"])
#Memorias funções
def read_chat():
    with open("chat_mem.json", "r", encoding="utf-8", errors="surrogateescape") as arquivo:
        return json.load(arquivo)
    
def read_mem():
    with open("mem.txt", "r", encoding="utf-8", errors="surrogateescape") as arquivo:
        return arquivo.read()
    
def add_chat(role, text):
    with open("chat_mem.json", "r", encoding="utf-8", errors="surrogateescape") as arquivo:
        h = json.load(arquivo)
    h.append(
        {"role":role, "content": [{"type":("output_text" if role == "assistant" else "input_text"),"text":text}]}
    )
    with open("chat_mem.json", "w", encoding="utf-8", errors="surrogateescape") as arquivo:
        json.dump(h, arquivo, ensure_ascii=False, indent=4)

def write_mem(text):
    with open("mem.txt", "w", encoding="utf-8", errors="surrogateescape") as arquivo:
        arquivo.write(text)

def reset_chat(entrada=None):
    if entrada == None: entrada = "Você é um assistente geral, seu nome é Pietro,você é curto e direto ao ponto"
    with open("chat_mem.json", "w", encoding="utf-8", errors="surrogateescape") as arquivo:
        json.dump([{"role": "developer","content": [{"type": "input_text","text": entrada}]}], arquivo, ensure_ascii=False, indent=4)

#CORES Ui Ui Ui
CINZA = "\033[90m"
NEGRITO = "\033[1m"
ITALICO = "\033[3m"
RESET = "\033[0m"

#cliente = Para quem mandar a mensagem?
try:
    client = OpenAI(
        api_key = os.environ["MODEL_API_KEY"],
        base_url="https://api.meta.ai/v1",
        )
except KeyError:
    print("SEM META API")
    print("Progama finalizado.")
    exit()

#mensagem para AI
def api_input(txt, responseid=None):
    #manda para AI
    if debug: print(f"{CINZA}{ITALICO}Debug: API request{RESET}")

    if cont_token(txt) >= 1000000: print("PASSOU DO LIMITEE")

    if responseid == None:
        response = client.responses.create(
            model=modelo,
            reasoning = {"effort": reasoning_effort}, 
            input = txt,
            tools=tools.list,
            )
    else:
        response = client.responses.create(
            model=modelo,
            reasoning = {"effort": reasoning_effort},
            input = txt,
            previous_response_id=responseid,
            tools=tools.list,
            )
    return response
#loop PRINCIPAL
while True:
    entrada = input("Entrada: ")
    #comandos --<==================>--
    if entrada.startswith("/"): 
        entrada = entrada.lower()
        if entrada == "/": print("Comandos:\n/sair\n/debug\n/verbose\n/reasoning\n/reset chat\n/developer"); continue
        elif entrada == "/sair":sair = True; break
        elif entrada == "/debug": print("/debug true\n/debug false"); continue
        elif entrada == "/debug true": debug = True; continue
        elif entrada == "/debug false": debug = False; continue
        elif entrada == "/verbose": print("/verbose true\n/verbose false"); continue
        elif entrada == "/verbose true": verbose = True; continue
        elif entrada == "/verbose false": verbose = False; continue
        elif entrada == "/reasoning": print("/reasoning minimal (defalt)\n/reasoning low\n/reasoning medium\n/reasoning high\n/reasoning xhigh"); continue
        elif entrada == "/reasoning minimal": reasoning_effort = "minimal"; continue
        elif entrada == "/reasoning low": reasoning_effort = "low"; continue
        elif entrada == "/reasoning medium": reasoning_effort = "medium"; continue
        elif entrada == "/reasoning high": reasoning_effort = "high"; continue
        elif entrada == "/reasoning xhigh": reasoning_effort = "xhigh"; continue
        elif entrada == "/reset chat": reset_chat(); continue
        elif entrada == "/developer": print("/deveoper Mensagem do sistema aqui"); continue
        elif entrada.startswith("/developer") and entrada != "/developer": reset_chat(entrada.removeprefix("/developer")); print(f"Set to: {entrada.removeprefix("/developer")}"); continue
        else: print("Comando não encontrado"); continue
    #salvar no chat
    add_chat("user", entrada)
    #mandar para a AI-------------------
    response = api_input(read_chat())

    #vê se a AI pediu uma ferramenta
    while True:
        resultados_tools =[]

        for item in response.output:
            if item.type == "function_call":

                if item.name in tools.dic:
                    args = json.loads(item.arguments)
                    funcao =  tools.dic[item.name]
                    result = funcao(**args)
                    add_chat("system", f"tool use: {item.name},arguments: {args} results: {result}")
                    if debug: print(f"{CINZA}{ITALICO}Debug: tool use {item.name}, {args}{RESET}")

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
        response = api_input(resultados_tools, response.id)

    add_chat("assistant", response.output_text)

    print(response.output_text)
    if verbose:
        print(f'''
{CINZA}verbose:
Model: {response.model}
reasoning: {reasoning_effort}
''')
        if response.usage is not None:
            print(f'''
input tokens: {response.usage.input_tokens}
output tokens: {response.usage.output_tokens}{RESET}
''')
        else: print("erro: sem uso de tokens")

print("Progama finalizado.")