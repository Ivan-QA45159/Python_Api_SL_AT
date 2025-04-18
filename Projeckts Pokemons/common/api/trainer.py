"""
Модуль для работы с тренирами
"""

from common.api.basic import Api


class TrainerApi(Api):
    """
    Methods for trainer
    """
    def get_trainers(self, trainer_id: int = None):
        """
        Get trainer
        """
        url = f'{self.url}/trainers'
        return self.get(url=url, params={'trainer_id': trainer_id})
    