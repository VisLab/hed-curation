import os
from bsmschema.models import BIDSStatsModel
if __name__ == '__main__':

    models = ['model-factor-leftvsright_smdl.json', 'model-factor-successvsunsuccess_smdl.json']
    models = ['model-factor-successvsunsuccess_smdl.json']
    models = ['model-factor-leftvsright_smdl.json']
    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./models")
    for model in models:
        print(f"\n\nValidating {model}")
        schema_file = os.path.join(base_path, model)
        # try:
        BIDSStatsModel.parse_file(schema_file)
        # except Exception as e:
        #    print("failed")