import os
import shutil
from distutils.dir_util import copy_tree

def get_csharp_files(directory):
    csharp_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                csharp_files.append(os.path.join(root, file))
    return csharp_files

def simple_find_out_class_lines(file_path):
    start_bracket = 0
    end_bracket = 0
    file_data = []
    is_had_namespace = False
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        for i, line in enumerate(file, start=1):
            file_data.append(line)
            if '{' in line:
                if start_bracket == 0:
                    start_bracket = i-1
            if '}' in line:
                end_bracket = i-1
            if "namespace " in line:
                is_had_namespace = True
    return start_bracket, end_bracket, file_data, is_had_namespace

# main function
def generate_namespaced_code(root_folder, namespace_prefix):
    directory_name = os.path.basename(root_folder)
    print("dict name: " + directory_name)

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    
    #shutil.rmtree(directory_name, ignore_errors=True)
    #shutil.copytree(root_folder, directory_name)
    copy_tree(root_folder, directory_name)
    directory = directory_name
    all_csharp_files = get_csharp_files(directory)
    print("count file cs:", len(all_csharp_files))

    namespace_added = []
    for csFile in all_csharp_files:
        print("Add namespace for file:", csFile)
        start_bracket, end_bracket, file_data, is_had_namespace = simple_find_out_class_lines(csFile)
        if is_had_namespace:
            print("File alread had namespace")
            continue
        # print(start_bracket,end_bracket)
        # print(file_data[start_bracket])
        # print(file_data[end_bracket])
        # for i in range(1, start_bracket):
        #     index = start_bracket - i
        #     line = file_data[index]
        #     if "using" in line:
        #         print("first using line:",line)
        #         print(file_data[index+1])
        #         parent_directory = os.path.basename(os.path.dirname(csFile))
        #         namespace = f"{namespace_prefix}.{parent_directory}"
        #         if (namespace not in namespace_added and "Editor" not in namespace):
        #             namespace_added.append(namespace)
        #         file_data.insert(index+1,  "namespace " + namespace +"{\n")
        #         file_data.append("}")
        #         break

        parent_directory = os.path.basename(os.path.dirname(csFile))
        namespace = f"{namespace_prefix}.{parent_directory}"
        if (namespace not in namespace_added and "Editor" not in namespace):
            namespace_added.append(namespace)
        file_data.insert(0,  "namespace " + namespace +"{\n")
        file_data.append("}")

        with open(csFile, "w", encoding='utf-8', errors='replace') as file:
            for item in file_data:
                file.write(item)

    for csFile in all_csharp_files:
        file_data = []
        with open(csFile, 'r', encoding='utf-8', errors='replace') as file:
            for i, line in enumerate(file, start=1):
                file_data.append(line)
        for namespace in namespace_added:
            file_data.insert(0, "using "+namespace+";\n")
        with open(csFile, "w", encoding='utf-8', errors='replace') as file:
            for item in file_data:
                file.write(item)
            

folder = r"E:\\Lab\\Unity\\MazeCustom\\MazeGameCustom\Assets\Animals Match Pack Customed"
namespace_prefix = "AMP_Game.org"
generate_namespaced_code(folder, namespace_prefix)