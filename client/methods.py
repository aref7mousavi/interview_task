import operator
from abc import abstractmethod, ABC
import copy

from django.core.exceptions import ValidationError


class ABCCalStr(ABC):
    def __init__(self, string, objs, kpi_list, kpi_excluded=None):
        self.string = string
        self.objs = objs
        self.kpi_list = kpi_list
        self.kpi_excluded = kpi_excluded
        if kpi_excluded is None:
            self.kpi_excluded = {}

    @abstractmethod
    def start_calc(self):
        pass

    def full_string(self, x, string):
        start = None
        for index in range(len(string)):
            if string[index] == "(":
                start = index
            elif string[index] == ")":
                stop = index
                if start is None:
                    raise ValidationError("Invalid kpi key")
                inner_result = calc(string[start:(stop + 1)], x)
                string = string[:start] + str(inner_result) + string[(stop + 1):]
                return full_string(x, string)
        else:
            return calc(string, x)

    def calc(self, easy, x):
        easy = easy.replace("(", "").replace(")", "").strip()
        for operand in ("+", "-", "*", "/"):
            if operand in easy:
                nums = easy.split(operand)
                first = nums[0].strip()
                second = nums[1].strip()
                if not first.replace('.', '').isnumeric():
                    first = x.get(kpi=first).value
                if not second.replace('.', '').isnumeric():
                    second = x.get(kpi=second).value
                return evaluate_expression(operand)(float(first), float(second))
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


class CalStr(ABCCalStr):

    def start_calc(self, kpi_excluded=None):
        response = {}
        for kpi in set(self.kpi_list):
            if kpi not in self.kpi_excluded.keys():
                for sub_obj in self.objs.filter(kpi=kpi):
                    self.kpi_excluded[kpi] = sub_obj
                    new_kpi_excluded = copy.deepcopy(self.kpi_excluded)
                    x = self.objs.filter(kpi=kpi)
                    x = x.exclude(id=sub_obj.id)
                    x = self.objs.exclude(id__in=x.values_list("id", flat=True))
                    if x.count() == len(set(self.kpi_list)):
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.site.name} - {sub_obj.site.city.name} - {sub_obj.site.city.province.name}"
                        ] = self.full_string(copy.deepcopy(x), copy.copy(self.string))
                    else:
                        sub_response = CalStr(
                            copy.copy(self.string),
                            copy.deepcopy(x),
                            self.kpi_list,
                            new_kpi_excluded
                        ).start_calc()
                        if not sub_response:
                            continue
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.site.name} - {sub_obj.site.city.name} - {sub_obj.site.city.province.name}"
                        ] = [sub_response]
        return response


class CalCity(ABCCalStr):

    def start_calc(self, kpi_excluded=None):
        response = {}
        for kpi in set(self.kpi_list):
            if kpi not in self.kpi_excluded.keys():
                for sub_obj in self.objs.filter(kpi=kpi):
                    self.kpi_excluded[kpi] = sub_obj
                    new_kpi_excluded = copy.deepcopy(self.kpi_excluded)
                    x = self.objs.filter(kpi=kpi)
                    x = x.exclude(id=sub_obj.id)
                    x = self.objs.exclude(id__in=x.values_list("id", flat=True))
                    if x.count() == len(set(self.kpi_list)):
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.city.name} - {sub_obj.city.province.name}"
                        ] = self.full_string(copy.deepcopy(x), copy.copy(self.string))
                    else:
                        sub_response = CalCity(
                            copy.copy(self.string),
                            copy.deepcopy(x),
                            self.kpi_list,
                            new_kpi_excluded
                        ).start_calc()
                        if not sub_response:
                            continue
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.city.name} - {sub_obj.city.province.name}"
                        ] = [sub_response]
        return response


class CalProvince(ABCCalStr):

    def start_calc(self, kpi_excluded=None):
        response = {}
        for kpi in set(self.kpi_list):
            if kpi not in self.kpi_excluded.keys():
                for sub_obj in self.objs.filter(kpi=kpi):
                    self.kpi_excluded[kpi] = sub_obj
                    new_kpi_excluded = copy.deepcopy(self.kpi_excluded)
                    x = self.objs.filter(kpi=kpi)
                    x = x.exclude(id=sub_obj.id)
                    x = self.objs.exclude(id__in=x.values_list("id", flat=True))
                    if x.count() == len(set(self.kpi_list)):
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.province.name}"
                        ] = self.full_string(copy.deepcopy(x), copy.copy(self.string))
                    else:
                        sub_response = CalProvince(
                            copy.copy(self.string),
                            copy.deepcopy(x),
                            self.kpi_list,
                            new_kpi_excluded
                        ).start_calc()
                        if not sub_response:
                            continue
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.province.name}"
                        ] = [sub_response]
        return response


# functional mode for test


def city_start_calc(string, objs, kpi_list, kpi_excluded=None):
    if kpi_excluded is None:
        kpi_excluded = {}
    response = {}
    for kpi in set(kpi_list):
        if kpi not in kpi_excluded.keys():
            for sub_obj in objs.filter(kpi=kpi):
                kpi_excluded[kpi] = sub_obj
                new_kpi_excluded = copy.deepcopy(kpi_excluded)
                new_kpi_excluded[kpi] = sub_obj
                x = objs.filter(kpi=kpi)
                x = x.exclude(id=sub_obj.id)
                x = objs.exclude(id__in=x.values_list("id", flat=True))
                if x.count() == len(set(kpi_list)):
                    response[
                        f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.city.name} - {sub_obj.city.province.name}"
                    ] = full_string(copy.deepcopy(x), string)
                else:
                    sub_response = city_start_calc(string, copy.deepcopy(x), kpi_list, new_kpi_excluded)
                    if not sub_response:
                        continue
                    response[
                        f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.city.name} - {sub_obj.city.province.name}"
                    ] = [sub_response]
    return response


def province_start_calc(string, objs, kpi_list, kpi_excluded=None):
    if kpi_excluded is None:
        kpi_excluded = {}
    response = {}
    for kpi in set(kpi_list):
        if kpi not in kpi_excluded.keys():
            for sub_obj in objs.filter(kpi=kpi):
                kpi_excluded[kpi] = sub_obj
                new_kpi_excluded = copy.deepcopy(kpi_excluded)
                new_kpi_excluded[kpi] = sub_obj
                x = objs.filter(kpi=kpi)
                x = x.exclude(id=sub_obj.id)
                x = objs.exclude(id__in=x.values_list("id", flat=True))
                if x.count() == len(set(kpi_list)):
                    response[
                        f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.province.name}"
                    ] = full_string(copy.deepcopy(x), string)
                else:
                    sub_response = province_start_calc(string, copy.deepcopy(x), kpi_list, new_kpi_excluded)
                    if not sub_response:
                        continue
                    response[
                        f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.province.name}"
                    ] = [sub_response]
    return response


def start_calc(string, objs, kpi_list, kpi_excluded=None):
    if kpi_excluded is None:
        kpi_excluded = {}
    response = {}
    for kpi in set(kpi_list):
        if kpi not in kpi_excluded.keys():
            for sub_obj in objs.filter(kpi=kpi):
                kpi_excluded[kpi] = sub_obj
                new_kpi_excluded = copy.deepcopy(kpi_excluded)
                new_kpi_excluded[kpi] = sub_obj
                x = objs.filter(kpi=kpi)
                x = x.exclude(id=sub_obj.id)
                x = objs.exclude(id__in=x.values_list("id", flat=True))
                if x.count() == len(set(kpi_list)):
                    response[
                        f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.site.name} - {sub_obj.site.city.name} - {sub_obj.site.city.province.name}"
                    ] = full_string(copy.deepcopy(x), string)
                else:
                    sub_response = start_calc(string, copy.deepcopy(x), kpi_list, new_kpi_excluded)
                    if not sub_response:
                        continue
                    response[
                        f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.site.name} - {sub_obj.site.city.name} - {sub_obj.site.city.province.name}"
                    ] = [sub_response]
    return response


def full_string(x, string):
    start = None
    for index in range(len(string)):
        if string[index] == "(":
            start = index
        elif string[index] == ")":
            stop = index
            if start is None:
                raise ValidationError("Invalid kpi key")
            inner_result = calc(string[start:(stop + 1)], x)
            string = string[:start] + str(inner_result) + string[(stop + 1):]
            return full_string(x, string)
    else:
        return calc(string, x)


def calc(easy, x):
    easy = easy.replace("(", "").replace(")", "").strip()
    for operand in ("+", "-", "*", "/"):
        if operand in easy:
            nums = easy.split(operand)
            first = nums[0].strip()
            second = nums[1].strip()
            if not first.replace('.', '').isnumeric():
                first = x.get(kpi=first).value
            if not second.replace('.', '').isnumeric():
                second = x.get(kpi=second).value
            return evaluate_expression(operand)(float(first), float(second))
    return easy


def evaluate_expression(expression):
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    return operators[expression]