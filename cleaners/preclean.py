# Shi Dai, 2019/05/16
# To run before surgical to remove strong RFI that corrupt surgical algorithm

import numpy as np

from coast_guard import cleaners
from coast_guard import config
from coast_guard import clean_utils
from coast_guard import utils
import config_types
#import cleaners
#import config
#import clean_utils
#import config_types
#import utils

class PreCleaner(cleaners.BaseCleaner):
    name = 'preclean'
    description = 'Very rough clean for strong RFI in the sub-integration and frequency domain. '

    def _set_config_params(self):
        self.configs.add_param('prethresh', config_types.FloatVal, \
                         aliases=['prethresh'], \
                         help='The threshold (in number of sigmas) to ' \
                                'pre-clean strong RFI. ')
                                
        self.parse_config_string(config.cfg.preclean_default_params)

    def _clean(self, ar):
        threshold = self.configs.prethresh
        #threshold = 10

        patient = ar.clone()
        patient.pscrunch()
        patient.remove_baseline()
        
        # Get weights
        weights = patient.get_weights()
        # Remove profile from dedispersed data
        patient.dedisperse()
        data = patient.get_data().squeeze()

        # apply weights
        data = clean_utils.apply_weights(data, weights)

        # get the subint v.s. frequency array
        dyn = np.average(data, axis=2)
        std = np.std(dyn)
        mean = np.mean(dyn)
        mask = np.fabs(dyn - mean) > threshold*std

        while np.any(mask):
            dyn[np.fabs(dyn - mean) > threshold*std] = 0.0
            std = np.std(dyn)
            mean = np.mean(dyn)
            mask = np.fabs(dyn - mean) > threshold*std
        
        for (isub, ichan) in np.argwhere(dyn == 0.0):
            # Be sure to set weights on the original archive, and
            # not the clone we've been working with.
            ar.get_Integration(int(isub)).set_weight(int(ichan), 0.0)

Cleaner = PreCleaner

