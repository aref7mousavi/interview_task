from typing import List, Tuple, Union, Optional


class MyDataFrame:
    def __init__(self, data: List[Tuple[Union[int, None], ...]], columns: List[str]):
        """
        Initialize MyDataFrame object.

        Args:
            data (List[Tuple[Union[int, None], ...]]): The data rows, where each row is represented as a tuple
                                                        containing numbers and/or None.
            columns (List): The column names.
        """
        self.data = data
        self.columns = columns
        self._width = []

    def calculate_width(self) -> List[int]:
        """
        Calculate and cache the maximum width for each column in the data.

        Returns:
            List[int]: A list of integers representing the maximum width of each column.
        """
        if not self._width:
            w = self.data.copy()
            w.append(self.columns)
            self._width = [max(len(str(item[i])) for item in w) for i in range(len(self.columns))]
        return self._width

    def formatter(self) -> str:
        """
        Create a formatter string for aligning columns based on their widths.

        This method generates a formatter string using the calculated column widths
        to ensure that each column is properly aligned when printed.

        Returns:
            str: A formatter string for formatting rows of data.
        """
        return "\t\t".join([f"{{:<{width}}}" for width in self.calculate_width()])

    def __str__(self):
        result = self.formatter().format(*self.columns) + "\n"
        for row in self.data:
            result += self.formatter().format(*[str(item) for item in row]) + "\n"
        return result

    def index(self, row_index: int):
        """
        Return specific row of data with selected row index.

        Args:
            row_index (int): most be an index of data rows
        Raises:
            IndexError: if given index is invalid
        Returns:
            list: The selected row from data.
        """
        if row_index < 0 or row_index >= len(self.data):
            raise IndexError("Row index out of range")
        return list(self.data[row_index])

    def sort(self, column: str, mode: str):
        """
        Return full data filtered by selected column and asc or dsc chosen by mode.

        Args:
            column (str): most be a name of columns

            mode (str): descending to sort dsc and ascending(or anything else) to sort asc

        Returns:
            str: The formatted string of the sorted data.
        """
        col_index = self.columns.index(column)
        sorted_data = sorted(
            self.data,
            key=lambda x: (x[col_index] is None, x[col_index]),
            reverse=(mode == 'descending')
        )
        result = self.formatter().format(*self.columns) + "\n"

        for row in sorted_data:
            result += self.formatter().format(*[str(item) for item in row]) + "\n"
        return result

    def __getitem__(self, cols: List[str]) -> Optional[List[List[Union[int, None]]]]:
        """
        Return full data filtered by selected column and asc or dsc chosen by mode.

        Args:
            cols (str): most be a name of columns

        Returns:
            Optional[List[List[Union[int, None]]]]: The selected columns' data,
                                                    or None if cols is not a list of strings.
        """
        if isinstance(cols, list):
            output = []
            for ind in (self.columns.index(col) for col in cols):
                output.append([row[ind] for row in self.data])
            return output

    def __getattr__(self, col: str) -> Optional[List[Union[int, None]]]:
        """
        Return a list including value of selected column in all data rows.

        Args:
            col (str): most be a name of columns

        Returns:
            Optional[List[Union[int, None]]]: A list, or None if col is not valid string.
        """
        if col in self.columns:
            col_index = self.columns.index(col)
            return [row[col_index] for row in self.data]


df = MyDataFrame([(1, 2, 3), (4, None, 10), (5, 1, 19), (3, 0, 17)], columns=['a', 'b', 'c'])
print(df)
# a		b   		c
# 1		2   		3
# 4		None		10
# 5		1   		19
# 3		0   		17

print(df.a)
# [1, 4, 5, 3]

print(df[["a", 'c']])
# [[1, 4, 5, 3], [3, 10, 19, 17]]

print(df.index(1))
# [4, None, 10]

print(df.sort('b', mode="ascending"))
# a		b   		c
# 3		0   		17
# 5		1   		19
# 1		2   		3
# 4		None		10
