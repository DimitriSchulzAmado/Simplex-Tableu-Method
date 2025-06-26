import pulp as plp

from data.app_state import ObjectiveFunctionState, ObjectiveFunctionType, ConstraintSymbol


class SimplexTableau:
    def __init__(self):
        self._model: plp.LpProblem

    def build(self, problem: ObjectiveFunctionState):
        """"
        Build the simplex tableau for the given linear programming problem.
        
        :param problem: An instance of ObjectiveFunctionState containing the problem definition.
        """
        objective = plp.LpMaximize
        match problem.objective_function:
            case ObjectiveFunctionType.MAXIMIZE:
                objective = plp.LpMaximize
            case ObjectiveFunctionType.MINIMIZE:
                objective = plp.LpMinimize
            case _:
                raise ValueError("Invalid objective function type")

        ppl = plp.LpProblem("Simplex Problem", objective)

        variables: list[plp.LpVariable] = []
        for variable in problem.variables:
            var = plp.LpVariable(variable.name, lowBound=0)
            variables.append(var)

        # Define the objective function
        ppl += plp.lpSum(coefficient.value * var for coefficient, var in zip(problem.variables, variables))

        # Define the constraints
        for constraint in problem.constraints:
            match constraint.symbol:
                case ConstraintSymbol.LESS_THAN_OR_EQUAL:
                    ppl += plp.lpSum(coefficient.value * var for coefficient, var in zip(constraint.variables, variables)) <= constraint.value
                case ConstraintSymbol.GREATER_THAN_OR_EQUAL:
                    ppl += plp.lpSum(coefficient.value * var for coefficient, var in zip(constraint.variables, variables)) >= constraint.value
                case ConstraintSymbol.EQUAL:
                    ppl += plp.lpSum(coefficient.value * var for coefficient, var in zip(constraint.variables, variables)) == constraint.value
                case _:
                    raise ValueError("Invalid constraint type")
        
        # Store the model in the instance variable
        # This allows the tableau to be used later for solving or extracting results
        self._model = ppl

    def solve(self):
        """
        Solve the linear programming problem using the simplex method.
        
        :return: The status of the solution.
        """
        self._model.solve()
        return plp.LpStatus[self._model.status]

    def get_solution(self):
        return {
            "status": plp.LpStatus[self._model.status],
            "objective_value": plp.value(self._model.objective),
            "variables": {v.name: v.varValue for v in self._model.variables()}
        }

    def get_objective_value(self):
        return plp.value(self._model.objective)

    def is_optimal(self):
        return plp.LpStatus[self._model.status] == "Optimal"