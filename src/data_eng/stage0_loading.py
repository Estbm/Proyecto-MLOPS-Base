import sys
import os
import pandas as pd
import requests
import hydra

from app_logging import logging
from app_exception.exception import AppException
from config.schemas import DataEngConfig


class GetData:
    """
    The main functionality is to get data from external source
    Function return data
    """

    def __init__(self):
        pass

    def get_data(self, config: DataEngConfig):
        try:
            logging.info("Getting the data from the external source")

            # URL del archivo CSV en GitHub
            # aquí se asume que config_path es la URL del archivo CSV
            # github_csv_url = config_path
            github_csv_url = config.data_source.url

            # Ruta local donde se guardará el archivo
            # self.external_data = "data/external"
            self.external_data = config.data_source.external_data_dir
            os.makedirs(self.external_data, exist_ok=True)
            # local_path = os.path.join(self.external_data, "Consignment_pricing.csv")
            local_path = os.path.join(self.external_data, config.data_source.filename)

            if not os.path.isfile(local_path):
                # Descargar el archivo CSV desde GitHub
                response = requests.get(github_csv_url)
                response.raise_for_status()  # lanza una excepción si la descarga falla

                with open(local_path, "wb") as f:
                    f.write(response.content)

                logging.info("CSV file downloaded successfully")
            else:
                logging.info("CSV file already exists, skipping download")

            # Leer el archivo CSV descargado
            self.data_path = local_path
            print(local_path)
            self.data = pd.read_csv(self.data_path, sep=",", encoding="utf-8")

            logging.info("Data successfully uploaded from downloaded file")
            return self.data

        except Exception as e:
            logging.error(f"Exception occurred while getting data from the source --> {e}")
            raise AppException(e, sys) from e


@hydra.main(config_path=f"{os.getcwd()}/configs", config_name="data_eng", version_base=None)
def main(cfg: DataEngConfig):
    logging.basicConfig(level=logging.INFO)
    data = GetData().get_data(cfg)
    return data


if __name__ == "__main__":
    # args = argparse.ArgumentParser()
    # args.add_argument(
    #     "--input_path",
    #     default="https://raw.githubusercontent.com/jmem-ec/KRRCourse/ccbd6ccf8389ba0988d53fc9300a64da00e6368b/Consignment_pricing.csv",
    # )

    # parsed_args = args.parse_args()
    # data = GetData().get_data(config_path=parsed_args.input_path)
    main()
