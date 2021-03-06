"""
Copyright 2014 Quentin Kaiser

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from nessusobject import NessusObject
from user import User


class Group(NessusObject):
    """
    A Nessus group.

    Attributes:
        id(int): identification
        name(str): group's name
    _Google Python Style Guide:
    http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
    """

    def __init__(self, server):
        """Constructor"""
        super(Group, self).__init__(server)
        self._name = None
        self._users = []

    def create(self):
        """
        Create a group.
        Params:
        Returns:
        """
        response = self._server._api_request(
            "POST",
            "/groups",
            {"name": self.name}
        )
        if response is not None:
            self.id = response["id"]
            self._name = response["name"]
            self._permissions = response["permissions"]
            return True
        else:
            return False

    def edit(self):
        """
        Edit a group
        Params:
        Returns:
        """
        response = self._server._api_request(
            "POST",
            "/groups/%d" % self.id,
            {"name": self.name}
        )
        if response is not None:
            self.id = response["id"]
            self._name = response["name"]
            self._permissions = response["permissions"]
            return True
        else:
            return False

    def delete(self):
        """
        Delete a group.
        Params:
        Returns:
        """
        response = self._server._api_request(
            "DELETE",
            "/groups/%d" % self.id,
            ""
        )
        if response is None:
            return True
        else:
            return False

    def list_users(self):

        response = self._server._api_request(
            "GET",
            "/groups/%d/users" % (self.id),
            ""
        )
        if response is not None:
            self._users = []
            if "users" in response and response["users"] is not None:
                for u in response["users"]:
                    user = User(self._server)
                    user.id = u["id"]
                    user.username = u["username"]
                    user.name = u["name"]
                    user.email = u["email"]
                    user.permissions = u["permissions"]
                    user.lastlogin = u["lastlogin"]
                    user.type = u["type"]
                    self._users.append(user)
            return True
        else:
            return False

    def add_user(self, user):
        if type(user) is User:
            response = self._server._api_request(
                "POST",
                "/groups/%d/users/%d" % (self.id, user.id),
                ""
            )
            if response is None:
                return True
            else:
                return False
        else:
            raise Exception("Invalid user format.")

    def delete_user(self, user):
        if type(user) is User:
            response = self._server._api_request(
                "DELETE",
                "/groups/%d/users/%d" % (self.id, user.id),
                ""
            )
            if response is None:
                return True
            else:
                return False
        else:
            raise Exception("Invalid user format.")

    @property
    def users(self):
        """
        Return the group user list.
        Params:
        Returns:
        """
        return self._users

    @users.setter
    def users(self, value):
        if type(value) == list:
            self._users = value
        else:
            raise Exception("Invalid format.")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = int(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, value):
        self._permissions = int(value)

    @property
    def user_count(self):
        return self._user_count

    @user_count.setter
    def user_count(self, value):
        self._user_count = int(value)

