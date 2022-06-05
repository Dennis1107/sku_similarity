import pandas as pd
import json
import os


def read_sku_json(path: str = "data/Mercedes-test-data.json") -> pd.DataFrame:
    """Read json data and transform to pandas dataframe

    Args:
        path (str, optional): location of json file. Defaults to "../Mercedes-test-data.json".

    Returns:
        pd.DataFrame: json input as dataframe
    """
    with open(path, "r") as f:
        data = json.load(f)
    data_sku = pd.DataFrame.from_dict(data, orient="index")
    return data_sku


def return_column_names(data_input: pd.DataFrame) -> list:
    """returns column names as list

    Args:
        data_input (pd.DataFrame): input dataframe

    Returns:
        list: columns names as list
    """
    return data_input.columns


def columns_to_numerical(data_input: pd.DataFrame, column_names: list) -> pd.DataFrame:
    """Keep only numbers in each column and transform to numerical

    Args:
        data_input (pd.DataFrame): input dataframe
        column_names (list): column names for which this function should be applied

    Returns:
        pd.DataFrame: numerical dataframe
    """
    for column in column_names:
        data_input[column] = data_input[column].str.extract("(\d+)")
    data_input = data_input.astype(int)
    return data_input


def index_reset_rename(data_input: pd.DataFrame) -> pd.DataFrame:
    """apply reset of index in order to use the sku name as column and rename it

    Args:
        data_input (pd.DataFrame): input dataframe

    Returns:
        pd.DataFrame: input dataframe including additional sku column
    """
    data_input = data_input.reset_index()
    data_input = data_input.rename(columns={"index": "sku"})
    return data_input


def check_for_sku_existance(data_input: pd.DataFrame, sku_code: str) -> bool:
    """checks if supplied sku code exists in the json data

    Args:
        data_input (pd.DataFrame): input dataframe
        sku_code (str): provided sku code

    Raises:
        ValueError: sku code does not exist

    Returns:
        bool: True if exits
    """
    if any(data_input.sku.str.contains(sku_code)):
        return True
    else:
        raise ValueError("Provided sku-code does not exist!")


def split_dataframe(data_input: pd.DataFrame, sku_code: str):
    """Split the whole dataset into the sku code which is the target and the rest of the sku codes for which similarity should be checked

    Args:
        data_input (pd.DataFrame): input dataframe
        sku_code (str): sku_code which is searched

    Returns:
        pd.Dataframe: dataframe containing all other sku except the requested one
        pd.Dataframe: dataframe containing the requested sku
    """
    data_search_space = data_input[data_input.sku != sku_code].reset_index(drop=True)
    data_target_space = data_input[data_input.sku == sku_code].reset_index(drop=True)
    return data_search_space, data_target_space


def calculate_similarity_score(
    data_search_input: pd.DataFrame, data_target_input: pd.DataFrame, column_names: list
) -> pd.DataFrame:
    """calculate the similarity score.
    Similarity is the absolute sum of column wise deviations from the target sku.

    Args:
        data_search_input (pd.DataFrame): dataframe containing all other sku except the requested one
        data_target_input (pd.DataFrame): dataframe containing the requested sku
        column_names (list): column names for which this function should be applied

    Returns:
        pd.DataFrame: dataframe including column with similarity scores
    """
    data_search_input["similarity_scores"] = 0
    for column in column_names:
        data_search_input["similarity_scores"] = data_search_input[
            "similarity_scores"
        ] + abs(data_search_input[column] - data_target_input[column][0])
    return data_search_input


def get_n_similar_sku(data_input: pd.DataFrame, number_sku: int) -> pd.DataFrame:
    """return most similar sku

    Args:
        data_input (pd.DataFrame): input dataframe
        number_sku (int): number of returned sku codes

    Returns:
        pd.DataFrame: filtered dataframe
    """
    data_input = data_input.sort_values(by="similarity_scores").reset_index(drop=True)
    data_most_similar = data_input[: int(number_sku)].reset_index(drop=True)
    return data_most_similar


def apply_similarity_calculation(sku_code: str, input_number_sku: int) -> pd.DataFrame:
    """apply the whole similarity pipeline

    Args:
        sku_code (str): search sku code
        input_number_sku (int): number of similar skus

    Returns:
        pd.DataFrame: filtered dataframe based on similarity
    """
    data = read_sku_json()
    column_names = return_column_names(data)
    data = columns_to_numerical(data, column_names)
    data = index_reset_rename(data)
    check_for_sku_existance(data, sku_code)
    data_search, data_target = split_dataframe(data, sku_code)
    data_similarity = calculate_similarity_score(data_search, data_target, column_names)
    data_most_similar = get_n_similar_sku(data_similarity, input_number_sku)
    return data_most_similar
