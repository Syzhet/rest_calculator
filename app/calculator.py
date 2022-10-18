import operator
from typing import Callable, List, Dict, Any, Union, Generator


MATH_CALC_DICT: Dict[str, Callable[[int, int], int]] = {
    '+': (1, operator.add),
    '-': (1, operator.sub),
    '*': (2, operator.mul),
    '/': (2, operator.truediv)
}


class Stack:
    """Class for creating an instance of a Stack-type data structure."""

    def __init__(self) -> None:
        """Constructor of the Stack class."""

        self.__seq: List[Any] = []

    def is_empty(self) -> bool:
        """Checks if there are elements in the stack."""

        return self.size() == 0

    def push(self, x: Any) -> None:
        """Adds an element to the top of the stack."""

        self.__seq.append(x)

    def pop(self) -> Any:
        """Removes and returns an element from the top of the stack."""

        if self.is_empty():
            return IndexError('Стэк пуст')
        x: Any = self.__seq.pop()
        return x

    def size(self) -> int:
        """Returns the number of elements in the stack."""

        return len(self.__seq)

    @property
    def get_result(self) -> Any:
        """Returns the last element in the stack as a result."""

        try:
            return self.__seq[-1]
        except IndexError:
            return 'Необходимо ввести операнды для расчета значения'


def parse(formula_string: str) -> Generator[float, None, None]:
    """String parsing function."""

    number: str = ''
    for symbol in formula_string:
        if symbol not in '1234567890.()/*+-':
            raise ValueError('Bad operands or operators')
        if symbol in '1234567890.':
            number += symbol
        elif number:
            yield float(number)
            number = ''
        if symbol in MATH_CALC_DICT or symbol in "()":
            yield symbol
    if number:
        yield float(number)


def from_infix_to_postfix(
    parsed_formula: Callable[[str], Generator[Union[float, str], None, None]]
) -> Generator[Union[float, str], None, None]:
    """Converts a sequence from infix to postfix form."""

    help_l: List[Union[float, str]] = []
    for token in parsed_formula:
        if token in MATH_CALC_DICT:
            while (
                help_l and help_l[-1] != "("
                and MATH_CALC_DICT[token][0] <= MATH_CALC_DICT[help_l[-1]][0]
            ):
                yield help_l.pop()
            help_l.append(token)
        elif token == ")":
            while help_l:
                x = help_l.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            help_l.append(token)
        else:
            yield token
    while help_l:
        yield help_l.pop()


def calculator(
    postfix_notation: Generator[Union[float, str], None, None]
) -> float:
    """Postfix notation processing function."""

    stack: Stack = Stack()
    for symbol in postfix_notation:
        try:
            stack.push(float(symbol))
        except ValueError:
            b: int = stack.pop()
            a: int = stack.pop()
            stack.push(MATH_CALC_DICT[symbol][1](a, b))
    return stack.get_result


def start_calculation(input_str: str) -> float:
    """The function starts the calculation."""

    return calculator(from_infix_to_postfix(parse(input_str)))


if __name__ == '__main__':
    test_str = '(2+2*(2*2))/2'
    assert start_calculation(test_str) == 5.0, 'Неверное знаечние'
