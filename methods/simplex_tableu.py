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

    def get_shadow_prices(self):
        """
        Get the shadow prices (dual values) for each constraint.
        
        :return: A dictionary of constraint names and their shadow prices.
        """
        shadow_prices = {}
        for name, constraint in self._model.constraints.items():
            shadow_prices[name] = constraint.pi
        return shadow_prices

    def get_detailed_shadow_price_analysis(self):
        """
        Get detailed shadow price analysis including variation limits.
        
        :return: A dictionary with detailed analysis for each constraint.
        """
        try:
            constraint_names = list(self._model.constraints.keys())
            analysis_results = {}
            
            for i, name in enumerate(constraint_names):
                constraint = self._model.constraints[name]
                # O RHS original é o negativo da constante no PuLP
                original_rhs = -constraint.constant if constraint.constant is not None else 0
                # Preço-sombra vem diretamente do PuLP - usar o valor absoluto se necessário
                shadow_price_raw = constraint.pi if constraint.pi is not None else 0
                
                # Corrigir preços-sombra negativos pequenos (problemas de precisão numérica)
                if abs(shadow_price_raw) < 1e-6:
                    shadow_price = 0.0
                else:
                    # Para problemas de maximização, o preço-sombra já vem com o sinal correto
                    shadow_price = shadow_price_raw
                
                # Calcular limites de variação usando análise de sensibilidade básica
                max_increase, max_decrease = self._calculate_rhs_limits(name, original_rhs)
                
                analysis_results[name] = {
                    "constraint_name": name,
                    "original_rhs": original_rhs,
                    "shadow_price": shadow_price,
                    "max_increase": max_increase,
                    "max_decrease": max_decrease,
                    "valid_range_min": original_rhs - max_decrease,
                    "valid_range_max": original_rhs + max_increase
                }
            
            return analysis_results
        except Exception as e:
            print(f"Erro na análise de preços-sombra: {e}")
            return {}

    def _calculate_rhs_limits(self, constraint_name: str, original_rhs: float):
        """
        Calcula os limites de variação para o RHS de uma restrição.
        
        :param constraint_name: Nome da restrição
        :param original_rhs: Valor original do RHS
        :return: Tupla (max_increase, max_decrease)
        """
        try:
            # Testes incrementais para encontrar limites
            test_increases = [1, 5, 10, 20, 50, 100]
            test_decreases = [1, 5, 10, 20, 50, 100]
            
            max_increase = 0
            max_decrease = 0
            
            original_constraint = self._model.constraints[constraint_name]
            original_constant = original_constraint.constant
            
            # Testar aumentos
            for increase in test_increases:
                try:
                    # Aplicar aumento temporário
                    original_constraint.constant = original_constant - increase
                    
                    # Testar se ainda é viável
                    status = self._model.solve()
                    
                    if status == plp.LpStatusOptimal:
                        max_increase = increase
                    else:
                        break
                finally:
                    # Restaurar valor original
                    original_constraint.constant = original_constant
            
            # Testar reduções
            for decrease in test_decreases:
                try:
                    # Aplicar redução temporária
                    original_constraint.constant = original_constant + decrease
                    
                    # Testar se ainda é viável
                    status = self._model.solve()
                    
                    if status == plp.LpStatusOptimal:
                        max_decrease = decrease
                    else:
                        break
                finally:
                    # Restaurar valor original
                    original_constraint.constant = original_constant
            
            # Re-resolver o problema original para garantir que está no estado correto
            self._model.solve()
            
            return max_increase, max_decrease
            
        except Exception as e:
            print(f"Erro no cálculo de limites para {constraint_name}: {e}")
            return 10.0, 10.0  # Valores padrão

    def _find_max_rhs_change(self, constraint_name: str, direction: str = "increase", max_test_value: float = 1000):
        """
        Find the maximum change in RHS value before the solution becomes infeasible.
        
        :param constraint_name: Name of the constraint to analyze
        :param direction: "increase" or "decrease"
        :param max_test_value: Maximum value to test
        :return: Maximum change allowed
        """
        original_constraint = self._model.constraints[constraint_name]
        original_constant = original_constraint.constant
        
        # Binary search to find maximum change
        if direction == "increase":
            low, high = 0, max_test_value
        else:
            low, high = 0, max_test_value
        
        max_valid_change = 0
        
        # Test changes incrementally
        test_values = [1, 5, 10, 25, 50, 100, 250, 500, 1000]
        
        for test_change in test_values:
            try:
                # Apply test change
                if direction == "increase":
                    original_constraint.constant = original_constant - test_change
                else:
                    original_constraint.constant = original_constant + test_change
                
                # Test solve
                temp_status = self._model.solve()
                
                if temp_status == plp.LpStatusOptimal:
                    max_valid_change = test_change
                else:
                    break
                    
            except:
                break
            finally:
                # Restore original
                original_constraint.constant = original_constant
        
        return max_valid_change

    def get_reduced_costs(self):
        """
        Get the reduced costs for each variable.
        
        :return: A dictionary of variable names and their reduced costs.
        """
        reduced_costs = {}
        for v in self._model.variables():
            reduced_costs[v.name] = v.rc
        return reduced_costs

    def analyze_change_viability(self, changed_problem: ObjectiveFunctionState):
        """
        Analyze the viability of changes by re-solving the problem with modified parameters.
        This is a simplified approach and might need more sophisticated sensitivity analysis for real-world scenarios.
        
        :param changed_problem: A new ObjectiveFunctionState with the proposed changes.
        :return: A dictionary containing viability status, new optimal profit, and shadow price validity limits.
        """
        original_objective_value = plp.value(self._model.objective)
        
        # Create a new SimplexTableau instance for the changed problem
        changed_tableau = SimplexTableau()
        changed_tableau.build(changed_problem)
        changed_tableau.solve()

        new_objective_value = plp.value(changed_tableau._model.objective)
        
        is_viable = changed_tableau.is_optimal()
        
        # For shadow price validity limits, a more in-depth sensitivity analysis is needed.
        # PuLP provides some basic sensitivity analysis, but full range calculation is complex.
        # For this implementation, we'll indicate that a more detailed analysis is required.
        shadow_price_validity_limits = {"note": "Detailed shadow price validity limits require advanced sensitivity analysis not fully supported by basic PuLP output for all cases."}

        return {
            "is_viable": is_viable,
            "new_optimal_profit": new_objective_value,
            "original_optimal_profit": original_objective_value,
            "shadow_price_validity_limits": shadow_price_validity_limits
        }

    def analyze_resource_availability_change(self, new_constraint_values: list[float]):
        """
        Analyze the viability of changes in resource availability (RHS values).
        
        :param new_constraint_values: List of new constraint values in the same order as the original constraints.
        :return: Dictionary containing viability status and new optimal value.
        """
        # Store original constraint values
        original_constraints = []
        constraint_names = list(self._model.constraints.keys())
        
        # Store original RHS values
        for name in constraint_names:
            original_constraints.append(self._model.constraints[name].constant)
        
        try:
            # Update constraint values
            for i, name in enumerate(constraint_names):
                if i < len(new_constraint_values):
                    # Update the constraint's RHS value
                    constraint = self._model.constraints[name]
                    # For PuLP, we need to modify the constraint expression
                    # This is a simplified approach - in practice, you might need to rebuild the model
                    constraint.constant = -new_constraint_values[i]
            
            # Solve with new values
            original_objective = plp.value(self._model.objective)
            self._model.solve()
            new_objective = plp.value(self._model.objective)
            
            is_viable = self._model.status == plp.LpStatusOptimal
            
            # Restore original values
            for i, name in enumerate(constraint_names):
                self._model.constraints[name].constant = original_constraints[i]
            
            return {
                "is_viable": is_viable,
                "new_optimal_value": new_objective if is_viable else None,
                "original_optimal_value": original_objective,
                "status": plp.LpStatus[self._model.status]
            }
            
        except Exception as e:
            # Restore original values in case of error
            for i, name in enumerate(constraint_names):
                self._model.constraints[name].constant = original_constraints[i]
            
            return {
                "is_viable": False,
                "new_optimal_value": None,
                "original_optimal_value": plp.value(self._model.objective),
                "status": f"Error: {str(e)}"
            }


