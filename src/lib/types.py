from datetime import datetime
from typing import Generator

SheetRowGenerator = Generator[tuple[datetime, datetime, str], None, None]
