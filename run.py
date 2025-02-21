""" Used to run toolchain from commandline"""
import argparse

from toolchain.llm import LLM
from toolchain.util import Utils
from toolchain.common import logger
from toolchain.file_operations import FileOperations, X83_Parser


def main(path_to_xml:str,path_to_txt:str,path_to_output:str) -> None:
    """runs the toolchain from command line

    Args:
        path_to_xml (str): does what is says on the tin
        path_to_txt (str): "                          "
        path_to_output (str):"                        "
    """
    logger.info(f"reading XML at {path_to_xml}")
    root = FileOperations.parse_xml_file(path_to_xml)
    xml_parser:X83_Parser = X83_Parser(root)
    xml_dict:dict = xml_parser.create_dict()

    logger.info(f"reading TXT at {path_to_txt}")
    content:str = FileOperations.parse_txt_file(path_to_txt)
    sections:list = content.split("\n\n")
    sections:list = [section.strip("\n") for section in sections]

    language_model:LLM = LLM('toolchain_model')

    logger.info("creating prompts")
    prompts:list = []
    for i,value in enumerate(xml_dict.values()):
        prompts.append(Utils.create_prompt(value['Description'], sections[i]))

    logger.info("getting responses... this may take a moment")
    try:
        responses:list = [language_model.get_response(prompt) for prompt in prompts]
        #logger.debug(responses)
    except Exception as e:
        logger.error(f"failed due to {e}")

    data:list=[output.response for output in responses]
    df = Utils.create_dataframe_from_responses(data)

    logger.info(f"writing to {path_to_output}")
    try:
        FileOperations.write_to_xls(df)
    except Exception as e:
        logger.error(f"writing failed due to {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Interface for the toolchain")
    parser.add_argument("path_to_xml",
                        type=str,
                        help="Path to the XML-File."
                        )
    parser.add_argument("path_to_txt",
                        type=str,
                        help="Path to the TXT-File"
                        )
    parser.add_argument("path_to_output",
                        type=str,
                        help="Path to the Output File (xls)",
                        default="output.xls"
                        )
    args = parser.parse_args()
    main(args.path_to_xml, args.path_to_txt, args.path_to_output)
