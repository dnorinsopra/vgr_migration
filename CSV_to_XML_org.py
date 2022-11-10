import csv
from yattag import Doc, indent


def convert_csv_to_xml_org(org):

    doc, tag, text = Doc().tagtext()
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_schema = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"></xs:schema>'

    doc.asis(xml_header)
    doc.asis(xml_schema)

    unitDefaultOid = '1.2.752.129.2.1.4.1'
    unitDefaultCode = 'SE2321000131-E000000000757'
    unitDefaultName = 'Akutmottagning Mölndal'

    careUnitDefaultOid = '1.2.752.129.2.1.4.1'
    careUnitDefaultOidefaultCode = 'SE2321000131-E000000000740'
    careUnitDefaultName = 'Verksamhet Medicin och akutsjukvård Mölndal'

    if org == 'su1':
        csv_file_path = r'C:\Users\dnorin\Documents\SU1_organisation (klar).csv'
    if org == 'su2':
        csv_file_path = r'C:\Users\dnorin\Documents\SU2_organisation (2022-10-10).csv'

    emptyRows = []

    with tag('masterValueCatalogs'):

        with tag("masterValueCatalog", name="Enhet", defaultOid=unitDefaultOid, defaultCode=unitDefaultCode, defaultName=unitDefaultName):
            csv_file = open(csv_file_path)
            csv_reader = csv.DictReader(csv_file, delimiter=";")
            for row in csv_reader:
                if row['newEnhet'] and row['newEnhetName']:
                    doc.stag("mvcItem", oid=unitDefaultOid, code=row['newEnhet'], name=row['newEnhetName'], edasField=row['oldValue'])
                else if # båda inte har vårde - INFO - logging saknas mappning
                else: # errorloggning, finns ej fallet att bara en har värde
                    emptyRows.append(row['oldValue'])

        with tag("masterValueCatalog", name="Vårdenhet", defaultOid=careUnitDefaultOid, defaultCode=careUnitDefaultOidefaultCode, defaultName=careUnitDefaultName):
            csv_file = open(csv_file_path)
            csv_reader = csv.DictReader(csv_file, delimiter=";")
            for row in csv_reader:
                if row['newVardenhet'] and row['newVardenhetName']:
                    doc.stag("mvcItem", oid=careUnitDefaultOid, code=row['newVardenhet'], name=row['newVardenhetName'], edasField=row['oldValue'])
                else: # error pga båda måste finnas (gäller bara för vårdenhet)
                    emptyRows.append(row['oldValue'])
                    # logg missing mapping for oldValue... + hela raden

    result = indent(
        doc.getvalue(),
        indentation='    ',
        indent_text=True
    )
    print(result)

    if org == 'su1':
        with open("MasterValueCatalog_org_su1.xml", "w") as f:
            f.write(result)
    if org == 'su2':
        with open("MasterValueCatalog_org_su2.xml", "w") as f:
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
    convert_csv_to_xml_org('su2')

