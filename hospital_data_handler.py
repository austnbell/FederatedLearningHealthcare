import logging
import pandas as pd


from ffl_framework.data.data_handler import DataHandler

logger = logging.getLogger(__name__)


class HospitalDataHandler(DataHandler):
    """
    Custom data handler for for hospital readmission dataset.
    """
    def __init__(self, data_config=None):
        super().__init__()
        self.file_name = None
        if data_config is not None:
            if 'txt_file' in data_config:
                self.file_name = data_config['txt_file']

        self.training_dataset, self.x_test, self.y_test = self.load_training_data()

    def load_training_data(self):
        """
        Read hospital readmission file and commits to memory

        :return: A dataset structure
        :rtype: `pandas.core.frame.DataFrame`
        """
        if self.file_name is None:
            raise ValueError("No path to data found")
            
        else:
            try:
                logger.info('Loaded training data from ' +
			                str(self.file_name))
                training_dataset = pd.read_csv(self.file_name,
			                                   dtype='category')
            except:
                raise IOError('Unable to load training data from path '
			                  'provided in config file: ' + self.file_name)
                
        y_test = training_dataset['class'].values.tolist()
        x_test = training_dataset.drop(['class'], axis=1)
        
        return training_dataset, x_test, y_test 

    def get_training_data(self):
        """
        Returns training data set

        :return: A dataset structure
        :rtype: `pandas.core.frame.DataFrame`
        """
        
        return self.training_dataset, (self.x_test, self.y_test)

    def get_dataset_info(self):
        """
        Read hospital data and extract data information

        :return: spec, a dictionary that contains list_of_features,
        feature_values and list_of_labels.
        :rtype: `dict`
        """
        training_dataset, (_, _) = self.get_training_data()
        spec = {}
        spec['list_of_features'] = list(range(training_dataset.shape[1] - 1))

        feature_values = []
        for feature in range(training_dataset.shape[1]):
            if training_dataset.columns[feature] != 'class':
                feature_values.append(
                    training_dataset[training_dataset.columns[feature]].cat.categories)
        spec['feature_values'] = feature_values

        list_of_labels = training_dataset['class'].cat.categories
        spec['list_of_labels'] = list_of_labels.tolist()

        return spec
