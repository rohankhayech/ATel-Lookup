"""
Contains the AliasResult data structure, representing an alias and the object it is associated with.

Author:
    Rohan Khayech

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

class AliasResult:
    """
    An object representing an alias and the object it is associated with.
    """

    def __init__(self, alias:str, object_ID:str):
        """
        Creates an object alias.

        Args:
            alias (str): String representing an alternative name of the object.
            object_ID (str): String representing the main object ID associated with the alias.
        """
        self._alias = str(alias)
        self._object_ID = str(object_ID)

    def __str__(self) -> str:
        return f"{self.alias} refers to object: {self.object_ID}"

    @property
    def alias(self)->str:
        """
        String representing an alternative name of the object.
        """
        return self._alias

    @alias.setter
    def alias(self, x):
        """
        Modifying alias is unsupported.
        """
        raise TypeError("Cannot modify alias (AliasResult is an immutable object.)")

    @property
    def object_ID(self)->str:
        """
        String representing an alternative name of the object.
        """
        return self._object_ID

    @object_ID.setter
    def object_ID(self, x):
        """
        Modifying object ID is unsupported.
        """
        raise TypeError("Cannot modify object_ID(AliasResult is an immutable object.)")
