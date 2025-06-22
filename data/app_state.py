from dataclasses import dataclass, field

@dataclass
class ObjectiveFunctionState:
    """Estado da função objetivo."""
    quantity_of_variables: int = 2
    quantity_of_constraints: int = 2

    def reset(self):
        """Reseta para os valores padrão."""
        self.quantity_of_variables = 2
        self.quantity_of_constraints = 2

    def set_quantity_of_variables(self, quantity: int):
        """Define o número de variáveis."""
        if quantity < 2:
            raise ValueError("The number of variables must be at least 2.")
        self.quantity_of_variables = quantity

    def set_quantity_of_constraints(self, quantity: int):
        """Define o número de restrições."""
        if quantity < 2:
            raise ValueError("The number of constraints must be at least 2.")
        self.quantity_of_constraints = quantity

@dataclass
class AppState:
    """Estado global da aplicação."""
    objective_function: ObjectiveFunctionState = field(default_factory=ObjectiveFunctionState)
    is_solving: bool = False

    def reset(self):
        """Reseta todo o estado da aplicação."""
        self.objective_function.reset()
        self.is_solving = False

    def set_is_solving(self, is_solving: bool):
        self.is_solving = is_solving

    def set_quantity_of_variables(self, quantity: int):
        self.objective_function.set_quantity_of_variables(quantity)

    def set_quantity_of_constraints(self, quantity: int):
        self.objective_function.set_quantity_of_constraints(quantity)

# Instância global
app_state = AppState()
