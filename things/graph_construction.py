import pandas as pd
import os


def read_nodes(root, monster, offline_file, mode):
    filename = os.path.join(root, monster, "Node.xlsx")
    df = pd.read_excel(filename)
    dict_ = {}
    for index, row in df.iterrows():
        temp_ = []
        for index2, column_name in enumerate(df.columns):  # 遍历列名
            if index2 == 0:
                if row[column_name] == monster or "Element" in row[column_name] or "Pierce Pod" in row[column_name]:
                    temp_.append(row[column_name])
                else:
                    temp_.append(monster + " " + row[column_name])
            else:
                temp_.append(row[column_name])

        if str(temp_[1]) != "nan":
            root_images_ = os.path.join(root, monster, "Knowledge_Images", temp_[1])

            if os.path.isdir(root_images_):
                root_images = []
                for rootp, dirs, files in os.walk(root_images_):
                    for file in files:
                        file_path = os.path.join(rootp, file)
                        root_images.append(file_path)
            else:
                root_images = [root_images_]
        else:
            root_images = ""

        if str(temp_[2]) != "nan":
            root_videos = os.path.join(root, monster, "Knowledge_Videos", temp_[2])
        else:
            root_videos = ""

        if str(temp_[3]) != "nan":
            content_3 = temp_[3]
        else:
            content_3 = ""

        if str(temp_[4]) != "nan":
            content_4 = temp_[4]
        else:
            content_4 = ""

        if "Online" in mode:
            content_3 = ""

        # offline use pre-extracted caption
        if offline_file != "":
            if temp_[0] in offline_file:
                content_3 = offline_file[temp_[0]].replace("**Response:**", "")

        dict_.update({temp_[0]: {"Images": root_images, "Video": root_videos, "Action Description": content_3, "Additional Information": content_4}})

    elements = ["None Element Weapon", "Fire Element Weapon", "Water Element Weapon", "Thunder Element Weapon", "Ice Element Weapon", "Dragon Element Weapon", "Blast Element Weapon", "Poison Element Weapon",
                "Fire Element", "Water Element", "Thunder Element", "Ice Element", "Dragon Element", "Sleep Element"]

    for element in elements:
        dict_.update({element: {"Images": "", "Video": "", "Action Description": "", "Additional Information": ""}})

    return dict_


def read_relations(root, monster):
    filename = os.path.join(root, monster, "Relations.xlsx")
    df = pd.read_excel(filename)
    dict_ = {}
    for index, row in df.iterrows():
        temp_ = []
        for index2, column_name in enumerate(df.columns):
            if str(row[column_name]) != "nan":
                content = row[column_name]
            else:
                content = ""

            if index2 == 0 or index2 == 4:
                if content == monster or "Element" in content or "Pierce Pod" in row[column_name] or content in monster_name:
                    temp_.append(content)
                else:
                    temp_.append(monster + " " + content)
            else:
                temp_.append(content)

        if temp_[0] in dict_:
            dict_[temp_[0]].update({temp_[4]: {"Relation": temp_[1], "Information": temp_[2], "Condition": temp_ [3]}})
        else:
            dict_.update({temp_[0]: {temp_[4]: {"Relation": temp_[1], "Information": temp_[2], "Condition": temp_ [3]}}})
    return dict_


def construct_graph(root, offline_file, mode):
    root = os.path.join(root, "mmkg")
    # aggregate all nodes and relations into two dicts
    node_aggregation = {}
    relation_aggregation = {}
    monster_names = [entry.name for entry in os.scandir(root) if entry.is_dir()]


    for monster in monster_names:
        temp_node = read_nodes(root, monster, offline_file, mode)
        temp_relation = read_relations(root, monster)
        node_aggregation.update(temp_node)
        relation_aggregation.update(temp_relation)

    return node_aggregation, relation_aggregation


monster_name = ["Anjanath", "Azure Rathalos", "Barroth", "Bazelgeuse", "Brachydios", "Diablos", "Frostfang Barioth",
                            "Glavenus", "Kushala Daora", "Legiana", "Nergigante", "Rathalos", "Rathian", "Teostra", "Tigrex",
                            "Nargacuga", "Zinogre", "Pink Rathian", "Yian Garuga", "Radobaan", "Lunastra", "Stygian Zinogre"]