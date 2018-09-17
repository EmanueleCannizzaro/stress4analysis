#from ...f06_table import F06Table

#from __future__ import print_function, absolute_import
#from six import iteritems, itervalues
#from six.moves import range

import os

#from ._file_reader import FileReader
#from .f06_table import F06Table

#from six import iteritems, iterkeys, itervalues, 
from six import add_metaclass


_tables = set()


def _register_class(kls):
    _tables.add(kls)


class RegisterClass(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(RegisterClass, cls).__new__(cls, clsname, bases, attrs)
        _register_class(newclass)
        return newclass


@add_metaclass(RegisterClass)
class F06Table(object):

    _last_table = None

    @classmethod
    def find_table(cls, table_lines):
        if cls._last_table is not None:
            if cls._last_table.is_match(table_lines):
                return cls._last_table

        for table in _tables:
            if table.is_match(table_lines):
                cls._last_table = table
                return table

        return None

    @classmethod
    def is_match(cls, table_lines):
        return False

    def __init__(self):
        self.header = []
        self.data = []
        self.line_number = -1

    def to_punch(self):
        raise NotImplementedError

    def set_data(self, table_lines):
        raise NotImplementedError

    def _load_factor(self):
        raise NotImplementedError

class _DummyTable(object):
    def __init__(self):
        self.header = []
        self.data = []
        self.line_number = -1
        self.table_format = None


class TableFormat(object):
    def __init__(self):
        self.header_check = b'D I S P L A C E M E N T   V E C T O R'
        self.header_check_line = 2
        self.header_lines = 5


class F06Reader(object):
    def __init__(self, filename):
        self.file = FileReader(filename)

        self._done_reading = False

        self._table_formats = [TableFormat()]

        self._current_table = None

        self._callback = None

    def register_callback(self, callback):
        assert callable(callback)
        self._callback = callback

    def read(self):
        while not self._done_reading:
            table_lines, line_number = self._read_table()
            if self._done_reading:
                break

            table_format = F06Table.find_table(table_lines)

            if table_format is None:
                self._process_table(self._current_table)
                self._current_table = None
                continue

            table = table_format()
            table.set_data(table_lines)
            table.line_number = line_number

            for i in range(len(table.header)):
                table.header[i] = table.header[i].strip()

            if self._current_table is None:
                self._current_table = table
            else:
                if self._current_table.header == table.header:
                    self._current_table.data.extend(table.data)
                else:
                    self._process_table(self._current_table)
                    self._current_table = table

        if self._current_table is not None:
            self._process_table(self._current_table)
            self._current_table = None

    def _process_table(self, table):
        if table is None:
            return

        pch_table = table.to_punch()

        if isinstance(pch_table, (list, tuple)):
            for table in pch_table:
                self._callback(table)
        else:
            self._callback(pch_table)

    def _read_table(self):
        table_lines = []

        first_line = self._find_next_table()
        if self._done_reading:
            return None, None

        line_number = self.file.line_number()

        while True:
            if first_line is not None:
                line = first_line
                first_line = None
            else:
                line = self.file.next_line()

            self._check_done_reading(line)
            if self._done_reading:
                break

            # print(line)

            if line.startswith(b'1'):
                break

            table_lines.append(line)

        return table_lines, line_number

    def _find_next_table(self):
        while True:
            line = self.file.next_line()
            self._check_done_reading(line)
            if self._done_reading:
                break

            if line.startswith(b'0') and b'SUBCASE' in line:
                return line

        return None

    def _check_done_reading(self, line):
        if line is None or b'END OF JOB' in line:
            self._done_reading = True



class FileReader(object):
    def __init__(self, filename):
        self.filename = filename

        self.filesize = os.path.getsize(self.filename)

        self.f = open(self.filename, 'rb')

        some_data = self.f.read(1024)

        if b'\r\n' in some_data:
            self.separator = b'\r\n'
        else:
            self.separator = b'\n'

        self.f.seek(0)

        self.chunksize = int(self.filesize / 100)

        maxchunk = 1024 * 1000

        if self.chunksize > maxchunk:
            self.chunksize = maxchunk

        self._counter = 0

        self._data = []
        self._old_data = None
        self._new_data = None

        self._data_read = 0
        self._old_data_read = 0

        self._line_number = 0

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.f.close()
        except AttributeError:
            pass

        self.f = None

    def next_line(self):
        try:
            tmp = self._data[self._counter]
            self._counter += 1
            self._line_number += 1
            return tmp
        except IndexError:
            if self._new_data is not None:
                self._data = self._new_data
                self._new_data = None
                self._counter = 0
                self._line_number = 0

                return self._data[self._counter]

            self._old_data = self._data

            self._old_data_read = self._data_read

            # print('reading data...')

            _data = self.f.read(self.chunksize)

            _data_len = _data.rfind(self.separator) + 1

            rewind = len(_data) - _data_len

            self.f.seek(self.f.tell() - rewind)

            _data = _data[:_data_len]

            self._data_read += len(_data)

            if len(_data) == 0:
                return None

            self._data = _data.split(self.separator)
            self._data.pop()
            self._counter = 0

            try:
                tmp = self._data[self._counter]
                self._counter += 1
                self._line_number += 1
                return tmp
            except IndexError:
                return None

    def previous_line(self):
        self._counter -= 1
        self._line_number -= 1

        try:
            return self._data[self._counter]
        except IndexError:
            if self._old_data is not None:
                self._new_data = self._data
                self._data = self._old_data
                self._old_data = None
                self._counter = len(self._data) - 1
                self._line_number = self._counter

                return self._data[self._counter]
            else:
                return None

    def line_number(self):
        return self._line_number


class DisplacementTable1(F06Table):
    @classmethod
    def is_match(cls, table_lines):
        try:
            return b'D I S P L A C E M E N T   V E C T O R' in table_lines[2]
        except IndexError:
            return False

    def set_data(self, table_lines):
        del self.header[:]
        del self.data[:]

        self.header.extend(table_lines[:5])
        self.data.extend(table_lines[5:])

    def to_punch(self):
        from h5Nastran.post_process.result_readers.punch import PunchTableData

        table_data = PunchTableData()
        header = table_data.header

        header._results_type = 'DISPLACEMENTS'
        header.lineno = self.line_number
        header.title = ''
        header.subtitle = ''
        header.label = ''
        header.other = {}
        header.real_output = True
        header._subcase_id = self.header[0].split()[-1].decode()

        load_factor = self._load_factor()

        if load_factor is not None:
            header.other['LOAD FACTOR'] = load_factor

        data = table_data.data

        for line in self.data:
            data.append(
                [line[1:14], line[14:24], line[24:39], line[39:54], line[54:69], line[69:84], line[84:99], line[99:114]]
            )

        return table_data

    def _load_factor(self):
        if b'LOAD STEP' in self.header[1]:
            tmp = self.header[1].split()
            return tmp[2].decode()
        else:
            return None
