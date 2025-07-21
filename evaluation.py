from things.model_options import model_selection
from things.data_loading import data_reform, data_organize
from things.templates import evaluation_temp
import os, json
import numpy as np


def route_similarity_compute(route1, route2):
    if len(route2) == 0:
        return [0, 0, 0]
    else:
        count = 0
        for item1 in route1:
            for item2 in route2:
                if item1 == item2:
                    count += 1
                    break
        return [count/(len(route1)+len(route2)-count), count/len(route1), count/len(route2)]

def main():
    model = model_selection("gpt-4o-2024-11-20")
    all_data = data_reform(root)
    if os.path.exists(json_file_evaluation):
        with open(json_file_evaluation, "r", encoding="utf-8") as f:
            json_record = json.load(f)
    else:
        json_record = {}

    if current_name not in json_record:
        json_record.update({current_name: {}})

    current_save = json_record[current_name]
    for i in range(len(all_data)):
        data_point = data_organize(root, all_data[i], "", use_name, use_extra)
        file = data_point["File"]
        # print(file)
        question = data_point["Question"]
        if file in current_save:
            continue

        answer_true = data_point["Answer"]
        route_to_knowledge_true = data_point["Search Route"]
        if file not in predict_results:
            continue

        if mode == "Direct Vision-needed" or mode == "Direct" or mode == "Perfect":
            route_to_knowledge_predict = [""]
            answer_predict = predict_results[file]
        else:
            route_to_knowledge_predict = predict_results[file]["Route"]
            answer_predict = predict_results[file]["Answer"]


        route_similarity = route_similarity_compute(route_to_knowledge_true, route_to_knowledge_predict)
        # json_record[current_name][file]["route similarity"] = route_similarity

        temp = evaluation_temp(question, answer_true, answer_predict)
        answer = model(temp, [])
        current_save.update({file: {"answer correctness": answer, "route similarity": route_similarity}})

        with open(json_file_evaluation, "w", encoding="utf-8") as f:
            json.dump(json_record, f, ensure_ascii=False, indent=4)


def count_score():
    with open(json_file_evaluation, "r", encoding="utf-8") as f:
        json_record = json.load(f)
    current_count = json_record[current_name]
    index_ = list(current_count.keys())
    yes_count = 0
    route_count= 0
    route_count_re = 0
    route_count_pre = 0
    for item in index_:
        # rand_int = np.random.randint(1, 17)
        # if rand_int == 5:
        #     continue
        if current_count[item]["answer correctness"] == "Yes":
            yes_count += 1
        route_count += current_count[item]["route similarity"][0]
        route_count_re += current_count[item]["route similarity"][1]
        route_count_pre += current_count[item]["route similarity"][2]

    acc = yes_count / len(index_)
    print("acc:", acc)
    # print("route count:", route_count / len(index_))
    print("route count re:", route_count_re / len(index_))
    print("route count pre:", route_count_pre / len(index_))

if __name__ == "__main__":
    # mode = "Direct Vision-needed"
    # mode = "Direct"
    # mode = "Perfect"
    # mode = "Self Search"
    # mode = "Offline"
    # mode = "Online Vision-needed"

    # mode = "Online Vision-needed Name False"

    modes = ["Direct Vision-needed", "Direct", "Perfect", "Self Search", "Offline", "Online Vision-needed"]
    model_name = "claude-3-5-haiku-20241022"

    for mode in modes:
        print("mode:", mode)
        use_name = True
        use_extra = True

        root = "D:\PycharmProjects\MM-KG"
        current_name = f"{model_name}_{mode}"

        json_file = os.path.join(root, "results", f"{model_name}_{mode}.json")
        with open(json_file, "r", encoding="utf-8") as f:
            predict_results = json.load(f)

        json_file_evaluation = os.path.join(root, f"evaluation.json")
        main()
        count_score()