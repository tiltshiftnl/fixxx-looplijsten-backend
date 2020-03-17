import math
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from woonfraude_model import score

from api.fraudprediction.models import FraudPrediction

class Command(BaseCommand):
    help = 'Uses the fraud prediction model to score and store Predictions'

    def handle(self, *args, **options):
        keys = ['adres', 'bwv_adres_periodes', 'bbga', 'hotline',
                'personen', 'personen_hist', 'stadia', 'zaken']
        dbconfig = self.get_database_configs(keys)

        print(dbconfig)

        case_ids = self.get_case_ids_to_score()
        scorer = score.Scorer(cache_dir=settings.FRAUD_PREDICTION_CACHE_DIR, dbconfig=dbconfig)
        results = scorer.score(zaak_ids=case_ids, zaken_con=connections[settings.BWV_DATABASE_NAME])

        try:
            results = results.to_dict(orient='index')

            for case_id in case_ids:
                case_result = results.get(case_id)
                print(case_result.get('business_rules'))
                print(case_result.get('shap_values'))
                try:
                    FraudPrediction.objects.update_or_create(
                        case_id=case_id,
                        defaults={
                            'fraud_probability': case_result.get('prob_woonfraude'),
                            'fraud_prediction': case_result.get('prediction_woonfraude'),
                            'business_rules': self.clean_dictionary(case_result.get('business_rules')),
                            'shap_values': self.clean_dictionary(case_result.get('shap_values'))
                        }
                    )
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)

    def get_database_configs(self, keys=[]):
        config = {}
        for key in keys:
            config[key] = self.get_database_config()
        return config

    def get_database_config(self):
        config = settings.DATABASES[settings.BWV_DATABASE_NAME]
        config = {
            'host': config.get('HOST'),
            'db': config.get('NAME'),
            'user': config.get('USER'),
            'password': config.get('PASSWORD')
        }
        return config

    def get_case_ids_to_score(self):
        return ['192026_1', '138168_5']

    def clean_dictionary(self, dictionary):
        '''
        Replaces dictionary NaN values with 0
        '''
        dictionary = dictionary.copy()

        for key, value in dictionary.items():
            if math.isnan(value):
                dictionary[key] = 0.0

        return dictionary
