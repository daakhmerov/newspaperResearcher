# Импорт сторонних модулей
import pandas as pd
import numpy as np
import dask.dataframe as dd
import plotly.express as px


class CorporaReport:
    def __init__(self, year: int, tokens, title: str | None = None):
        self.year = year
        self.tokens = tokens.loc[tokens['newspaper_year'] == self.year]
        self.sum = self.sum_tokens_per_issue()
        self.title = title

    def sum_tokens_per_issue(self):
        return self.tokens.loc[self.tokens.newspaper_year == self.year].groupby('newspaper_issue').token_.sum().to_frame().reset_index()

    def pivot_table(self):
        return pd.pivot_table(pd.pivot_table(self.tokens, index=['newspaper_month', 'newspaper_issue'], values=['token_'], aggfunc=sum).reset_index(), index='newspaper_month', values='token_', aggfunc=[min, max, np.median])

    def bar_issues(self, threshold: None | int = None):
        labels = {
            "newspaper_issue": "Номер выпуска газеты, №",
            "token_": "Вхождение токена в корпус, ед."
        }

        if self.title == None:
            fig = px.bar(self.sum if threshold ==
                         None else self.sum.loc[self.sum.token_ >= threshold], x='newspaper_issue', y='token_', labels=labels)
            fig.update_traces(marker=dict(color="crimson"))
            fig.show()
        else:
            fig = px.bar(self.sum if threshold == None else self.sum.loc[self.sum.token_ >=
                         threshold], x='newspaper_issue', y='token_', title=self.title, labels=labels)
            fig.update_traces(marker=dict(color="crimson"))
            fig.show()
