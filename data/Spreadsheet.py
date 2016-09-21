import openpyxl

from data.DataStore import DataStore


class Spreadsheet(DataStore):
    def __init__(self, filename):
        self._filename
        self._workbook = openpyxl.load_workbook(self._filename)
        self._sheet = self._workbook.active


    def set_title(self, title):
        self._sheet.title = title
        self._workbook.save(self._filename)

