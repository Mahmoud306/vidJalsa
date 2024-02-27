from abc import ABC, abstractmethod

class ICRUD(ABC):
    @abstractmethod
    def add(self, *args, **kwargs):
        """
        Add a new item to the database.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        """
        Retrieve an item from the database.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The retrieved item.
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Update an item in the database.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            None
        """
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """
        Delete an item from the database.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            None
        """
        pass
