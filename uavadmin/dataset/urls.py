from django.urls import include, path
from rest_framework import routers

from uavadmin.dataset.view import (
    DispatchView,
    DsDataset,
    DsImageView,
    DsModelExecView,
    DsModelView,
    DsPatient,
    ImportDataset,
)

DsDataset_url = routers.SimpleRouter()
DsDataset_url.register(r"ds_dataset", DsDataset.DsDatasetViewSet)
DsDataset_url.register(r"ds_patient", DsPatient.DsPatientViewSet)
DsDataset_url.register(r"ds_image", DsImageView.DsImageViewSet)
DsDataset_url.register(r"ds_model", DsModelView.DsModelViewSet)
DsDataset_url.register(r"ds_model_exec", DsModelExecView.DsModelExecViewSet)

urlpatterns = [
    path("", include(DsDataset_url.urls)),
]
urlpatterns += [path(r"ds_lcmed_dispatch", DispatchView.dispatchView.as_view())]
urlpatterns += [
    path(r"ds_dataset/import_zip", ImportDataset.multipleFileUpload.as_view())
]
