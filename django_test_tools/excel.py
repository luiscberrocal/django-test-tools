from openpyxl import load_workbook


class ExcelAdapter(object):
    @classmethod
    def convert_to_list(cls, filename, sheet_name=None, has_header=True):
        """
        Reads an Excel file and convertes every row into a list of values.
        :param filename: <str> Excel filename
        :param sheet_name: <str> Name of the sheet
        :param has_header: <bool> If true the first row is not included in the list.
        :return: <list> A list of lists.
        """
        data = list()
        wb = load_workbook(filename=filename, data_only=True)
        if sheet_name is None:
            sheet = wb.active
        else:
            sheet = wb[sheet_name]
        row_num = 1
        for row in sheet.rows:
            row_data = list()
            if row_num == 1 and has_header:
                row_num += 1
                continue
            for column in range(0, len(row)):
                row_data.append(row[column].value)
            data.append(row_data)
            row_num += 1
        return data
