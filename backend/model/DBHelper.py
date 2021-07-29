

class AliasResult:
    """
    An object representing an alias and the object it is associated with.
    """

    def __init__(self, alias:str, object_ID:str):
        """
        Creates an object alias

        Args:
            alias (str): String representing an alternative name of the object.
            object_ID (str): String representing the main object ID associated with the alias.
        """

        #TODO: type/value checking in constructor as object is immutable
        self.__alias = alias
        self.__object_ID = object_ID

    @property
    def alias(self)->str:
        """
        String representing an alternative name of the object.
        """
        return self.__alias

    @alias.setter
    def alias(self, x):
        """
        Modifying alias is unsupported.
        """
        raise TypeError("Cannot modify alias (AliasResult is an immutable object.)")

    @property
    def objectID(self)->str:
        """
        String representing an alternative name of the object.
        """
        return self.__alias

    @alias.setter
    def objectID(self, x):
        """
        Modifying object ID is unsupported.
        """
        raise TypeError("Cannot modify object_ID(AliasResult is an immutable object.)")