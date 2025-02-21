"""File operations and data Extraction """
from typing import Optional, Dict

import pandas as pd
from lxml import etree

#pylint: disable=E0402
from .common import logger

class FileOperations:
    """ FIle IO """
    @staticmethod
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
            logger.error(f"Error parsing XML file {path}: {e}")
            return None
        # pylint: disable=W0718
        # i know that my catch all Exception is very broad
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def parse_txt_file(path:str) -> Optional[str]:
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
            logger.error(f"Error parsing txt file {path}: {e}")
            return None
        # pylint: disable=W0718
        # i know that my catch all Exception is very broad
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def write_to_xls(df:pd.DataFrame, path:str="output.xls",sheet_name:str="Sheet1") -> bool:
        """ Writes data to xls file 

        Args:
            data (list): data to be written into the file 
            path (str): path to the file, defaults to output.xls

        Returns:
            bool: True if the successful
        """
        try:
            with pd.ExcelWriter(path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            logger.info(f"Data successfully written to {path}, sheet '{sheet_name}'.")
            return True
        # pylint: disable=W0718
        # i know that my catch all Exception is very broad
        except Exception as e:
            logger.error(f"An error occurred while writing to Excel: {e}")
            return False


class X83_Parser:
    """Class to parse X83"""

    def __init__(self, xml_root:etree._Element):
        self.root:etree._Element = xml_root
        self.namespace:str = "http://www.gaeb.de/GAEB_DA_XML/DA83/3.3"

    @staticmethod
    def remove_namespace(element_tag:str) -> str:
        """removes the namespace from a tag"""
        if isinstance(element_tag, str):
            return element_tag.split('}')[-1]
        return str(element_tag)
    
    @staticmethod
    def has_children(element:etree._Element) -> bool:
        """Checks if an element has any child elements"""
        return next(element.iterchildren(), None) is not None

    @staticmethod
    def is_whitespace(string:str) -> bool:
        """Checks if a string consists only of whitespace characters."""
        return string.isspace()

    def create_dict(self) -> Dict:
        """
        Creates and returns a  Dicts (for each in the form:
            {"ID":{
                "Quantity": int, 
                "Units": str,
                "DescriptionID": str,
                "Description": dict
            }, 
            ID:{
                ...
            },
            }
            
        Returns:
            List[Dict]: _description_
        """
        def build_description(element:etree._Element, temp:list):
            """concats the information in the <Text> Tag into a single string """
            for child in element:
                if self.has_children(child):
                    build_description(child, temp)
                elif child.text and not self.is_whitespace(child.text):
                    temp.append(child.text)
        
        def add_values_recursive(element:etree._Element):
            """iterates over Tags, creates key-value-pair if there a no children"""
            for child in element:
                if isinstance(child, etree._Comment):
                    continue
                if self.remove_namespace(child.tag) == "Text":
                    temp:list = []
                    build_description(child, temp)
                    dictionary[ID]["Description"] = "".join([f" {el} " for el in temp])
                    return
                if self.has_children(child):
                    add_values_recursive(child)
                elif not self.has_children(child) and \
                    child.tag not in ["{%s}"% self.namespace +tag for tag in ['p', 'span']]:
                    if child.text and not self.is_whitespace(child.text):
                        dictionary[ID][self.remove_namespace(child.tag)] = child.text

        dictionary:dict = {}
        for element in self.root.iter("{%s}Item" % self.namespace):
            ID:str = element.attrib.get('ID')
            dictionary[ID] = {}
            add_values_recursive(element)
        return dictionary
