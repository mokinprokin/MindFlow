from aiogoogle import Aiogoogle
import asyncio
from .token import TokenService
from ..schemas.google_sheets import GoogleSheet


class GoogleSheetsService:
    @classmethod
    async def get_last_sheet(cls) -> GoogleSheet:

        creds = await asyncio.to_thread(TokenService.get_google_credentials)

        async with Aiogoogle(**creds) as google:
            drive_v3 = await google.discover("drive", "v3")

            query = (
                "mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
            )
            results = await google.as_user(
                drive_v3.files.list(
                    q=query,
                    pageSize=1,
                    fields="files(id, name, createdTime, webViewLink)",
                    orderBy="createdTime desc",
                )
            )

            files = results.get("files", [])
            file_data = files[0] if files else None

            if not file_data:
                return None

            return GoogleSheet.model_validate(file_data)

    @classmethod
    async def get_sheet_data(cls, spreadsheet_id, range_name="A1:Z100"):
        creds = await asyncio.to_thread(TokenService.get_google_credentials)

        async with Aiogoogle(**creds) as google:
            sheets_v4 = await google.discover("sheets", "v4")

            result = await google.as_user(
                sheets_v4.spreadsheets.values.get(
                    spreadsheetId=spreadsheet_id, range=range_name
                )
            )

            return result.get("values", [])


