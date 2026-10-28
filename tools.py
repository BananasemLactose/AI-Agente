#ferramentas codigo-------------
def c_arquivo(content, name):
    "cria um arquivo"
    with open("Agent-work/"+name, "w",encoding="utf-8", errors="surrorgateescape") as arquivo:
        arquivo.write(content)
    return{"status": "sucess", "name": name}

def r_arquivo(name):
    "le o conteudo do arquivo"
    with open("Agent-work/"+name, "r",encoding="utf-8", errors="surrorgateescape") as arquivo:
        content = arquivo.read()
    return{"status": "sucess", "name": name, "content": content}

def l_arquivos():
    "lista de arquivos"
    arquivos = os.listdir("Agent-work/")
    return {"status": "sucess", "arquivos": arquivos}

def e_arquivo(content, name):
    "edita um arquivo existent"
    with open("Agent-work/"+name, "w", encoding="utf-8", errors="surrogateescape") as arquivo:
        arquivo.write(content)
    return {"status": "sucess", "name": name}

list=[
        {
            "type": "function",
            "name": "c_arquivo",
            "description": "Cria um arquivo contendo texto dentro, podendo ser scrips como arquivo.py por exemplo",
            "parameters": {"type": "object", "properties":{"content":{"type": "string", "description": "O texto dentro do arquivo"}, "name": {"type": "string", "description": "o nome do arquivo, por exemmplo: main.py ou documento.txt"}}, "required": ["name", "content"]}
        },
        {
            "type": "function",
            "name": "r_arquivo",
            "description": "Lê o conteúdo de um arquivo existente",
            "parameters": {"type": "object", "properties":{"name":{"type": "string", "description": "o nome do arquivo a ser lido"}}, "required": ["name"]}
        },
        {
            "type": "function",
            "name": "l_arquivos",
            "description": "Lista os arquivos existentes",
            "parameters": {"type": "object", "properties":{}}
        },
        {
            "type": "function",
            "name": "e_arquivo",
            "description": "Edita o conteúdo de um arquivo existente",
            "parameters": {"type": "object", "properties":{"content":{"type": "string", "description": "O novo conteúdo do arquivo"}, "name":{"type": "string", "description": "o nome do arquivo a ser editado"}}, "required": ["name", "content"]}
        }
    ]