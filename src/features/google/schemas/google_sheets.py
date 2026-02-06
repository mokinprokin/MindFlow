from pydantic import BaseModel, ConfigDict


class GoogleSheet(BaseModel):
    id: str
    name: str
    webViewLink: str
    model_config = ConfigDict(extra="ignore")


class GoogleSheetData(BaseModel):
    time: str
    task: str
    priority: str
    model_config = ConfigDict(extra="ignore")