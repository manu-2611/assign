from read import Calculation, GetFiles, ReadFIle
from write import WriteFIle
from config import DATA_PATH


class CalculateSqrt():

    def from_json(self,):
        files_obj = GetFiles(DATA_PATH)
        list_of_files = files_obj.get_list_of_all_files()
        calculated_list_obj = []

        for file_name in list_of_files:
            file_name = f"vendor_data/{file_name}"

            read_obj = ReadFIle(file_name)
            json_obj = read_obj.read_json()

            calc = Calculation(json_obj)
            calc_obj = calc.calculate_sqrt()

            calculated_list_obj.append(calc_obj)
            break

        write_obj = WriteFIle()
        write_obj.write_text_file(calculated_list_obj)






obj = CalculateSqrt()
obj.from_json()