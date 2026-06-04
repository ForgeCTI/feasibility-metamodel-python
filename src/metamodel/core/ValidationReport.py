from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationMessage:
    validator: str
    message: str
    severity: str = "error"


@dataclass
class ValidationReport:
    messages: list[ValidationMessage] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not any(msg.severity == "error" for msg in self.messages)

    @property
    def errors(self) -> list[ValidationMessage]:
        return [msg for msg in self.messages if msg.severity == "error"]

    @property
    def warnings(self) -> list[ValidationMessage]:
        return [msg for msg in self.messages if msg.severity == "warning"]

    def add_error(self, validator: str, message: str) -> None:
        self.messages.append(ValidationMessage(validator=validator, message=message, severity="error"))

    def add_warning(self, validator: str, message: str) -> None:
        self.messages.append(ValidationMessage(validator=validator, message=message, severity="warning"))

    def extend(self, other: "ValidationReport") -> None:
        self.messages.extend(other.messages)
