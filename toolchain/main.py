"""Entry Point of the toolchain"""
from typing import Optional

import pandas as pd
from lxml import etree

#pylint: disable=E0402
from .common import logger
from .llm import LLM

def parse_xml_file(path:str) -> Optional[etree._Element]:
    """ Returns root of the etree 

    Args:
        path (str): path to the xml file

    Returns:
        Optional[etree._Element]: root of etree
    """
    try:
        tree = etree.parse(path)
        root = tree.getroot()
        return root
    except (FileNotFoundError, etree.XMLSyntaxError, OSError) as e:
        logging.error(f"Error parsing XML file {path}: {e}")
        return None
    # pylint: disable=W0718
    # i know that my catch all Exception is very broad
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def parse_txt_file(path:str) -> str:
    """ reads content of txt file and returns it as string

    Args:
        path (str): path to file

    Returns:
        str: content of file
    """
    try:
        with open(path, 'r', encoding='UTF-8') as f:
            return f.read()
    except (FileNotFoundError,OSError) as e:
        logging.error(f"Error parsing txt file {path}: {e}")
        return None
    # pylint: disable=W0718
    # i know that my catch all Exception is very broad
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def write_to_xls(data:list, path:str="output.xls",sheet_name:str="Sheet1") -> bool:
    """ Writes data to xls file 

    Args:
        data (list): data to be written into the file 
        path (str): path to the file, defaults to output.xls

    Returns:
        bool: True if the successful
    """
    try:
        if isinstance(data[0], list) or isinstance(data[0], tuple):
            df = pd.DataFrame(data)
        else:   # This should never be the case !
            df = pd.DataFrame(data, columns=['Data'])

        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Data successfully written to {path}, sheet '{sheet_name}'.")
    # pylint: disable=W0718
    # i know that my catch all Exception is very broad
    except Exception as e:
        print(f"An error occurred while writing to Excel: {e}")


def main():
    path_to_xml: str = 'data/LV.X83'
    path_to_txt: str = 'data/Angebot_Lieferant.txt'
    logger.debug(parse_xml_file(path_to_xml))
    logger.debug(parse_txt_file(path_to_txt))
 
    questions: list = [
        "Is cheese ?",
        "why is cheese ?",
    ]
    while True:
        language_model = LLM()
        for question in questions:
            logger.info(question)
            logger.info(language_model.get_response(question)['response'])
