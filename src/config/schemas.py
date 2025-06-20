from dataclasses import dataclass
from hydra.core.config_store import ConfigStore


# --- data_eng.yaml ---
@dataclass
class DataSourceConfig:
    url: str
    external_data_dir: str
    filename: str


@dataclass
class RawDataConfig:
    raw_data_dir: str
    raw_filename: str


@dataclass
class CleanedDataConfig:
    cleaned_data_dir: str
    cleaned_filename: str


@dataclass
class ProcessedDataConfig:
    processed_data_dir: str
    processed_filename: str


@dataclass
class SplitedDataConfig:
    train_data_dir: str
    train_filename: str
    test_data_dir: str
    test_filename: str
    split_ratio: float
    random_state: int


@dataclass
class DataEngConfig:
    data_source: DataSourceConfig
    raw_data: RawDataConfig
    cleaned_data: CleanedDataConfig
    processed_data: ProcessedDataConfig
    splited_data: SplitedDataConfig


# --- model_eng.yaml ---
@dataclass
class ModelDataConfig:
    train_data_dir: str
    train_filename: str
    test_data_dir: str
    test_filename: str
    target_data: str
    models_dir: str
    file_model: str
    reports_dir: str


@dataclass
class RFParamsConfig:
    criterion: str
    max_depth: int
    min_sample_leaf: int
    min_sample_split: int
    n_estimators: int
    oob_score: bool


@dataclass
class EstimatorsConfig:
    RandomForestRegressor: "RandomForestRegressorConfig"


@dataclass
class RandomForestRegressorConfig:
    params: RFParamsConfig


@dataclass
class RandomizedSearchCVParamsConfig:
    n_estimators: list[int]
    criterion: list[str]
    max_depth: list[int]
    min_samples_split: list[int]
    min_samples_leaf: list[int]


@dataclass
class RandomizedSearchCVConfig:
    n_iter: int
    scoring: str
    verbose: int
    cv: int
    random_state: int
    n_jobs: int
    return_train_score: bool
    params: RandomizedSearchCVParamsConfig


@dataclass
class ReportsConfig:
    scores: str
    params: str


@dataclass
class MLflowConfig:
    mlruns_path: str
    tracking_uri: str


@dataclass
class ModelEngConfig:
    model_data: ModelDataConfig
    estimators: EstimatorsConfig
    RandomizedSearchCV: RandomizedSearchCVConfig
    reports: ReportsConfig
    mlflow: MLflowConfig


cs = ConfigStore.instance()
cs.store(name="data_eng_schema", node=DataEngConfig)
cs.store(name="model_eng_schema", node=ModelEngConfig)
