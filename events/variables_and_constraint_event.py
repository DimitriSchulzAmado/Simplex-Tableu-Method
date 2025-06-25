import enum

import flet as ft

from data.app_state import app_state


class TextEnum(enum.Enum):
    """
    This class is used to define text constants for the application.
    It inherits from enum.Enum to provide a structured way to manage text values.
    """
    
    VARIABLE_LABEL = "VARIABLE_LABEL"
    CONSTRAINT_LABEL = "CONSTRAINT_LABEL"


class VariablesAndConstraintEvent:
    """
    This class represents an event that contains variables and constraints.
    It is used to manage the state of variables and constraints in a system.
    """

    def __init__(self, page: ft.Page, texts: dict[TextEnum, ft.Text]) -> None:
        self._page = page
        self._texts = texts

    def add_variable(self, _event: ft.ControlEvent):
        """Adds a variable to the event."""
        new_quantity = app_state.objective_function.quantity_of_variables + 1

        app_state.objective_function.set_quantity_of_variables(
            new_quantity
        )

        self._texts[TextEnum.VARIABLE_LABEL].value = f"{new_quantity} Variaveis"
        self._page.update()

    def remove_variable(self, _event: ft.ControlEvent):
        """Removes a variable from the event."""
        if app_state.objective_function.quantity_of_variables > 2:
            new_quantity = app_state.objective_function.quantity_of_variables - 1
            app_state.objective_function.set_quantity_of_variables(
                new_quantity
            )

            self._texts[TextEnum.VARIABLE_LABEL].value = f"{new_quantity} Variaveis"
            self._page.update()
        else:
            self._page.update()

    def add_constraint(self, _event: ft.ControlEvent):
        """Adds a constraint to the event."""
        new_quantity = app_state.objective_function.quantity_of_constraints + 1
        app_state.objective_function.set_quantity_of_constraints(
            new_quantity
        )

        self._texts[TextEnum.CONSTRAINT_LABEL].value = f"{new_quantity} Restrições"
        self._page.update()

    def remove_constraint(self, _event: ft.ControlEvent):
        """Removes a constraint from the event."""
        if app_state.objective_function.quantity_of_constraints > 2:
            new_quantity = app_state.objective_function.quantity_of_constraints - 1
            app_state.objective_function.set_quantity_of_constraints(
                new_quantity
            )

            self._texts[TextEnum.CONSTRAINT_LABEL].value = f"{new_quantity} Restrições"
            self._page.update()
        else:
            self._page.update()