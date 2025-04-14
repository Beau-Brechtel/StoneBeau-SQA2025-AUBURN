'''
Akond Rahman 
April 30, 2021 
Parser to file YAML files
'''
import sys
import ruamel.yaml 
from ruamel.yaml.scanner import ScannerError
import json
import constants 
import pathlib as pl
import re
import subprocess
import os
import logging

# Update basepath
base_path = r" "
key_jsonpath_mapping = {}

# Sets up Forensic Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def checkIfWeirdYAML(yaml_script):
    '''
    To filter invalid YAMLs such as ./github/workflows/
    '''
    val = False
    if any(x_ in yaml_script for x_ in constants.WEIRD_PATHS):
        val = True 
    return val 


def keyMiner(dic_, value):
    '''
    Gets the key path to the given value in nested dict/list
    '''
    logging.info(f"keyMiner called with value={value}")  # forensics logging
    if isinstance(dic_, dict):
        for k, v in dic_.items():
            if v == value:
                logging.info(f"Match found at key: {k}")  # forensics logging
                return [k]
            p = keyMiner(v, value)
            if p:
                return [k] + p
    elif isinstance(dic_, list):
        for i in range(len(dic_)):
            if dic_[i] == value:
                logging.info(f"Match found at index: {i}")  # forensics logging
                return [str(i)]
            p = keyMiner(dic_[i], value)
            if p:
                return [str(i)] + p
    return None


def getKeyRecursively(dict_, list2hold, depth_=0):
    '''
    Retrieves all keys in nested dictionary structure
    '''
    logging.info("getKeyRecursively called")  # forensics logging
    if isinstance(dict_, dict):
        for key_, val_ in sorted(dict_.items(), key=lambda x: x[0] if isinstance(x[0], str) else str(x[0])):
            list2hold.append((key_, depth_))
            if isinstance(val_, dict):
                getKeyRecursively(val_, list2hold, depth_ + 1)
            elif isinstance(val_, list):
                for listItem in val_:
                    if isinstance(listItem, dict):
                        getKeyRecursively(listItem, list2hold, depth_ + 1)


def getValuesRecursively(dict_):
    '''
    Retrieves all values in nested dictionary or list
    '''
    logging.info("getValuesRecursively called")  # forensics logging
    if isinstance(dict_, dict):
        for val_ in dict_.values():
            yield from getValuesRecursively(val_)
    elif isinstance(dict_, list):
        for v_ in dict_:
            yield from getValuesRecursively(v_)
    else:
        logging.info(f"Value yielded: {dict_}")  # forensics logging
        yield dict_


def getValsFromKey(dict_, target, list_holder):
    '''
    Gets all values for keys that match the target key in nested structures
    '''
    logging.info(f"getValsFromKey called with target={target}")  # forensics logging
    if isinstance(dict_, dict):
        for key, value in dict_.items():
            if key == target and value != {}:
                logging.info(f"Value matched for key '{key}': {value}")  # forensics logging
                list_holder.append(value)
            if isinstance(value, (dict, list)):
                getValsFromKey(value, target, list_holder)
    elif isinstance(dict_, list):
        for item in dict_:
            getValsFromKey(item, target, list_holder)


def checkIfValidHelm(path_script):
    '''
    Checks if path_script matches known Helm patterns
    '''
    logging.info(f"checkIfValidHelm called with path: {path_script}")  # forensics logging
    val_ret = False
    path_script = path_script.lower()
    if (
        "values.yaml" in path_script
        or "helmfile.yaml" in path_script
        or (constants.HELM_KW in path_script)
        or (constants.CHART_KW in path_script)
        or (constants.SERVICE_KW in path_script)
        or (constants.INGRESS_KW in path_script)
        or (constants.HELM_DEPLOY_KW in path_script)
        or (constants.CONFIG_KW in path_script)
    ) and ("yaml" in path_script or "yml" in path_script):
        val_ret = True
        logging.info("Helm-related file detected.")  # forensics logging
    else:
        logging.info("File not identified as Helm-related.")  # forensics logging
    return val_ret


def readYAMLAsStr(path_script):
    yaml_as_str = constants.YAML_SKIPPING_TEXT
    with open(path_script, constants.FILE_READ_FLAG) as file_:
        yaml_as_str = file_.read()
    return yaml_as_str


def checkParseError(path_script):
    flag = True
    with open(path_script, constants.FILE_READ_FLAG) as yml:
        yaml = ruamel.yaml.YAML()
        try:
            for dictionary in yaml.load_all(yml):
                pass
        except ruamel.yaml.parser.ParserError:
            flag = False
            print(constants.YAML_SKIPPING_TEXT)
        except ruamel.yaml.error.YAMLError:
            flag = False
            print(constants.YAML_SKIPPING_TEXT)
        except UnicodeDecodeError:
            flag = False
            print(constants.YAML_SKIPPING_TEXT)
    return flag


def loadMultiYAML(script_):
    dicts2ret = []
    with open(script_, constants.FILE_READ_FLAG) as yml_content:
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False
        try:
            for d_ in yaml.load_all(yml_content):
                dicts2ret.append(d_)
        except (ruamel.yaml.parser.ParserError, ruamel.yaml.error.YAMLError, UnicodeDecodeError):
            print(constants.YAML_SKIPPING_TEXT)
        find_json_path_keys(dicts2ret)
        if checkParseError(script_):
            update_json_paths(find_json_path_keys(dicts2ret))
    return dicts2ret


def count_initial_comment_line(filepath):
    initial_comment_line = 0
    comment_found = False
    with open(filepath, constants.FILE_READ_FLAG) as yamlfile:
        textfile = yamlfile.read()
        for line in textfile.split('\n'):
            if line.startswith('#'):
                comment_found = True
                initial_comment_line += 1
            elif not line:
                if not comment_found:
                    initial_comment_line += 1
            elif line.startswith('---'):
                if not comment_found:
                    initial_comment_line += 1
            else:
                break
    return 0 if not comment_found else initial_comment_line


def find_json_path_keys(json_file, parent_path='', paths=None):
    regex_key_dot = re.compile("([^\s\.]+[.][\S]+)")
    regex_special_character_removal = re.compile("[^A-Za-z0-9]+")
    regex_remove_initial_index = re.compile("^/?(\[)([0-9])+(\])")
    if paths is None:
        paths = []
    if isinstance(json_file, dict):
        for key, value in json_file.items():
            if (isinstance(key, ruamel.yaml.comments.CommentedKeyMap) and value is None) or isinstance(key, int):
                continue
            if regex_key_dot.match(key):
                str_key = regex_special_character_removal.sub("*", key)
                path = regex_remove_initial_index.sub('', f"{parent_path}.{str_key}")
                key_jsonpath_mapping.setdefault(key, []).append(path)
                paths.append(path)
                find_json_path_keys(value, parent_path=path, paths=paths)
            else:
                path = regex_remove_initial_index.sub('', f"{parent_path}.{key}")
                key_jsonpath_mapping.setdefault(key, []).append(path)
                paths.append(path)
                find_json_path_keys(value, parent_path=path, paths=paths)
    elif isinstance(json_file, list):
        for index, value in enumerate(json_file):
            path = regex_remove_initial_index.sub('', f"{parent_path}[{index}]")
            paths.append(path)
            find_json_path_keys(value, parent_path=path, paths=paths)
    return paths


def update_json_paths(paths):
    regex_remove_initial_index = re.compile("^/?(\[)([0-9])+(\])")
    updated_paths = []
    for path in paths:
        cleaned = regex_remove_initial_index.sub('', path)
        if cleaned not in updated_paths:
            updated_paths.append(cleaned)
    return updated_paths


def getSingleDict4MultiDocs(lis_dic):
    dict2ret = {}
    key_lis = []
    counter = 0
    for dic in lis_dic:
        if isinstance(dic, list):
            dic = dic[0]
        if dic and isinstance(dic, dict):
            for k_ in dic:
                if k_ in key_lis:
                    dict2ret[f"{k_}.{constants.YAML_DOC_KW}{counter}"] = dic[k_]
                else:
                    key_lis.append(k_)
                    dict2ret[k_] = dic[k_]
            counter += 1
    return dict2ret


if __name__ == '__main__':
    yaml_path = pl.Path(base_path, 'test.yaml')
    dic_lis = loadMultiYAML(yaml_path)
