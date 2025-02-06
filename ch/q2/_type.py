from qiime2.plugin import SemanticType
from q2_types.sample_data import SampleData

Hulls = SemanticType(
    'Hulls', variant_of=SampleData.field['type'])
