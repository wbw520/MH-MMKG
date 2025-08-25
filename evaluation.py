from things.model_options import model_selection
from things.data_loading import data_reform, data_organize
from things.templates import evaluation_temp
import os, json
from configs import parser


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
    model = model_selection(model_name, api_key)
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
        if current_count[item]["answer correctness"] == "Yes":
            yes_count += 1
        route_count += current_count[item]["route similarity"][0]
        route_count_re += current_count[item]["route similarity"][1]
        route_count_pre += current_count[item]["route similarity"][2]

    acc = yes_count / len(index_)
    print("acc:", acc)
    print("route count re:", route_count_re / len(index_))
    print("route count pre:", route_count_pre / len(index_))


if __name__ == "__main__":
    args = parser.parse_args()
    root = args.dataset_dir
    model_name = args.model_name
    api_key = args.api_key
    use_name = args.use_name
    use_extra = args.use_extra
    mode = args.mode
    if args.mode == "all":
        modes = ["Direct Vision-needed", "Direct", "Perfect", "self Search", "Offline", "Online Vision-needed"]
    else:
        modes = [mode]

    for mode in modes:
        print("mode:", mode)
        current_name = f"{model_name}_{mode}"

        json_file = os.path.join(root, "results", f"{model_name}_{mode}.json")
        with open(json_file, "r", encoding="utf-8") as f:
            predict_results = json.load(f)

        json_file_evaluation = os.path.join(root, f"evaluation.json")
        main()
        count_score()