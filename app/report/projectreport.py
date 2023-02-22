# Импорт сторонних модулей
import pandas as pd
import numpy as np
import plotly.express as px


class ProjectReport:
    def __init__(self, tokens, title: str | None):
        self.tokens = tokens
        self.title = title

    def pivot_table(self):
        return pd.pivot_table(pd.pivot_table(self.tokens, index=['newspaper_year', 'newspaper_issue'], values=['token_'], aggfunc=np.sum).reset_index(), index='newspaper_year', values='token_', aggfunc=[min, max, np.median])

    def bar_corporas(self):
        labels = {
            "newspaper_year": "Год издания выпусков, гг.",
            "token_": "Сумма вхождений токенов в корпус, ед."
        }

        if self.title == None:
            fig = px.bar(pd.pivot_table(pd.pivot_table(self.tokens, index=['newspaper_year', 'newspaper_issue'], values=['token_'], aggfunc=np.sum).reset_index(
            ), index='newspaper_year', values='token_', aggfunc=sum).reset_index(), x='newspaper_year', y='token_', labels=labels)
            fig.update_traces(marker=dict(color="crimson"))
            fig.show()
        else:
            fig = px.bar(pd.pivot_table(pd.pivot_table(self.tokens, index=['newspaper_year', 'newspaper_issue'], values=['token_'], aggfunc=np.sum).reset_index(
            ), index='newspaper_year', values='token_', aggfunc=sum).reset_index(), x='newspaper_year', y='token_', labels=labels, title=self.title)
            fig.update_traces(marker=dict(color="crimson"))
            fig.show()
