import os, json
from openai import OpenAI
print("Hello World with AI!! 2.0")

entrada = input("Entrada: ")
modelo = "muse-spark-1.3-contributor"
#ferramentas codigo-------------
def clima(cidade):#dá o clima
    
    print(f"Debug: O modelo deu como cidade:{cidade}")
    return {'Cidade': cidade, 'Clima': 'Chuvoso', 'Temperatura': '19 ºC'}

def posicao():
    return {'Cidade': 'Campo Mourão'}
#ferramentas descrição------------
tools=[
        {
            "type": "function", 
            "name": "clima", 
            "description": "Retorna o clma e a temperatura de uma cidade", 
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
        }
    ]

#Dicionario com comandos (UAUUUU)
funcoes = {
    "clima": clima,
    "posicao": posicao
}

#mandar para a AI-------------------
client = OpenAI(
    api_key = os.environ["MODEL_API_KEY"],
    base_url="https://api.meta.ai/v1",
)
response = client.responses.create(
    model=modelo,
    input=entrada,
    tools=tools,
)

#vê se a AI pediu uma ferramenta

while True:
    tool_chamada = False

    for item in response.output:
        if item.type == "function_call":

            tool_chamada = True

            if item.name in funcoes:
                args = json.loads(item.arguments)
                funcao = funcoes[item.name]
                result = funcao(**args)

            else: result = {'erro': "Ferramenta não encontrada"}

                #manda devolta para a AI a resposta da ferramenta
            response = client.responses.create(
                model=modelo,
                input = [
                    {
                    "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(result),
                    }
                ],
                previous_response_id=response.id,
                tools=tools,
            )
    if not tool_chamada: break

print(response.output_text)