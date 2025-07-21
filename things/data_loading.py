import pandas as pd
import os


def data_reform(root):
    # read all data points
    all_data = []
    df = pd.read_excel(os.path.join(root, "questions_mh", "question_list.xlsx"))

    for index, row in df.iterrows():
        temp_ = {}
        for column_name in df.columns:  # 遍历列名
            temp_.update({column_name: row[column_name]})
        all_data.append(temp_)
    return all_data


def data_organize(root, data_point, file_offline, use_name=True, use_extra=True):
    # organize one data point into structure, convert nan or pure text data to ""
    if "Pure Text" not in data_point["File"]:
        data_root = os.path.join(root, "questions_mh", str(data_point["File"]))
        root_ = os.path.join(data_root, data_point["Image"])
        if os.path.isdir(root_):
            images_root = []
            for root, dirs, files in os.walk(root_):
                for file in files:
                    file_path = os.path.join(root, file)
                    images_root.append(file_path)
        else:
            images_root = [root_]

        if str(data_point["Video"]) != "nan":
            video_root = os.path.join(data_root, data_point["Video"])
        else:
            video_root = ""
        perception = data_point["Perception"]
    else:
        images_root = ""
        video_root = ""
        perception = ""

    search_route = data_point["Search Route"]
    question_raw = data_point["Question"]
    monster_name = data_point["Monster Name"]
    extra_info = data_point["Extra Information"]
    answer = data_point["Answer"]
    file = data_point["File"]
    type_ = data_point["Type"]

    all_route = search_route.split(";")
    all_route_ = []
    for route in all_route:
        nodes = route.split(">")
        search_route_ = []
        current_monster = monster_name
        for node in nodes:
            if node == monster_name or node == "" or "Element" in node or "Pierce Pod" in node or node in monster_name_:
                search_route_.append(node)
                if node != monster_name and node in monster_name_:
                    monster_name = node
            else:
                search_route_.append(monster_name + " " + node)
        monster_name = current_monster
        all_route_.append(search_route_)

    question_final = question_organize(file, question_raw, monster_name, extra_info, use_name, use_extra)

    if file_offline != "" and file in file_offline:
        perception = file_offline[file]

    return {"Images": images_root, "Video": video_root, "Question": question_final, "Monster Name": monster_name, "Extra Information": extra_info,
            "Perception": perception, "Search Route": all_route_, "Answer": answer, "File": file, "Type": type_}


def question_organize(file, question_raw, monster_name, extra_info, use_name=True, use_extra=True):
    template_1 = "I am playing 'Monster Hunter: World'{}."
    option_1 = " and fighting with{}"

    # whether gives the name of the monster
    if use_name or "Pure Text" in file:
        temp_ = template_1.format(option_1.format(" " + monster_name))
        question = temp_ + "{}" + question_raw.format(" " + monster_name)
    else:
        question = template_1.format("") + "{}" + question_raw.format(" the monster")

    # whether gives additional information (if there is)
    if use_extra and str(extra_info) != "nan":
        if "{}" in extra_info:
            extra_info = extra_info.format(" " + monster_name)
        question_final = question.format(" " + extra_info + " ")
    else:
        question_final = question.format(" ")

    return question_final

monster_name_ = ["Anjanath", "Azure Rathalos", "Barroth", "Bazelgeuse", "Brachydios", "Diablos", "Frostfang Barioth",
                            "Glavenus", "Kushala Daora", "Legiana", "Nergigante", "Rathalos", "Rathian", "Teostra", "Tigrex",
                            "Nargacuga", "Zinogre", "Pink Rathian", "Yian Garuga", "Radobaan", "Lunastra", "Stygian Zinogre"]