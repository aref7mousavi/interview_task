import operator
from abc import abstractmethod
import copy

from django.core.exceptions import ValidationError
from django.db.models import Q


class ABCCalStr:
    def __init__(self, string, objs, kpi_list):
        self.string = string
        self.objs = objs
        self.kpi_list = kpi_list

    @abstractmethod
    def start_calc(self, kpi_excluded=None):
        pass

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
                return self.evaluate_expression(operand)(float(first), float(second))
        return easy

    def full_string(self, x):
        start = None
        for index in range(len(self.string)):
            if self.string[index] == "(":
                start = index
            elif self.string[index] == ")":
                stop = index
                if start is None:
                    raise ValidationError("Invalid kpi key")
                inner_result = self.calc(self.string[start:(stop + 1)], x)
                self.string = self.string[:start] + str(inner_result) + self.string[(stop + 1):]
                return self.full_string(x)
        else:
            return self.calc(self.string, x)

    @staticmethod
    def evaluate_expression(expression):
        operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        return operators[expression]


class CalCity(ABCCalStr):

    def start_calc(self, kpi_excluded=None):
        if kpi_excluded is None:
            kpi_excluded = {}
        response = {}
        for kpi in set(self.kpi_list):
            if kpi not in kpi_excluded.keys():
                for sub_obj in self.objs.filter(kpi=kpi):
                    kpi_excluded[kpi] = sub_obj
                    x = self.objs.filter(kpi=kpi)
                    x = x.exclude(id=sub_obj.id)
                    x = self.objs.exclude(id__in=x.values_list("id", flat=True))
                    if x.count() == len(set(self.kpi_list)):
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.city.name} - {sub_obj.city.province.name}"
                        ] = self.full_string(x)
                    else:
                        sub_response = CalCity(self.string, copy.deepcopy(x), self.kpi_list).start_calc(
                            copy.deepcopy(kpi_excluded))
                        if not sub_response:
                            continue
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.city.name} - {sub_obj.city.province.name}"
                        ] = [sub_response]
        return response


class CalStr(ABCCalStr):

    def start_calc(self, kpi_excluded=None):
        if kpi_excluded is None:
            kpi_excluded = {}
        response = {}
        for kpi in set(self.kpi_list):
            if kpi not in kpi_excluded.keys():
                for sub_obj in self.objs.filter(kpi=kpi):
                    kpi_excluded[kpi] = sub_obj
                    x = self.objs.filter(kpi=kpi)
                    x = x.exclude(id=sub_obj.id)
                    x = self.objs.exclude(id__in=x.values_list("id", flat=True))
                    if x.count() == len(set(self.kpi_list)):
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} -{sub_obj.site.name} - {sub_obj.site.city.name} - {sub_obj.site.city.province.name}"
                        ] = self.full_string(x)
                    else:
                        sub_response = CalStr(self.string, copy.deepcopy(x), self.kpi_list).start_calc(
                            copy.deepcopy(kpi_excluded))
                        if not sub_response:
                            continue
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} -{sub_obj.site.name} - {sub_obj.site.city.name} - {sub_obj.site.city.province.name}"
                        ] = [sub_response]
        return response


class CalProvince(ABCCalStr):

    def start_calc(self, kpi_excluded=None):
        if kpi_excluded is None:
            kpi_excluded = {}
        response = {}
        for kpi in set(self.kpi_list):
            if kpi not in kpi_excluded.keys():
                for sub_obj in self.objs.filter(kpi=kpi):
                    kpi_excluded[kpi] = sub_obj
                    x = self.objs.filter(kpi=kpi)
                    x = x.exclude(id=sub_obj.id)
                    x = self.objs.exclude(id__in=x.values_list("id", flat=True))
                    if x.count() == len(set(self.kpi_list)):
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.province.name}"
                        ] = self.full_string(x)
                    else:
                        sub_response = CalProvince(self.string, copy.deepcopy(x), self.kpi_list).start_calc(
                            copy.deepcopy(kpi_excluded))
                        if not sub_response:
                            continue
                        response[
                            f"{sub_obj.id} - {kpi}: {sub_obj.value} - {sub_obj.province.name}"
                        ] = [sub_response]
        return response
