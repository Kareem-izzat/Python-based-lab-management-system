# hamza al shaer 1211162
# kareem al qoutb   1211756

class Patient:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient_id):
        if patient_id in self.patients:
            print(f"Patient with ID {patient_id} already exists.")
        else:
            self.patients[patient_id] = {}
            print(f"Patient with ID {patient_id} added successfully.")

    def get_patient(self, patient_id):
        return self.patients.get(patient_id, "Patient not found.")

class TestRecords:
    def __init__(self, file_name="midecalRecord.txt"):
        self.records = {}
        self.file_name = file_name
        self.load_records_from_file()

    def load_records_from_file(self):
        try:
            with open(self.file_name, "r") as file:
                for line in file:
                    match = re.match(
                        r'(\d{7}): (\w+), (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}), ([\d.]+), ([\w/]+), (\w+)(?:, (\d{4}-\d{2}-\d{2}))?(?:, (\d{2}:\d{2}))?',
                        line
                    )
                    if match:
                        patient_id = match.group(1)
                        record = {
                            "Test Name": match.group(2),
                            "Start_Date": match.group(3),
                            "Start_Time": match.group(4),
                            "Result": match.group(5),
                            "Unit": match.group(6),
                            "Status": match.group(7)
                        }
                        if match.group(8):
                            record["End_Date"] = match.group(8)
                        if match.group(9):
                            record["End_Time"] = match.group(9)

                        if patient_id in self.records:
                            self.records[patient_id].append(record)
                        else:
                            self.records[patient_id] = [record]
        except FileNotFoundError:
            print("Error: The file does not exist.")

    def add_record(self, patient_id, test_name, date, time, result, unit, status, end_date=None, end_time=None):
        record = {
            "Test Name": test_name,
            "Start_Date": date,
            "Start_Time": time,
            "Result": result,
            "Unit": unit,
            "Status": status,
            "End_Date": end_date if status == "completed" else "",
            "End_Time": end_time if status == "completed" else ""
        }

        if patient_id in self.records:
            self.records[patient_id].append(record)
        else:
            self.records[patient_id] = [record]

    def print_all_records(self):
        for patient_id, records in self.records.items():
            print(f"Patient ID: {patient_id}")
            for record in records:
                print(f"  Test Name: {record.get('Test Name', 'N/A')}")
                print(f"  Start Date: {record.get('Start_Date', 'N/A')}")
                print(f"  Start Time: {record.get('Start_Time', 'N/A')}")
                print(f"  Result: {record.get('Result', 'N/A')}")
                print(f"  Unit: {record.get('Unit', 'N/A')}")
                print(f"  Status: {record.get('Status', 'N/A')}")
                if record.get('Status', 'N/A') == "completed":
                    print(f"  End Date: {record.get('End_Date', 'N/A')}")
                    print(f"  End Time: {record.get('End_Time', 'N/A')}")
                print()

    def save_update_records_to_file(self):
        with open(self.file_name, "w") as file:
            for patient_id, records in self.records.items():
                for record in records:
                    record_line = (f"{patient_id}: {record['Test Name']}, {record['Start_Date']} {record['Start_Time']}, "
                                   f"{record['Result']}, {record['Unit']}, {record['Status']}")
                    if record.get("End_Date") and record.get("End_Time"):
                        record_line += f", {record['End_Date']}, {record['End_Time']}"
                    file.write(record_line + "\n")

    def update_record_test(self):
        while True:
            patient_id = input("Enter the Patient ID to update records: ")

            # Check if the Patient ID is exactly 7 digits and numeric
            if len(patient_id) != 7 or not patient_id.isdigit():
                print("Error: Patient ID must be exactly 7 digits.")
                continue

            if patient_id not in self.records:
                print("Error: No records found for this Patient ID.")
                continue

            break

        # Display all records for the patient
        records = self.records[patient_id]
        for idx, record in enumerate(records, 1):
            print(
                f"{idx}. Test Name: {record['Test Name']}, Date: {record['Start_Date']}, Time: {record['Start_Time']}, "
                f"Result: {record['Result']}, Unit: {record['Unit']}, Status: {record['Status']}")
            if "End_Date" in record and "End_Time" in record:
                print(f"   End Date: {record['End_Date']}, End Time: {record['End_Time']}")

        while True:
            try:
                record_num = int(input("Enter the number of the record you want to update: ")) - 1
                if record_num < 0 or record_num >= len(records):
                    raise ValueError("Invalid record number.")
                break  # Exit loop if the input is valid
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid record number.")

        record_to_update = records[record_num]

        while True:
            print("Which part would you like to update?")
            print("1. Test Name")
            print("2. Start Date")
            print("3. Start Time")
            print("4. Result")
            print("5. Unit")
            print("6. Status")
            if "End_Date" in record_to_update:
                print("7. End Date")
                print("8. End Time")
            print("9. Exit and save changes")

            try:
                field_num = int(input("Enter the number of the field you want to update: "))

                field_map = {
                    1: "Test Name",
                    2: "Start_Date",
                    3: "Start_Time",
                    4: "Result",
                    5: "Unit",
                    6: "Status",
                    7: "End_Date",
                    8: "End_Time"
                }

                if field_num not in field_map and field_num != 9:
                    print("Error: Invalid field number.")
                    continue

                if field_num == 9:
                    break

                field_name = field_map[field_num]
                new_value = input(f"Enter the new value for {field_name}: ")

                # Validate inputs based on field type
                if field_name == "Test Name":
                    while not re.match(r'^[A-Z]{3}$', new_value):
                        print("Error: Test Name must be exactly 3 uppercase letters.")
                        new_value = input(f"Enter the new value for {field_name}: ")

                    # Check if the new Test Name exists in medicalTest.txt
                    valid_test_name = False
                    while not valid_test_name:
                        with open("medicalTest.txt", "r") as file:
                            found = False
                            for line in file:
                                match = re.search(r'\b([A-Z]{3})\b', line)
                                if match and match.group(1) == new_value:
                                    found = True
                                    break
                            if found:
                                valid_test_name = True
                            else:
                                print("Error: This Test Name is not found in the system. Please enter again.")
                                new_value = input(f"Enter the new value for {field_name}: ")

                elif field_name == "Start_Date" or field_name == "End_Date":
                    if not re.match(r'^\d{4}-\d{2}-\d{2}$', new_value):
                        print("Error: Date must be in the format YYYY-MM-DD.")
                        continue

                elif field_name == "Start_Time" or field_name == "End_Time":
                    if not re.match(r'^\d{2}:\d{2}$', new_value):
                        print("Error: Time must be in the format HH:MM.")
                        continue

                elif field_name == "Result":
                    if not re.match(r'^[\d.]+$', new_value):
                        print("Error: Result must be a number.")
                        continue

                elif field_name == "Unit":
                    # Add specific unit validation if needed
                    pass

                # Update the record in the dictionary
                record_to_update[field_name] = new_value

                # Handle status change
                if field_name == "Status":
                    if new_value == "completed":
                        while True:
                            end_date = input("Enter the End Date (YYYY-MM-DD): ")
                            if not re.match(r'^\d{4}-\d{2}-\d{2}$', end_date):
                                print("Error: End Date must be in the format YYYY-MM-DD.")
                                continue
                            end_time = input("Enter the End Time (HH:MM): ")
                            if not re.match(r'^\d{2}:\d{2}$', end_time):
                                print("Error: End Time must be in the format HH:MM.")
                                continue
                            record_to_update["End_Date"] = end_date
                            record_to_update["End_Time"] = end_time
                            break
                    else:
                        record_to_update.pop("End_Date", None)
                        record_to_update.pop("End_Time", None)

                # Save changes to the file
                self.save_update_records_to_file()

                print(f"{field_name} updated successfully.")

            except ValueError:
                print("Error: Please enter a valid number.")

        print("All updates have been saved.")


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Validition of add new test
import re
from datetime import datetime
def get_valid_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print(error_message)
def get_valid_input2(prompt, validation_func,name, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input,name):
            return user_input
        print(error_message)
def Valid_ID_Record(id_str):
    return re.fullmatch(r'\d{7}', id_str) is not None

def Valid_Test_Name(name):
    # not empty and not digit
    return bool(name) and not any(char.isdigit() for char in name)
def Valid_Test_Name_Record (name):
    if len(name) != 3 or not name.isalpha() or not name.isupper():
        return False

    # check if the test name record found in midicalTest file as test
    with open("medicalTest.txt", "r") as file:
        for line in file:
            # Extract the symbolic name from the line
            match = re.search(r'\b([A-Z]{3})\b', line)
            if match and match.group(1) == name:
                return True

    print("This not Found in System")
    return False

def Valid_Symbolic_Name(symbolic_name):
    # not empty must 3 char and capital later
    return bool(symbolic_name) and len(symbolic_name) == 3 and symbolic_name.isupper()

def Valid_range(range_values):
    form_rang = r'^[><]\s*\d+(\.\d+)?(\s*,\s*[><]\s*\d+(\.\d+)?)?$'
    return bool(range_values) and re.match(form_rang, range_values)

def Valid_Unit(unit):
    return bool(unit) and not any(char.isdigit() for char in unit) and re.match(r'^[\w\s/]+$', unit)


def Valid_Unit2(unit, test_name):
    if not Valid_Unit(unit):
        print("Error: Invalid unit format.")
        return False

    unit = unit.strip()  # Strip any extra spaces from the unit

    with open("medicalTest.txt", "r") as file:
        for line in file:
            # Extract the full test name and units from the line
            match = re.search(r'(.*?);.*Unit:\s*([\w\s/,-]+)', line)
            if match:
                file_test_name = match.group(1).strip()
                file_units = match.group(2).strip().split(',')

                # Clean up the units
                file_units = [u.strip() for u in file_units]
                symbolic_test_name_match = re.search(r'\b([A-Z]{3})\b', file_test_name)

                if symbolic_test_name_match:
                    file_symbolic_name = symbolic_test_name_match.group(1)

                    # Check if the symbolic test name matches
                    if file_symbolic_name == test_name:
                        # Check if the provided unit matches any of the units in the file
                        if unit in file_units:
                            print("Unit matches.")
                            return True
                        else:
                            print("Error: The unit you entered does not match the unit for the test name you entered.")
                            return False

    print("Error: Test name not found in the medicalTest.txt file.")
    return False
def Valid_Turnaround_Time(turnaround_time):
    return bool(turnaround_time) and re.match(r'^\d{2}-\d{2}-\d{2}$', turnaround_time)

def Valid_Date(date):
    # Check if the date_str matches the YYYY-MM-DD format
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    return False

def Valid_Time(time):
    if re.fullmatch(r'\d{2}:\d{2}', time):
        try:
            datetime.strptime(time, '%H:%M')
            return True
        except ValueError:
            return False

def Valid_Status(status):
    return status in {"completed", "pending", "reviewed"}

def Valid_Result(result_str):
    # take integer of floating point and d --> must dicimal not char
    return re.fullmatch(r'^\d+(\.\d+)?$', result_str) is not None


#-------------function for opration "1"-------------------
def Add_New_Medical_test():
    test_name = get_valid_input("Enter the name of the new medical test: ",Valid_Test_Name,"Invalid input. Test name should not be empty or contain numbers.")
    symbolic_TestName = get_valid_input("Enter the symbolic name of the new medical test (3 Capital Letters): ",Valid_Symbolic_Name,"Invalid input. Symbolic name should be exactly 3 Caplital letters.")
    range_values = get_valid_input("Enter the range of the test (e.g., > 70, < 99): ",Valid_range,"Invalid input. Range should follow the format: > 70, < 99.")
    unit = get_valid_input("Enter the unit of measurement (e.g., mg/dL): ",Valid_Unit,"Invalid input. Unit should be non-empty and can contain letters and/or slashes.")
    turnaround_time = get_valid_input("Enter the turnaround time (e.g., 00-12-06): ",Valid_Turnaround_Time,"Invalid input. Turnaround time should follow the format: 00-12-06.")



    new_test_entry = f"{test_name} ({symbolic_TestName}); Range: {range_values}; Unit: {unit}, {turnaround_time}\n"

    # Append the new test entry to the file
    with open("medicalTest.txt", "a") as file:
        file.write(new_test_entry)

    print("Medical test added successfully.")

#-------------function for opration "2"-------------------
def Add_New_Medical_Record ():
    ID_Record = get_valid_input("Enter the 7-digit medical record ID: ",Valid_ID_Record,"Error: ID must be a 7-digit number. Please try again.")
    Test_name=get_valid_input("Enter the 3-character test name: ",Valid_Test_Name_Record,"Error: Test name must be exactly 3 letters. Please try again.")
    Start_Date = get_valid_input("Enter the date (YYYY-MM-DD): ",Valid_Date,"Error: Date must be in the format YYYY-MM-DD. Please try again.")
    Start_time = get_valid_input("Enter the time (HH:MM): ",Valid_Time,"Error: Time must be in the format HH:MM. Please try again.")
    result =get_valid_input("Enter the result value: ",Valid_Result,"Error: Result must be a valid number (integer or floating-point). Please try again.")
    unit = get_valid_input2("Enter the unit of measurement: ",Valid_Unit2,Test_name,"Error: Invalid unit. Please try again.")
    status = get_valid_input("Enter the status (completed, pending, reviewed): ",Valid_Status,"Error: Status must be 'completed', 'pending', or 'reviewed'. Please try again.")
    if status == "completed":
        End_Date = get_valid_input("Enter the end date (YYYY-MM-DD): ",Valid_Date,"Error: End date must be in the format YYYY-MM-DD. Please try again.")
        End_Time = get_valid_input("Enter the end time (HH:MM): ",Valid_Time,"Error: End time must be in the format HH:MM. Please try again.")
        end_datetime = f"{End_Date} {End_Time}"
    else:
        End_Date=""
        End_Time=""
        end_datetime = ""


    new_record_entry = f"{ID_Record}: {Test_name}, {Start_Date} {Start_time}, {result}, {unit}, {status}"
    # if complated add the end data and end time
    if status == "completed":
        new_record_entry += f", {end_datetime}"
    new_record_entry += "\n"

    # Append the new Record entry to the file
    with open("midecalRecord.txt", "a") as file:
        file.write(new_record_entry)

    record.add_record(ID_Record,Test_name,Start_Date,Start_time,result,unit,status,End_Date,End_Time)

    print("Medical record added successfully.")


#-------------function for opration "3"-------------------
def update_medicalTest():
    try:
        # Display the contents of the file with line numbers
        with open("medicalTest.txt", "r") as file:
            lines = file.readlines()
            for idx, line in enumerate(lines, 1):
                print(f"{idx}. {line.strip()}")

        # to get any midical test he want update
        while True:
            try:
                index = int(input("Enter the index of the medical test you want to update: "))
                if 1 <= index <= len(lines):
                    break
                else:
                    print(f"Error: Index must be between 1 and {len(lines)}.")
            except ValueError:
                print("Error: Please enter a valid number.")

        # sShow the midical test i want update
        selected_test = lines[index - 1].strip()
        print(f"Selected Test: {selected_test}")

        print("What would you like to update?")
        print("1. Name")
        print("2. Symbolic Name")
        print("3. Range")
        print("4. Unit")
        print("5. Time")

        while True:
            try:
                choice = int(input("Enter the number corresponding to the field you want to update: "))
                if 1 <= choice <= 5:
                    break
                else:
                    print("Error: Please choose a number between 1 and 5.")
            except ValueError:
                print("Error: Please enter a valid number.")

        # split the test we chose by ; and each part in index (name and Symbolic) (range) (unit and time)
        parts = re.split(r';\s*', selected_test)
        if choice == 1:
            while True:
                new_value = input("Enter the new Name: ")
                if any(char.isdigit() for char in new_value):
                    print("Error: Name cannot contain digits. Please enter a valid name.")
                    continue
                else:
                    # Find the index of the symbolic name (starts with '(')
                    symbolic_start = parts[0].find('(')
                    if symbolic_start != -1:
                        # Update only the name portion, keeping the symbolic part intact
                        parts[0] = new_value + " " + parts[0][symbolic_start:]
                        break

        elif choice == 2:
            while True:
                new_value = input("Enter the new Symbolic Name (3 capital letters): ")
                if re.match(r'^[A-Z]{3}$', new_value):
                    parts[0] = re.sub(r'\(\w+\)', f"({new_value})", parts[0])
                    break
                else:
                    print("Error: Symbolic Name must be exactly 3 capital letters.")

        elif choice == 3:
            while True:
                new_value = input("Enter the new Range (e.g., '> 90', '<90', '>80,<70'): ")
                if re.match(r'^[<>]\s*\d+(\.\d+)?(,\s*[<>]\s*\d+(\.\d+)?)?$', new_value):
                    parts[1] = f"Range: {new_value}"
                    break
                else:
                    print("Error: Invalid range format.")

        elif choice == 4:
            while True:
                new_value = input("Enter the new Unit: ")
                if re.search(r'\d', new_value):
                    print("Error: Unit cannot contain digits.")
                else:
                    # take only unit not with time : split part [2] to first comma the unit index -1
                    parts[2] = f"Unit: {new_value}, {parts[2].split(', ', 1)[-1]}"
                    break

        elif choice == 5:
            while True:
                new_value = input("Enter the new Time (HH-MM-SS): ")
                if re.match(r'^\d{2}-\d{2}-\d{2}$', new_value):
                    # take only time the time index 0
                    parts[2] = f"{parts[2].split(', ', 1)[0]}, {new_value}"
                    break
                else:
                    print("Error: Time must be in the format HH-MM-SS.")
        # [index -1] to reach the coorect index in file Then all part after change join with put ; between it then write to file
        lines[index - 1] = '; '.join(parts) + '\n'
        with open("medicalTest.txt", "w") as file:
            file.writelines(lines)

        print("Medical test updated successfully.")

    except FileNotFoundError:
        print("Error: medicalTest.txt file not found.")

# main
while True :
    record = TestRecords()
    print("select the service you want make (1-9) :")
    print("1.Add new medical test")
    print("2.Add a new medical test record")
    print("3.Update patient records including all fields")
    print("4.Update medical tests in the medicalTest file")
    print("5.Filter medical tests")
    print("6.Generate textual summary reports")
    print("7.Export medical records to a comma separated file")
    print("8.Import medical records from a comma separated file")
    print("9.exit")
    choice = input()

    if choice == '1':
        Add_New_Medical_test()
    elif choice == '2':
        Add_New_Medical_Record()
    elif choice == '3':
        record.update_record_test()
    elif choice == '4':
        update_medicalTest()


