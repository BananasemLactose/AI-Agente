def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        return "Erro: divisão por zero"
    return a / b

def calculadora():
    print("Calculadora Simples")
    print("Operações: + - * /")
    print("Digite 'sair' para encerrar")
    while True:
        op = input("\nDigite a operação (+, -, *, /) ou 'sair': ")
        if op.lower() == "sair":
            break
        if op not in ["+", "-", "*", "/"]:
            print("Operação inválida")
            continue
        try:
            n1 = float(input("Primeiro número: "))
            n2 = float(input("Segundo número: "))
        except ValueError:
            print("Número inválido")
            continue
        if op == "+":
            print("Resultado:", somar(n1, n2))
        elif op == "-":
            print("Resultado:", subtrair(n1, n2))
        elif op == "*":
            print("Resultado:", multiplicar(n1, n2))
        elif op == "/":
            print("Resultado:", dividir(n1, n2))

calculadora()