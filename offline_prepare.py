from things.model_options import model_selection
from things.graph_construction import construct_graph
from things.templates import offline_images_description
from things.data_loading import data_reform, data_organize
import json, os
from things.templates import TP


def kg_offline():
    nodes_aggregation, relation_aggregation = construct_graph(root, "", "")
    all_entities = list(nodes_aggregation.keys())
    file_path = os.path.join(root, "mmkg", "kg_offline_" + modal_name+".json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            json_record = json.load(f)
    else:
        json_record = {}


    for i in range(len(all_entities)):
        entity = all_entities[i]
        print(entity)
        if entity in json_record:
            continue
        image_root = nodes_aggregation[entity]["Images"]
        action_description = nodes_aggregation[entity]["Action Description"]
        if image_root == "" or action_description == "":
            continue
        monster_name = entity.split(" ")[0]
        temp = offline_images_description(image_root, " with " + monster_name, entity)
        final_answer = model(temp, image_root)
        json_record.update({entity: final_answer})

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_record, f, ensure_ascii=False, indent=4)


def question_offline():
    print("!!!!!!!!!!")
    file_path = os.path.join(root, "questions_mh\question_offline_" + modal_name + ".json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            json_record = json.load(f)
    else:
        json_record = {}

    all_data = data_reform(root)

    for i in range(len(all_data)):
        data_point = data_organize(root, all_data[i], "", use_name, use_extra)
        tp = TP(data_point, "", use_name, use_extra)
        file_name = data_point["File"]
        print(file_name)
        if file_name in json_record:
            continue
        if "Pure Text" in file_name:
            continue
        image_root = data_point["Images"]
        image_video = data_point["Video"]

        temp = tp.question_image_understanding()
        final_answer = model(temp, image_root)
        json_record.update({file_name: final_answer})

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_record, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    root = "D:\PycharmProjects\MM-KG"
    modal_name = "claude-3-5-haiku-20241022"
    use_name = True
    use_extra = True
    model = model_selection(modal_name)
    kg_offline()
    question_offline()