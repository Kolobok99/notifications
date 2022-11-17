from conf.settings import logger

from apps.mailings import models as mailing_models
from apps.polls.tasks import task_mailing


def mailing_task_creator_and_task_id_updator(instance: mailing_models.Mailing) -> mailing_models.Mailing:
    """
        Создает task_mailing для instance и добавляет/обновляет ему task_id

        Args:
            instance (Mailing): инстанс модели Mailing из прил. mailings

        Returns:
              переданный instance (Mailing) с добавленным/обновленным task_id

    """

    task = task_mailing.apply_async((instance.pk,), eta=instance.start_time)
    instance.task_id = task.task_id
    instance.save()
    logger.debug(f"CREATE <MAILING_TASK> {task.task_id} (start_time={instance.start_time})")
    return instance
