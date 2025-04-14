from abc import ABC, abstractmethod
from typing import Any


class BaseView(ABC):
    @abstractmethod
    def render(self, *args: Any) -> Any:
        """Renders the view and returns the data to be displayed.

        Returns:
            Dict[str, Any]: A dictionary containing the data
                that will be rendered in the view.
        """
        ...
