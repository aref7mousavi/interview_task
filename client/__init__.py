import operator

from django.core.exceptions import ValidationError


class CalStr:
    def __init__(self, string, obj):
        self.string = string
        self.obj = obj

    def __call__(self, *args, **kwargs):
        return self.full_string()

    def full_string(self):
        start = None
        for index in range(len(self.string)):
            if self.string[index] == "(":
                start = index
            elif self.string[index] == ")":
                stop = index
                if start is None:
                    raise ValidationError("Invalid kpi key")
                inner_result = self.calc(self.string[start:(stop + 1)])
                self.string = self.string[:start] + str(inner_result) + self.string[(stop + 1):]
                return self.full_string()
        else:
            return self.calc(self.string)

    def calc(self, easy):
        easy = easy.replace("(", "").replace(")", "").strip()
        for operand in ("+", "-", "*", "/"):
            if operand in easy:
                nums = easy.split(operand)
                first = nums[0].strip()
                second = nums[1].strip()
                if not first.isnumeric():
                    getattr(self.obj, first)
                if not second.isnumeric():
                    getattr(self.obj, second)
                return self.evaluate_expression(operand)(float(first), float(second))
        return easy

    @staticmethod
    def evaluate_expression(expression):
        operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        return operators[expression]


# def zxc(st):
#     start = None
#     for index in range(len(st)):
#         if st[index] == "(":
#             start = index
#         elif st[index] == ")":
#             stop = index
#             if start is None:
#                 raise ValidationError("")
#             inner_result = calc(st[start:(stop+1)])
#             st = st[:start] + str(inner_result) + st[(stop+1):]
#             return zxc(st)
#     else:
#         return calc(st)

# print(zxc(s))
# print(zxc("((1 + 2) * (7-5)) + 1"))

