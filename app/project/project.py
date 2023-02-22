import os
import dask.dataframe as dd
from tqdm import tqdm

class ResearchProject:
    def __init__(self, project_path:str):
        self.project_path = project_path
        self.df = dd.concat([dd.read_parquet(os.path.join(self.project_path, file)) for file in tqdm(os.listdir(self.project_path))])