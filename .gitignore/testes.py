name = "aa.py"
with open("Agent-work/"+name, "r",encoding="utf-8") as arquivo:
    print({"name": name, "content": arquivo.read()})