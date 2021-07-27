# Transforms JSON data into a list of lists based on field spec


class USCensusTransformer:
    def __init__(self):
        pass

    @staticmethod
    def transform(fields, data):
        transformed_data = []
        for row in data:
            new_row = []
            for field in fields:
                new_row.append(row[field])
            transformed_data.append(new_row)
        return transformed_data
