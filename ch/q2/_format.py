import qiime2.plugin.model as model
from qiime2.plugin import ValidationError


class HullsFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        with self.open() as fh:
            # check the header column names
            header = fh.readline()
            comp_columns = [head.replace('\n', '')
                            for head in header.split('\t')][1:]
            # ensure there at least two columns
            if len(comp_columns) < 3:
                raise ValidationError(
                    'There should be more than two '
                    'columns in the hull format')

    def _validate_(self, level):
        record_count_map = {'min': 1, 'max': None}
        self._validate(record_count_map[level])


def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


HullsDirectoryFormat = model.SingleFileDirectoryFormat(
    'HullsDirectoryFormat', 'hulls.tsv',
    HullsFormat)
