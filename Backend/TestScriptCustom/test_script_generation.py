import pandas as pd
import json
import xml.etree.ElementTree as ET
import xlwt


def print_first_row_with_headers(file_path):
    try:
        # Load the Excel file
        data = pd.read_excel(file_path)
        
        # Check if the file is not empty
        if not data.empty:
            # Get the first row with column headers
            data = pd.read_excel(file_path, sheet_name='TestData')
            first_row = data.iloc[0].to_dict()
            return first_row
        else:
            print("The file is empty.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

        

def convert_xml_to_json(xml_file_path, json_file_path):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # Convert XML to a dictionary
            def xml_to_dict(element):
                return {
                    element.tag: {
                        "attributes": element.attrib,
                        "text": element.text.strip() if element.text else None,
                        "children": [xml_to_dict(child) for child in element]
                    }
                }

            xml_dict = xml_to_dict(root)

            # Write the dictionary to a JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(xml_dict, json_file, indent=4)

            print(f"XML converted to JSON and saved to {json_file_path}")
        except FileNotFoundError:
            print(f"File not found: {xml_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

def generate_json_array_from_test_data(test_data):

    
    launch = [
            {
            "RowID": 1,
            "TestCaseID": "test_data_script_1",
            "Skip": "",
            "Debug": "",
            "Worksheet": "Master",
            "StepDescription": "Launch the URL",
            "Action": "LaunchBrowser",
            "Param1:": "<COL>URL</COL>",
            "Param2:": "SkipURLValidation",
            "Param3:": "",
            "Param4:": "",
            "Param5:": "",
            "Param6:": "",
            "Param7:": "",
            "Param8:": "",
            "ActionOnFail:": "",
            "FParam1:": "",
            "FParam2:": "",
            "ExpectedResult:": "",
            "Severity:": "",
            "Row:": ""
        }]
    
    close = [
            {
            "RowID": 1,
            "TestCaseID": "test_data_script_1",
            "Skip": "",
            "Debug": "",
            "Worksheet": "",
            "StepDescription": "Close Browser Instance",
            "Action": "CloseBrowser",
            "Param1:": "",
            "Param2:": "",
            "Param3:": "",
            "Param4:": "",
            "Param5:": "",
            "Param6:": "",
            "Param7:": "",
            "Param8:": "",
            "ActionOnFail:": "",
            "FParam1:": "",
            "FParam2:": "",
            "ExpectedResult:": "",
            "Severity:": "",
            "Row:": ""
        }]
    

    try:
        json_array = [
            {
            "RowID": 0,
            "TestCaseID": "",
            "Skip": "",
            "Debug": "",
            "Worksheet": "",
            "StepDescription": "Initial temp variable and set value = 1",
            "Action": "ChangeEnvVariableValue",
            "Param1:": "Counter",
            "Param2:": "1",
            "Param3:": "",
            "Param4:": "",
            "Param5:": "",
            "Param6:": "",
            "Param7:": "",
            "Param8:": "",
            "ActionOnFail:": "",
            "FParam1:": "",
            "FParam2:": "",
            "ExpectedResult:": "",
            "Severity:": "",
            "Row:": ""
        },
            {
            "RowID": 0,
            "TestCaseID": "",
            "Skip": "",
            "Debug": "",
            "Worksheet": "",
            "StepDescription": "Initialize Loop in the script",
            "Action": "Loop",
            "Param1:": "<Env>Counter</Env>",
            "Param2:": "LESS THAN",
            "Param3:": "5",
            "Param4:": "+1",
            "Param5:": "16",
            "Param6:": "",
            "Param7:": "",
            "Param8:": "",
            "ActionOnFail:": "",
            "FParam1:": "",
            "FParam2:": "",
            "ExpectedResult:": "",
            "Severity:": "",
            "Row:": ""
        },
        ]
        for idx, (key, value) in enumerate(test_data.items(), start=1):
            json_object = {
                "RowID": idx,
                "TestCaseID": f"test_data_script_{idx}",
                "Skip": f"<COL>{key}</COL>",
                "Debug": "",
                "Worksheet": "TestData",
                "StepDescription": f"Enter {key}",
                "Action": "EnterTextValue",
                "Param1:": f"<OBJ>{key}</OBJ>",
                "Param2:": f"<COL>{key}</COL>",
                "Param3:": "",
                "Param4:": "",
                "Param5:": "",
                "Param6:": "",
                "Param7:": "",
                "Param8:": "",
                "ActionOnFail:": "",
                "FParam1:": "",
                "FParam2:": "",
                "ExpectedResult:": "",
                "Severity:": "",
                "Row:": "<ENV>Counter</ENV>",
            }
            json_array.append(json_object)
            # Save the JSON array into an Excel file

            workbook = xlwt.Workbook()

#   -------------------------start -------          
            master_sheet = workbook.add_sheet("Launch")
            for row_idx, launch_item in enumerate(launch, start=1):
                for col_idx, (key, value) in enumerate(launch_item.items()):
                    if row_idx == 1:
                        master_sheet.write(0, col_idx, key)  # Write headers
                    master_sheet.write(row_idx, col_idx, value)  # Write data

#    ------------------------validation--         

            # Ensure "TestScript" sheet is created only once
            if "TestScript" not in [sheet.name for sheet in workbook._Workbook__worksheets]:
                sheet = workbook.add_sheet("TestScript")

            # Write headers
            headers = json_array[0].keys()
            for col, header in enumerate(headers):
                sheet.write(0, col, header)

            # Write data rows
            for row_idx, json_object in enumerate(json_array, start=1):
                for col_idx, (key, value) in enumerate(json_object.items()):
                    sheet.write(row_idx, col_idx, value)

# ----------------------------close-------------------
            close_sheet = workbook.add_sheet("Close")
            for row_idx, close_item in enumerate(close, start=1):
                for col_idx, (key, value) in enumerate(close_item.items()):
                    if row_idx == 1:
                        close_sheet.write(0, col_idx, key)  # Write headers
                    close_sheet.write(row_idx, col_idx, value)  # Write data
            # Save the workbook
            workbook.save('./output/script.xls')
        return json_array
    except Exception as e:
        print(f"An error occurred while generating JSON array: {e}")
        return []



