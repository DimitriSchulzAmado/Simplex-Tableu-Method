import pulp as plp
import pandas as pd


def main():
    # Define o objeto do problema
    max_or_min = input("Deseja maximizar ou minimizar? ('max' para maximizar, 'min' para minimizar): ")

    sense = {'max': plp.LpMaximize, 'min': plp.LpMinimize}.get(max_or_min)
    ppl = plp.LpProblem("Example_Problem", sense)

    # define a quantidade de variáveis
    quantity = int(input("Entre com a quantidade de variáveis: "))

    if quantity <= 1 or quantity > 4:
        print("A quantidade de variáveis deve ser 2,3 ou 4.")
        return

    # Define o valor das variaveis
    variables = []
    for i in range(quantity):
        input_data = input(f"Entre com o nome da variável {i + 1}: ")
        var = plp.LpVariable(input_data, lowBound=0)
        variables.append(var)

    # Define a função objetivo
    ppl += 50*variables[0] + 70*variables[1] + 100*variables[2]

    # Define as restrições (constraints)
    ppl += variables[0] <= 4
    ppl += variables[1] <= 8
    ppl += variables[2] <= 3
    ppl += variables[0] + variables[1] + variables[2] <= 10
    ppl += variables[0] + 2*variables[1] + 3*variables[2] <= 18

    # Solução do problema
    ppl.solve()

    # Exibe o status da solução
    for var in variables:
        print(var.varValue)
    plp.value(ppl.objective)

    # Exibe o nome das variaveis, preço sombra e o quanto sobrou
    o = [
        {
            'name': name,
            'shadow price': c.pi,
            'slack': c.slack
        }
        for name, c in ppl.constraints.items()
    ]
    print(pd.DataFrame(o))


if __name__ == "__main__":
    main()
