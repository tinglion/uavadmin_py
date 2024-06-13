from rest_framework import serializers

from uavadmin.dataset.models import DsDataset, DsImage, DsPatient
from uavadmin.utils.serializers import CustomModelSerializer


class DsDatasetSerializer(CustomModelSerializer):
    """
    序列化器
    """

    num_images = serializers.SerializerMethodField()
    num_images_custom = serializers.SerializerMethodField()

    def get_num_images(self, obj: DsDataset):
        try:
            patients = DsPatient.objects.filter(dataset_id=obj.id)
            if len(patients) > 0:
                return DsImage.objects.filter(
                    patient_id__in=[p.id for p in patients]
                ).count()
            return 0
        except Exception as e:
            logger.error(f"ERROR {e}")

    def get_num_images_custom(self, obj: DsDataset):
        try:
            patients = DsPatient.objects.filter(dataset_id=obj.id)
            if len(patients) > 0:
                return (
                    DsImage.objects.filter(patient_id__in=[p.id for p in patients])
                    .exclude(native_result_custom=None)
                    .count()
                )  # .filter(native_result_custom__isnull=False)
            return 0
        except Exception as e:
            logger.error(f"ERROR {e}")

    class Meta:
        model = DsDataset
        fields = "__all__"
        read_only_fields = ["id"]


class DsPatientSerializer(CustomModelSerializer):
    """
    序列化器
    """

    dataset_name = serializers.SerializerMethodField()

    def get_dataset(self, obj: DsPatient):
        try:
            return DsDataset.objects.get(id=obj.dataset_id)
        except Exception as e:
            return None

    def get_dataset_name(self, obj: DsImage):
        dataset = self.get_dataset(obj)
        return dataset.name if dataset else None

    class Meta:
        model = DsPatient
        fields = "__all__"
        read_only_fields = ["id"]


class DsImageSerializer(CustomModelSerializer):
    """
    序列化器
    """

    patient_uid = serializers.SerializerMethodField()
    dataset_id = serializers.SerializerMethodField()
    dataset_name = serializers.SerializerMethodField()

    def get_patient(self, obj: DsImage):
        try:
            return DsPatient.objects.get(id=obj.patient_id)
        except Exception as e:
            return None

    def get_dataset(self, obj: DsPatient):
        try:
            return DsDataset.objects.get(id=obj.dataset_id)
        except Exception as e:
            return None

    def get_patient_uid(self, obj: DsImage):
        patient = self.get_patient(obj)
        return patient.uid if patient else None

    def get_dataset_id(self, obj: DsImage):
        patient = self.get_patient(obj)
        if patient:
            dataset = self.get_dataset(patient)
            return dataset.id if dataset else None

    def get_dataset_name(self, obj: DsImage):
        patient = self.get_patient(obj)
        if patient:
            dataset = self.get_dataset(patient)
            return dataset.name if dataset else None

    class Meta:
        model = DsImage
        fields = "__all__"
        read_only_fields = ["id"]
