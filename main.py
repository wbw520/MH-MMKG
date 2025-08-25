from things.data_loading import data_reform, data_organize
from things.templates import TP
from things.model_options import model_selection
import os, json
from things.graph_search import KnowledgeSearch, construct_final_knowledge, construct_final_knowledge_self_search
from things.graph_construction import construct_graph
from configs import parser


def process():
    all_data = data_reform(root)
    nodes_aggregation, relation_aggregation = construct_graph(root, offline_file2, mode)
    model = model_selection(model_name, api_key)
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            json_record = json.load(f)
    else:
        json_record = {}

    for i in range(len(all_data)):
        data_point = data_organize(root, all_data[i], offline_file1, use_name, use_extra)
        file = data_point["File"]
        print(file)

        tp = TP(data_point, mode, use_name, use_extra)
        if "Direct" in mode:
            answer = final_answer(model, tp, knowledge="")
            json_record.update({file: answer})
        elif "Perfect" in mode:
            route_to_knowledge = data_point["Search Route"]
            given_knowledge = construct_final_knowledge(route_to_knowledge, nodes_aggregation, relation_aggregation)
            answer = final_answer(model, tp, given_knowledge)
            json_record.update({file: answer})
        else:
            route_record = KnowledgeSearch(tp, model, nodes_aggregation.copy(), relation_aggregation.copy(), mode)()
            if len(route_record) > 0:
                final_knowledge, all_routes, description = construct_final_knowledge_self_search(route_record, relation_aggregation)
            else:
                final_knowledge, all_routes, description = "", "", ""
            answer = final_answer(model, tp, final_knowledge)
            json_record.update({file: {"Answer": answer, "Route": all_routes, "Description": description}})

        with open(json_file, "w", encoding="utf-8") as f1:
            json.dump(json_record, f1, ensure_ascii=False, indent=4)


def final_answer(model, tp, knowledge):
    temp = tp.question_answer(knowledge)
    images = tp.images
    if images != "" and "Vision-needed" in mode:
        return model(temp, images)
    else:
        return model(temp, [])


if __name__ == "__main__":
    args = parser.parse_args()
    root = args.dataset_dir
    use_name = args.use_name
    use_extra = args.use_extra
    model_name = args.model_name
    api_key = args.api_key
    mode = args.mode
    if args.mode == "all":
        modes = ["Direct Vision-needed", "Direct", "Perfect", "self Search", "Offline", "Online Vision-needed"]
    else:
        modes = [mode]

    for mode in modes:
        print(mode)
        if "Offline" in mode:
            # file for question offline caption
            offline_file1_root = os.path.join(root, "questions_mh", "question_offline_" + model_name + ".json")
            with open(offline_file1_root, "r", encoding="utf-8") as f:
                offline_file1 = json.load(f)

            # file for mmkg caption
            offline_file2_root = os.path.join(root, "mmkg", "kg_offline_" + model_name + ".json")
            with open(offline_file2_root, "r", encoding="utf-8") as f:
                offline_file2 = json.load(f)
        else:
            offline_file1 = ""
            offline_file2 = ""


        json_file = os.path.join(root, "results", f"{model_name}_{mode}.json")
        process()


