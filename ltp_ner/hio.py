#!/usr/bin/env python
# -*- coding:utf-8 -*-
import csv
import pickle
from typing import List, Any, Dict
from ltp_ner.hlog import hlogger
import os

Path = str

__all__ = ['load_csv',
           'save_csv',
           'save_pkl',
           'load_pkl']


def load_pkl(filepath: Path, project: Path = os.getcwd()) -> Any:
    logger = hlogger(project)
    logger.info("Loading %s\n", filepath)

    with open(filepath, 'rb') as f:
        data = pickle.load(f)
        return data


def save_pkl(data: Any, filepath: Path, project: Path = os.getcwd()) -> None:
    logger = hlogger(project)
    logger.info("Saving %s\n", filepath)

    with open(filepath, 'wb') as f:
        pickle.dump(data, f)


def load_csv(filepath: Path, project: Path = os.getcwd()) -> Any:
    logger = hlogger(project)
    logger.info("Loading %s\n", filepath)

    is_tsv = True if '.tsv' in filepath else False
    dialect = 'excel-tab' if is_tsv else 'excel'
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, dialect=dialect)
        return list(reader)


def save_csv(data: List[Dict], filepath: Path, project: Path = os.getcwd(), write_head: bool = True) -> Any:
    logger = hlogger(project)
    logger.info("Saving %s\n", filepath)

    save_in_tsv = True if '.tsv' in filepath else False
    dialect = 'excel-tab' if save_in_tsv else 'excel'
    with open(filepath, 'w', encoding='utf-8', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames, dialect=dialect)
        if write_head:
            writer.writeheader()
        writer.writerows(data)
