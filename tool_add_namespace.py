import os
import shutil
from distutils.dir_util import copy_tree
import re

def get_csharp_files(directory):
    csharp_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                csharp_files.append(os.path.join(root, file))
    return csharp_files
def get_namespace_name(line):
    match = re.search(r'namespace\s+(\w+)', line)
    return match.group(1) if match else None
def simple_find_out_class_lines(file_path):
    start_bracket = 0
    end_bracket = 0
    file_data = []
    is_had_namespace = False
    is_preline_using = True
    old_namespace = ""
    line_old_namespace = 0
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        for i, line in enumerate(file, start=1):
            file_data.append(line)
            if 'using' in line and is_preline_using:
                start_bracket = i
            if '}' in line:
                end_bracket = i-1
            if "namespace " in line:
                is_had_namespace = True
                old_namespace = get_namespace_name(line)
                line_old_namespace = i-1
            if line.strip() != '' and "using" not in line:
                is_preline_using = False
    return start_bracket, end_bracket, file_data, is_had_namespace, old_namespace, line_old_namespace

# main function
def generate_namespaced_code(root_folder, namespace_prefix, mode = 'add'):
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
        start_bracket, end_bracket, file_data, is_had_namespace, old_namespace, line_old_namespace = simple_find_out_class_lines(csFile)
        namespace = f"{namespace_prefix}"
        if is_had_namespace:
            print("File alread had namespace")
            if mode == 'edit':
                namespace = f"{namespace_prefix}.{old_namespace}"
            else:
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
        # namespace = f"{namespace_prefix}.{parent_directory}"
        
        if (namespace not in namespace_added and "Editor" not in namespace):
            namespace_added.append(namespace)
        if (mode == 'add'):
            file_data.insert(start_bracket,  "namespace " + namespace +"{\n")
        elif (mode == 'edit') and is_had_namespace:
            file_data[line_old_namespace] = file_data[line_old_namespace].replace(old_namespace, namespace)
        if (not is_had_namespace):
            file_data.append("}")
        

        with open(csFile, "w", encoding='utf-8', errors='replace') as file:
            for item in file_data:
                if mode == "edit" and f"using {old_namespace}" in item:
                    item = item.replace(f"using {old_namespace}", f"using {namespace}")
                    file.write(item)
                else:
                    file.write(item)

    for csFile in all_csharp_files:
        file_data = []
        with open(csFile, 'r', encoding='utf-8', errors='replace') as file:
            for i, line in enumerate(file, start=1):
                file_data.append(line)
        for namespace in namespace_added:
            file_data.insert(2, "using "+namespace+";\n")
        with open(csFile, "w", encoding='utf-8', errors='replace') as file:
            for item in file_data:
                file.write(item)
            

folder = r"D:\\python_tools\\ToolAddNamespaceCSharp\\ScriptsPuzzle\\Scripts"
namespace_prefix = "RainbowGame"
generate_namespaced_code(folder, namespace_prefix, "edit")
