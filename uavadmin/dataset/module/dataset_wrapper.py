import copy
import logging
import traceback

from django.db import transaction

from uavadmin.dataset.models import DsDataset, DsImage, DsPatient

logger = logging.getLogger(__name__)


def clone_dataset(old_dataset):
    try:
        with transaction.atomic():
            new_dataset = copy.deepcopy(old_dataset)
            new_dataset.id = None
            new_dataset.name = f"{old_dataset.name}_new"
            new_dataset.save()

            n_patient = 0
            n_image = 0
            old_patient_list = DsPatient.objects.filter(dataset_id=old_dataset.id)
            for old_patient in old_patient_list:
                new_patient = copy.deepcopy(old_patient)
                new_patient.id = None
                new_patient.dataset_id = new_dataset.id
                new_patient.save()
                n_patient += 1

                old_image_list = DsImage.objects.filter(patient_id=old_patient.id)
                for old_image in old_image_list:
                    new_image = copy.deepcopy(old_image)
                    # DsImage.objects.create(**old_image.__dict__)
                    new_image.id = None
                    new_image.patient_id = new_patient.id
                    new_image.save()
                    n_image += 1
            logger.info(f"clone dataset_id={old_dataset.id} p={n_patient} i={n_image}")
            return new_dataset
    except Exception as e:
        logging.error("deep copy failed")
        traceback.print_exc()
    return None
