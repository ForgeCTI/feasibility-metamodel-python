from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_bool, require_optional_email, require_optional_str


class User(BaseEntity):
    """Represents the User entity from the metamodel."""

    _domain_attributes = ('username', 'email', 'role', 'privilege_level', 'mfa_enabled')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        username: str | None = None,
        email: str | None = None,
        role: str | None = None,
        privilege_level: str | None = None,
        mfa_enabled: bool | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._username: str | None
        self._email: str | None
        self._role: str | None
        self._privilege_level: str | None
        self._mfa_enabled: bool | None
        self.username = username
        self.email = email
        self.role = role
        self.privilege_level = privilege_level
        self.mfa_enabled = mfa_enabled

    @property
    def username(self) -> str | None:
        return self._username

    @username.setter
    def username(self, value: str | None) -> None:
        self._username = require_optional_str(value, "username")

    @property
    def email(self) -> str | None:
        return self._email

    @email.setter
    def email(self, value: str | None) -> None:
        self._email = require_optional_email(value, "email")

    @property
    def role(self) -> str | None:
        return self._role

    @role.setter
    def role(self, value: str | None) -> None:
        self._role = require_optional_str(value, "role")

    @property
    def privilege_level(self) -> str | None:
        return self._privilege_level

    @privilege_level.setter
    def privilege_level(self, value: str | None) -> None:
        self._privilege_level = require_allowed(require_optional_str(value, "privilege_level"), "privilege_level", {None, 'root', 'unknown', 'standard', 'privileged', 'low', 'none', 'admin'})

    @property
    def mfa_enabled(self) -> bool | None:
        return self._mfa_enabled

    @mfa_enabled.setter
    def mfa_enabled(self, value: bool | None) -> None:
        self._mfa_enabled = require_optional_bool(value, "mfa_enabled")

