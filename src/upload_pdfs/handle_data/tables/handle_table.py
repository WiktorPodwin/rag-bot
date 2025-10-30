from upload_pdfs.utils import summarize_object
from docling_core.types.doc import TableItem

from typing import List
import pandas as pd
import numpy as np


class HandleTables:

    def _convert_to_df(self, table: TableItem) -> pd.DataFrame:
        return table.export_to_dataframe()

    def _check_if_df_is_empty(self, df: pd.DataFrame) -> bool:
        if df.empty:
            return True
        pd.set_option("future.no_silent_downcasting", True)
        return df.replace("", np.nan).isna().all().all()

    def _summarize_table(self, df: pd.DataFrame) -> str:

        def convert_to_markdown(df: pd.DataFrame) -> str:
            return df.to_markdown()

        message_content = f"Summarize the following table up to 8 sentences (can be shorter): {convert_to_markdown(df)}"
        # return summarize_object(message_content)
        return "summary of some table"

    def handle_tabular_data(self, table: TableItem) -> str:
        df = self._convert_to_df(table=table)

        if self._check_if_df_is_empty(df=df):
            return ""

        return self._summarize_table(df=df)
