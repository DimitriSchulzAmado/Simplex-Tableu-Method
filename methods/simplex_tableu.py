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
        Get detailed shadow price analysis.
        
        :return: A dictionary with detailed analysis for each constraint.
        """
        try:
            constraint_names = list(self._model.constraints.keys())
            analysis_results = {}
            
            for i, name in enumerate(constraint_names):
                constraint = self._model.constraints[name]
                original_rhs = -constraint.constant if constraint.constant is not None else 0
                shadow_price_raw = constraint.pi if constraint.pi is not None else 0
                
                if abs(shadow_price_raw) < 1e-6:
                    shadow_price = 0.0
                else:
                    shadow_price = shadow_price_raw
                
                analysis_results[name] = {
                    "constraint_name": name,
                    "original_rhs": original_rhs,
                    "shadow_price": shadow_price
                }
            
            return analysis_results
        except Exception as e:
            print(f"Erro na análise de preços-sombra: {e}")
            return {}

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
        
        # Get original objective value BEFORE making any changes
        original_objective = plp.value(self._model.objective)
        
        try:
            # Update constraint values
            for i, name in enumerate(constraint_names):
                if i < len(new_constraint_values):
                    # Update the constraint's RHS value
                    constraint = self._model.constraints[name]
                    # For PuLP, we need to modify the constraint expression
                    constraint.constant = -new_constraint_values[i]
            
            # Solve with new values
            solve_status = self._model.solve()
            
            # Check if the problem has a feasible solution
            has_feasible_solution = solve_status == plp.LpStatusOptimal
            
            if has_feasible_solution:
                new_objective = plp.value(self._model.objective)
                
                # NOVA LÓGICA DE VIABILIDADE:
                # Viável = Novo Lucro > Lucro Original
                is_viable = new_objective > original_objective
                
                profit_difference = new_objective - original_objective
                
                result = {
                    "is_viable": is_viable,
                    "new_optimal_value": new_objective,
                    "original_optimal_value": original_objective,
                    "profit_difference": profit_difference,
                    "has_feasible_solution": True,
                    "status": f"Feasible - {'Viável' if is_viable else 'Inviável'} "
                            f"(Δ = {profit_difference:+.2f})",
                    "viability_reason": (
                        f"Novo lucro ({new_objective:.2f}) > "
                        f"Lucro original ({original_objective:.2f})"
                        if is_viable else
                        f"Novo lucro ({new_objective:.2f}) ≤ "
                        f"Lucro original ({original_objective:.2f})"
                    )
                }
            else:
                # Problem became infeasible or unbounded
                result = {
                    "is_viable": False,
                    "new_optimal_value": None,
                    "original_optimal_value": original_objective,
                    "profit_difference": None,
                    "has_feasible_solution": False,
                    "status": f"Infeasible - {plp.LpStatus[self._model.status]}",
                    "viability_reason": (
                        "Problema se tornou inviável com os novos valores de recursos"
                    )
                }
            
            return result
            
        except Exception as e:
            return {
                "is_viable": False,
                "new_optimal_value": None,
                "original_optimal_value": original_objective,
                "profit_difference": None,
                "has_feasible_solution": False,
                "status": f"Error: {str(e)}",
                "viability_reason": f"Erro durante análise: {str(e)}"
            }
            
        finally:
            # SEMPRE restaurar valores originais
            try:
                for i, name in enumerate(constraint_names):
                    self._model.constraints[name].constant = original_constraints[i]
                # Re-solve to restore original state
                self._model.solve()
            except Exception as restore_error:
                print(f"Erro ao restaurar valores originais: {restore_error}")
