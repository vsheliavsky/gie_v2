from typing import TypeAlias

FlexibleValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | list["FlexibleValue"]
    | dict[str, "FlexibleValue"]
)  # Basicaly used as a replacement for Any to avoid mypy complaining

ParamDict: TypeAlias = dict[str, FlexibleValue]

Json: TypeAlias = dict[str, FlexibleValue] | list[FlexibleValue]
