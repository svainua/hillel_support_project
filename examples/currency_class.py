# from dataclasses import dataclass
# from enum import StrEnum, auto


# class Currency(StrEnum):
#     USD = auto()
#     UAH = auto()
#     EUR = auto()


# @dataclass
# class Price:
#     amount: int
#     currency: Currency

#     def __eq__(self, value: object) -> bool:
#         if not isinstance(right, "Price"):
#             raise ValueError("Only Orice instances support this operation")

#         if (self.amount, self.currency) == (right.amount, right.currency):
#             return True
#         else:
#             return False
