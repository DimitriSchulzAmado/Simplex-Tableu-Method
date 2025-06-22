from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Literal

from utilities.array import find_index


class ObjectiveFunctionType(Enum):
    """Tipos de função objetivo."""
    MAXIMIZE = "MAXIMIZE"
    MINIMIZE = "MINIMIZE"


class ConstraintSymbol(Enum):
    """Símbolos de restrição."""
    EQUAL = "="
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN_OR_EQUAL = ">="


@dataclass(frozen=True)
class Variable:
    """Representa uma variável na função objetivo."""
    name: str
    value: float = 0.0

    def __post_init__(self):
        if not self.name:
            raise ValueError("Variable name cannot be empty.")
        if not isinstance(self.value, (int, float)):
            raise TypeError("Variable value must be a number.")
        

@dataclass(frozen=True)
class Constraint:
    """Representa uma restrição na função objetivo."""
    name: str
    symbol: ConstraintSymbol = field(default=ConstraintSymbol.LESS_THAN_OR_EQUAL)
    variables: list[Variable] = field(default_factory=list)
    value: float = 0.0
        
    def add_variable(self, variable: Variable):
        """Adiciona uma variável à restrição."""
        if not isinstance(variable, Variable):
            raise TypeError("Expected a Variable instance.")
        self.variables.append(variable)

    def remove_variable(self, variable_name: str):
        """Remove uma variável da restrição pelo nome."""
        index = find_index(lambda v: v.name == variable_name, self.variables)
        if index == -1:
            raise ValueError(f"Variable with name '{variable_name}' not found in constraint '{self.name}'.")
        del self.variables[index]

    def update_variable(self, variable: Variable):
        """Atualiza uma variável existente na restrição."""
        index = find_index(lambda v: v.name == variable.name, self.variables)
        if index == -1:
            raise ValueError(f"Variable with name '{variable.name}' not found in constraint '{self.name}'.")
        self.variables[index] = variable


@dataclass
class ObjectiveFunctionState:
    """Estado da função objetivo."""
    quantity_of_variables: int = 2
    quantity_of_constraints: int = 2
    objective_function: ObjectiveFunctionType = field(default=ObjectiveFunctionType.MAXIMIZE)

    variables: list[Variable] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)

    def __post_init__(self):
        if self.quantity_of_variables < 2:
            raise ValueError("The number of variables must be at least 2.")
        if self.quantity_of_constraints < 2:
            raise ValueError("The number of constraints must be at least 2.")
        if not isinstance(self.objective_function, ObjectiveFunctionType):
            raise ValueError("Invalid objective function type.")
        
        # Initialize variables with default values
        self.variables = [Variable(name=f"x{i+1}") for i in range(self.quantity_of_variables)]

        # Initialize constraints with default values
        self.constraints = [
            Constraint(
                name=f"Constraint {i+1}", 
                symbol=ConstraintSymbol.LESS_THAN_OR_EQUAL, 
                variables=[Variable(name=f"x{i+1}") for i in range(self.quantity_of_variables)]
            )
            for i in range(self.quantity_of_constraints)
        ]

    def reset(self):
        """Reseta para os valores padrão."""
        self.quantity_of_variables = 2
        self.quantity_of_constraints = 2
        self.objective_function = ObjectiveFunctionType.MAXIMIZE

    def set_quantity_of_variables(self, quantity: int):
        """Define o número de variáveis."""
        if quantity < 2:
            raise ValueError("The number of variables must be at least 2.")
        self.quantity_of_variables = quantity

        has_decreased = len(self.variables) > quantity
        if len(self.variables) > quantity:
            self.variables = self.variables[:quantity]
        elif len(self.variables) < quantity:
            self.variables.append(Variable(name=f"x{len(self.variables) + 1}"))  # Add a new variable

        _constraints: list[Constraint] = []
        for constraint in self.constraints:
            new_variables = [
                Variable(name=v.name, value=v.value)
                for v in constraint.variables
            ]

            if has_decreased:
                # Remove variables that are no longer in the new quantity
                new_variables = new_variables[:self.quantity_of_variables]
            else:
                new_variables.append(
                    Variable(name=f"x{len(new_variables) + 1}", value=0.0)
                )

            _constraints.append(
                Constraint(
                    name=constraint.name,
                    symbol=constraint.symbol,
                    variables=new_variables,
                    value=constraint.value,
                )
            )

        self.constraints = _constraints

    def set_quantity_of_constraints(self, quantity: int):
        """Define o número de restrições."""
        if quantity < 2:
            raise ValueError("The number of constraints must be at least 2.")
        self.quantity_of_constraints = quantity

        if len(self.constraints) > quantity:
            self.constraints = self.constraints[:quantity]
        elif len(self.constraints) < quantity:
            self.constraints.append(
                Constraint(
                    name=f"Constraint {len(self.constraints) + 1}",
                    symbol=ConstraintSymbol.LESS_THAN_OR_EQUAL,
                    variables=[Variable(name=f"x{i+1}") for i in range(self.quantity_of_variables)],
                    value=0.0,
                )
            )

    def set_objective_function(self, objective_function: ObjectiveFunctionType):
        """Define a função objetivo."""
        if not isinstance(objective_function, ObjectiveFunctionType):
            raise ValueError("Invalid objective function type.")
        self.objective_function = objective_function

    def update_variable(self, name: str, value: float):
        """Atualiza uma variável específica."""
        index_of_variable = find_index(lambda v: v.name == name, self.variables)
        if index_of_variable == -1:
            raise ValueError(f"Variable with name '{name}' not found.")

        self.variables[index_of_variable] = Variable(name=name, value=value)

    def update_constraint_variable(self, constraint_name: str, variable: Variable):
        """Atualiza uma variável em uma restrição específica."""
        index_of_constraint = find_index(lambda c: c.name == constraint_name, self.constraints)
        if index_of_constraint == -1:
            raise ValueError(f"Constraint with name '{constraint_name}' not found.")

        variable_index = find_index(lambda v: v.name == variable.name, self.constraints[index_of_constraint].variables)
        if variable_index == -1:
            raise ValueError(f"Variable with name '{variable.name}' not found in constraint '{constraint_name}'.")
        
        variables = self.constraints[index_of_constraint].variables.copy()
        variables[variable_index] = variable

        constraint = Constraint(
            name=constraint_name,
            symbol=self.constraints[index_of_constraint].symbol,
            variables=variables,
            value=self.constraints[index_of_constraint].value,
        )

        self.constraints[index_of_constraint] = constraint

    def update_contraint_symbol(self, constraint_name: str, symbol: ConstraintSymbol):
        """Atualiza o símbolo de uma restrição específica."""
        index_of_constraint = find_index(lambda c: c.name == constraint_name, self.constraints)
        if index_of_constraint == -1:
            raise ValueError(f"Constraint with name '{constraint_name}' not found.")

        constraint = Constraint(
            name=constraint_name, 
            symbol=symbol, 
            variables=self.constraints[index_of_constraint].variables,
            value=self.constraints[index_of_constraint].value,
        )
        self.constraints[index_of_constraint] = constraint

    def update_constraint_value(self, constraint_name: str, value: float):
        """Atualiza o valor de uma restrição específica."""
        index_of_constraint = find_index(lambda c: c.name == constraint_name, self.constraints)
        if index_of_constraint == -1:
            raise ValueError(f"Constraint with name '{constraint_name}' not found.")

        constraint = Constraint(
            name=constraint_name,
            symbol=self.constraints[index_of_constraint].symbol,
            variables=self.constraints[index_of_constraint].variables,
            value=value,
        )

        self.constraints[index_of_constraint] = constraint

@dataclass
class AppState:
    """Estado global da aplicação."""
    objective_function: ObjectiveFunctionState = field(default_factory=ObjectiveFunctionState)
    is_solving: bool = False

    _listeners: dict[Literal["objective_function", "constraint"], list[Callable]] = field(default_factory=dict)

    def reset(self):
        """Reseta todo o estado da aplicação."""
        self.objective_function.reset()
        self.is_solving = False

    def set_is_solving(self, is_solving: bool):
        self.is_solving = is_solving

    def set_quantity_of_variables(self, quantity: int):
        self.objective_function.set_quantity_of_variables(quantity)
        self._notify_listeners("objective_function")
        self._notify_listeners("constraint")

    def set_quantity_of_constraints(self, quantity: int):
        self.objective_function.set_quantity_of_constraints(quantity)
        self._notify_listeners("constraint")

    def set_objective_function(self, objective_function: ObjectiveFunctionType):
        self.objective_function.set_objective_function(objective_function)

    def subscribe(self, listener: Callable, type: Literal["objective_function", "constraint"] = "objective_function"):
        """Adiciona um ouvinte para mudanças no estado."""
        if type not in self._listeners:
            self._listeners[type] = []

        self._listeners[type].append(listener)

    def _notify_listeners(self, _type: Literal["objective_function", "constraint"] = "objective_function"):
        """Notifica todos os ouvintes sobre mudanças no estado."""
        for listener in self._listeners.get(_type, []):
            listener()

    def notify_all(self):
        """Notifica todos os ouvintes sobre mudanças no estado."""
        pass

# Instância global
app_state = AppState()
