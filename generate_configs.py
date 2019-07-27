import os
import pickle
import sys
import yaml
import pandas as pd
import numpy as np


def generate_agg_config(data_path, folder_name, depth):
    """
    Generates config file for aggregator

    :return: None
    """
    folder_configs = folder_name + '/configs'
    if not os.path.exists(folder_configs):
        os.makedirs(folder_configs)
    config_file = os.path.join(folder_configs, 'config_agg.yml')

    # extract feature statistics and generate model spec:
    create_model_spec(folder_configs, data_path)

    model = {
        'name': 'DTFFLModel',
        'path': 'ffl_framework.model.dt_ffl_model',
        'spec': os.path.join(folder_configs, 'dt_model_spec.pickle')
    }

    connection = {
        'name': 'FlaskConnection',
        'path': 'ffl_framework.connection.flask_connection',
        'info': {
            'ip': '127.0.0.1',
            'port': 5000
        },
        'synch': False
    }

    data = {
        'name': "HospitalDataHandler",
        'path': "hospital_data_handler",
        'info': {
                'txt_file':
                    str(data_path)
        }
    }

    fusion = {
        'name': 'DecisionTreeFusionHandler',
        'path': 'ffl_framework.aggregator.fusion.dt_fusion_handler'
    }

    hyperparams = {
        'global': {'max_depth': int(depth)}
    }

    protocol_handler = {
        'name': 'ProtoHandler',
        'path': 'ffl_framework.aggregator.protohandler.proto_handler'
    }
    content = {
        'connection': connection,
        'data': data,
        'model': model,
        'fusion': fusion,
        'hyperparams': hyperparams,
        'protocol_handler': protocol_handler
    }

    with open(config_file, 'w') as outfile:
        yaml.dump(content, outfile)

    print('Finished generating config file for aggregator. Files can be found in: ',
          os.path.abspath(config_file))


def generate_party_config_file(data_path, folder_name, party_num):
    
    folder_configs = folder_name + '/configs'
    if not os.path.exists(folder_configs):
        os.makedirs(folder_configs)
    
    # extract feature statistics and generate model spec:
    create_model_spec(folder_configs, data_path)

    # Now generate automatically config files for all parties:

    config_file = os.path.join(
        folder_configs, 'config_' + folder_name + '.yml')
    model = {
        'name': 'DTFFLModel',
        'path': 'ffl_framework.model.dt_ffl_model',
        'spec': os.path.join(folder_configs, 'dt_model_spec.pickle')
    }

    connection = {
        'name': 'FlaskConnection',
        'path': 'ffl_framework.connection.flask_connection',
        'info': {
            'ip': '127.0.0.1',
            'port': 8085 + int(party_num)
        },
            'synch': False
    }
    data = {
        'name': "HospitalDataHandler",
        'path': "hospital_data_handler",
        'info': {
            'txt_file': data_path
        }
    }
    protocol_handler = {
        'name': 'ProtocolHandlerPlainFL',
        'path': 'ffl_framework.party.protocol_handler_plain_fl'
    }
    aggregator = {
        'ip': '127.0.0.1',
        'port': 5000
    }
    content = {
        'connection': connection,
        'data': data,
        'model': model,
        'protocol_handler': protocol_handler,
        'aggregator': aggregator
    }

    with open(config_file, 'w') as outfile:
        yaml.dump(content, outfile)

    print('Finished generating config file. Files can be found in: ',
          os.path.abspath(os.path.join(folder_configs, 'config_party')))


def create_model_spec(pickle_path, data_path):
    """
    Create model_spec and saves it in folder_path
    :param data_path: (optional) A given path where the data is stored
    :param pickle_path: Generated model_spec is also stored in this path
    :return: None
    """
    data_file = data_path
    dataset = pd.read_csv(data_file, dtype='category')
    spec = dict()
    spec['list_of_features'] = list(range(dataset.shape[1] - 1))

    feature_values = list()
    for feature in range(dataset.shape[1]):
        if dataset.columns[feature] != 'class':
            new_feature = dataset[dataset.columns[feature]].cat.categories
            feature_values.append(new_feature.tolist())
    spec['feature_values'] = feature_values
    
    list_of_labels = dataset['class'].cat.categories
    spec['list_of_labels'] = list_of_labels.tolist()

    f_spec = os.path.join(pickle_path, 'dt_model_spec.pickle')
    with open(f_spec, 'wb') as f:
        pickle.dump(spec, f)


if __name__ == '__main__':
    config_type = sys.argv[1]
    folder_name = sys.argv[2]
    file_name = sys.argv[3]
    data_path = os.path.join(folder_name, file_name)

    
    if config_type == "party":
        party_num = sys.argv[4]
        generate_party_config_file(data_path, folder_name, party_num)
    elif config_type == "aggregator":
        depth = sys.argv[4]
        generate_agg_config(data_path, folder_name, depth)
    else:
        raise NameError("Please select to generate either a 'party' or a " 
                        "'aggregator' config file")
