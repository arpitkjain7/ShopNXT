from pydantic import BaseModel


class FileUpload(BaseModel):
    filePath: str


class S3Upload(BaseModel):
    bucket: str
    key: str


class PostProcessing(BaseModel):
    batch_id: str
    classified_label: str


class TextractException(BaseModel):
    batch_id: str


class MCRUpload(BaseModel):
    batch_id: str
    file_name: str
    file_path: str
    applicant: str
    disaster_id: str
    project_id: str
    rfr_id: str
    location: str


class UpdateExtractedValues(BaseModel):
    extracted_data: list
    batch_id: str


class UnknownToKnown(BaseModel):
    classification_dict: dict
    batch_id: str
