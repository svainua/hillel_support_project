from collections.abc import Generator
from pprint import pprint as print
from types import EllipsisType

nested_structure = {
    "teachers": {
        "john": {
            "age": ...,
            "full_name": ...,
        },
        "marry": {
            "age": ...,
            "address": ...,
        },
    },
    "students": {
        "john": {
            "average": {
                "math": ...,
                "music": ...,
            },
            "contacts": ...,
        }
    },
}


def extract_nested(
    data: dict, parents: list[str] | None = None, nested: int = 0
) -> Generator[tuple, None, None]:
    if nested > 100:
        raise NotImplementedError("smth")

    for key, value in data.items():
        if isinstance(value, EllipsisType):
            if parents:
                yield (*parents, key)
            else:
                yield (key,)
        elif isinstance(value, dict):
            if parents:
                parents.append(key)
                yield tuple(parents)
                # for item in extract_nested(data=value, parents=parents):
                #     yield item       #то же самое, что и ниже одной строкой #noqa
                yield from extract_nested(data=value, parents=parents)

            else:
                yield (key,)
                yield from extract_nested(data=value, parents=[key])
        else:
            raise NotImplementedError("smth2")


# results = list(extract_nested(nested_structure))
# print(results)

for item in extract_nested(nested_structure):
    print(item)


# (teachers)
# (teachers, john)
# (teachers, john, age)
# (teachers, john, full_name)
# (teachers, marry)
# (teachers, marry, age)
# (teachers, marry, address)
# (students)
# (students, john)
# (students, john, average)
# (students, john, average, math)
# (students, john, average, music)
# (students, john, contacts)
