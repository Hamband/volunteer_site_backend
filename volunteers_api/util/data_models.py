from typing import Optional, List

from pydantic import BaseModel, model_validator, ConfigDict

from volunteers_api.util.enums import DegreeType

from .. import i18n


class NewEntryRequestBodyDegree(BaseModel):
    type: DegreeType
    uni: str
    start_year: int
    end_year: int
    major: str

    @model_validator(mode="after")
    def validate(self):
        if self.start_year < 1300:
            raise ValueError(i18n.get("start_year_invalid"))
        if self.end_year < self.start_year:
            raise ValueError(i18n.get("end_year_invalid"))
        if len(self.uni) == 0:
            raise ValueError(i18n.get("uni_invalid"))
        if len(self.major) == 0:
            raise ValueError(i18n.get("major_invalid"))
        return self


class NewEntryRequestBodyContact(BaseModel):
    type: str
    address: str

    @model_validator(mode="after")
    def validate(self):
        errors = []
        if len(self.type) == 0:
            raise ValueError(i18n.get("invalid_contact_type"))
        if len(self.address) == 0:
            raise ValueError(i18n.get("invalid_contact_address"))
        return self


class NewEntryRequestBody(BaseModel):
    first_name: str
    last_name: str
    last_completed_degree: Optional[DegreeType]
    current_degree: Optional[DegreeType]
    fields: List[str]
    degrees: List[NewEntryRequestBodyDegree]
    contacts: List[NewEntryRequestBodyContact]

    @model_validator(mode="after")
    def validate(self):
        if len(self.first_name) == 0:
            raise ValueError(i18n.get("first_name_invalid"))
        if len(self.last_name) == 0:
            raise ValueError(i18n.get("last_name_invalid"))
        if len(self.fields) == 0:
            raise ValueError(i18n.get("fields_empty"))
        if len(self.contacts) == 0:
            raise ValueError(i18n.get("contacts_empty"))
        return self
