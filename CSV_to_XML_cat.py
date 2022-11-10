# -*- coding: utf-8 -*-
import csv
from yattag import Doc, indent

def convert_csv_to_xml_cat(org):

    doc, tag, text = Doc().tagtext()
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_schema = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"></xs:schema>'

    doc.asis(xml_header)
    doc.asis(xml_schema)

    categoryDefaultOid = '1.2.752.113.18.999.8'
    categoryDefaultCode = 'KAT110'
    categoryDefaultName = 'Äldre journal'

    subcategoryDefaultOid = '1.2.752.113.18.999.3'
    subcategoryDefaultCode = 'KAT110-010'
    subcategorydefaultName = 'Äldre journal'

    documenttypeDefaultOid = '1.2.752.113.18.999.10'
    documenttypeDefaultCode = 'U001'
    documenttypeDefaultName = 'Ktg 1 – Journalöversikt'

    if org == 'su1':
        csv_file_path = r'C:\Users\dnorin\Documents\SU1_Category_mapping3.csv'
    if org == 'su2':
        csv_file_path = r'C:\Users\dnorin\Documents\SU2_Category mapping (2022-10-06).csv'

    emptyRows = []

    with tag('masterValueCatalogs'):

        with tag("masterValueCatalog", name="Kategori", defaultOid=categoryDefaultOid, defaultCode=categoryDefaultCode, defaultName=categoryDefaultName):
            csv_file = open(csv_file_path)
            csv_reader = csv.DictReader(csv_file, delimiter=";")
            for row in csv_reader:
                if row['newDocumenType'] and row['newDocumenType'] != '-':
                    doc.stag("mvcItem", oid=categoryDefaultOid, code=row['newMainCategory'], name=row['newMainCategoryName'], edasField=row['oldValue'])
                else:
                    emptyRows.append(row['oldValue'])

        with tag("masterValueCatalog", name="Underkategori", defaultOid=subcategoryDefaultOid, defaultCode=subcategoryDefaultCode, defaultName=subcategorydefaultName):
            csv_file = open(csv_file_path)
            csv_reader = csv.DictReader(csv_file, delimiter=";")
            for row in csv_reader:
                if row['newDocumenType'] and row['newDocumenType'] != '-':
                    doc.stag("mvcItem", oid=subcategoryDefaultOid, code=row['newSubCategory'], name=row['newSubCategoryName'], edasField=row['oldValue'])
                else:
                    emptyRows.append(row['oldValue'])

        with tag("masterValueCatalog", name='Dokumenttyp', defaultOid=documenttypeDefaultOid, defaultCode=documenttypeDefaultCode, defaultName=documenttypeDefaultName):
            csv_file = open(csv_file_path)
            csv_reader = csv.DictReader(csv_file, delimiter=";")
            for row in csv_reader:
                if row['newDocumenType'] and row['newDocumenType'] != '-':
                    doc.stag("mvcItem", oid=documenttypeDefaultOid, code=row['newDocumenType'], name=(row['newDocumenTypeName']).strip(), edasField=row['oldValue'])
                else:
                    emptyRows.append(row['oldValue'])

    result = indent(
        doc.getvalue(),
        indentation='    ',
        indent_text=True
    )
    print(result)

    if org == 'su1':
        with open("MasterValueCatalog_cat_su1.xml", "w") as f:
            f.write(result)
    if org == 'su2':
        with open("MasterValueCatalog_cat_su2.xml", "w") as f:
            f.write(result)

    emptyRowListSansDuplicates = list(dict.fromkeys(emptyRows))
    print('\nMapping missing:')
    print('(', end='')
    for entry in emptyRowListSansDuplicates:
        print('\'', end='')
        print(entry, end='')
        if entry != emptyRowListSansDuplicates[-1]:
            print('\'', end=', ')
        else:
            print('\'', end='')
    print(')')

if __name__ == '__main__':
    convert_csv_to_xml_cat('su2')