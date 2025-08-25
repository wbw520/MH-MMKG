import random


def construct_final_knowledge(knowledge_routes, entity_aggregation, relation_aggregation):
    all_knowledge = ""
    for i in range(len(knowledge_routes)):
        route = knowledge_routes[i]
        knowledge = route_aggregation(route, entity_aggregation, relation_aggregation)
        all_knowledge += f"Retrieved Knowledge {i}:\n"
        all_knowledge = all_knowledge + knowledge
    return all_knowledge


def construct_final_knowledge_self_search(knowledge_routes, relation_aggregation):
    all_knowledge = ""
    all_routes = []
    all_description = []
    for i in range(len(knowledge_routes)):
        route = knowledge_routes[i]
        all_routes.append(route["route"])
        all_description.append(route["description"])
        knowledge = route_aggregation(route["route"], route["entity"], relation_aggregation)
        all_knowledge += f"Retrieved Knowledge {i}:\n"
        all_knowledge = all_knowledge + knowledge
    return all_knowledge, all_routes, all_description


def route_aggregation(search_route, entity_aggregation, relation_aggregation, end_not_include=False):
    # if end_not_include=True, last entity information will not be included.
    len_route = len(search_route)
    previous = []
    knowledge = """"""
    for i in range(len_route):
        if search_route[i] in previous:
            break
        elif i == len_route - 1 and end_not_include:
            break
        else:
            entity_1 = search_route[i]
            knowledge += entity_info_construction(entity_1, entity_aggregation, mode="")

            if i < len_route-1:
                entity_2 = search_route[i + 1]
                knowledge += relation_info_construction(entity_1, entity_2, relation_aggregation)
        previous.append(search_route[i])

    return knowledge


def entity_info_construction(entity_name, entity_aggregation, mode):
    if entity_name not in entity_aggregation:
        return "No Name"
    entity_info = entity_aggregation[entity_name]
    info = ""
    if "Online" in mode:
        if entity_info["Additional Information"] != "":
            info += "Additional Information: " + entity_info["Additional Information"]
            if entity_info["Action Description"] != "":
                info = "Action Description: " + entity_info["Action Description"] + " " + info
            return f"\"{entity_name}\"" + ": " + info + "\n"
        else:
            return ""
    else:
        if entity_info["Action Description"] != "":
            info += "Action Description: " + entity_info["Action Description"] + " "
        if entity_info["Additional Information"] != "":
            info += "Additional Information: " + entity_info["Additional Information"]
        return f"\"{entity_name}\"" + ": " + info + "\n"


def relation_info_construction(entity_1, entity_2, relation_aggregation):
    # print(entity_1)
    # print(entity_2)
    # print(relation_aggregation[entity_1])
    entity_1_relation_entity_2 = relation_aggregation[entity_1][entity_2]
    relation = entity_1_relation_entity_2["Relation"]
    condition = entity_1_relation_entity_2["Condition"]
    if condition == "":
        relation_ = f"\"{entity_1}\" " + relation + f" \"{entity_2}\"" + ".\n"
    else:
        relation_ = f"\"{entity_1}\" " + relation + f" \"{entity_2}\" (if satisfied \"Condition\" of {condition})" + ".\n"
    return relation_


class KnowledgeSearch:
    def __init__(self, tp, model, entity_aggregation, relation_aggregation, mode):
        self.mode = mode
        self.knowledge_route = []
        self.tp = tp
        self.model = model
        self.root_explore_index = 0
        self.root_record = {}
        self.entity_aggregation = entity_aggregation
        self.relation_aggregation = relation_aggregation
        self.time_record = []

    def search(self,record, current_entity):
        # if there are neighbors
        if len(self.knowledge_route) > 4:
            # default using 5 knowledge
            print(f"already have 5 knowledge!")
            return
        if current_entity in self.relation_aggregation:
            all_neighbours_info = self.relation_aggregation[current_entity]
            all_neighbours_entity = list(all_neighbours_info.keys())
            neighbour_selection = ""

            # aggregating all neighbours entity with relations
            for neighbour_entity in all_neighbours_entity:
                neighbour_selection += relation_info_construction(current_entity, neighbour_entity, self.relation_aggregation)

            memory_for_entity_selection = route_aggregation(record["route"], record["entity"], self.relation_aggregation)
            related_neighbour_entity = self.model(self.tp.entity_selection(memory_for_entity_selection, current_entity, neighbour_selection), []).replace("\n", "")
            # print("NNNNNNNNNNNNN", related_neighbour_entity)

            # save all current loop info
            recursion_calls = []
            # if there is any related neighbour entity
            if related_neighbour_entity != "None":
                related_neighbour_entity_ = related_neighbour_entity.split(";")
                if "Phase" in related_neighbour_entity:
                    # force to process only one phase type neighbour
                    rrrr = []
                    for rr in related_neighbour_entity_:
                        if rr != "":
                            rrrr.append(rr)
                    ll = len(rrrr)
                    if ll > 1:
                        sl = random.randrange(0, ll)
                        related_neighbour_entity_ = [rrrr[sl]]

                # print(related_neighbour_entity_)
                for next_search_entity in related_neighbour_entity_:
                    next_search_entity = next_search_entity.strip()
                    if next_search_entity == "":
                        break
                    if next_search_entity not in self.relation_aggregation[current_entity]:
                        continue
                    # if next neighbour_entity will cause of circle we stop it and record it as a possible knowledge
                    # print("record route", record["route"])
                    # print("current search entity", next_search_entity)
                    if next_search_entity in record["route"]:
                        current_route_record = record["route"].copy()
                        current_route_record.append(next_search_entity)
                        self.knowledge_route.append({"route": current_route_record, "entity": record["entity"].copy(), "description": record["description"].copy()})
                        continue
                    next_search_entity_info = entity_info_construction(next_search_entity, record["entity"], self.mode)
                    current_route_record = record["route"].copy()
                    current_route_record.append(next_search_entity)
                    memory_for_entity_analysis = route_aggregation(current_route_record, record["entity"], self.relation_aggregation, True)

                    #get entity images for online mode if exist
                    images = record["entity"][next_search_entity]["Images"]
                    if next_search_entity in self.tp.monster_name:
                        images = ""

                    if "Online" in self.mode and images != "":
                        print(images)
                        next_search_entity_results = self.model(self.tp.entity_analysis(memory_for_entity_analysis, next_search_entity, next_search_entity_info, images), images)
                        all_results = next_search_entity_results.split(";")
                        next_search_entity_status, entity_description = all_results[0], all_results[1]
                        # record the online action description
                        record["entity"][next_search_entity]["Action Description"] = entity_description
                        # print(entity_description)
                        record["description"].update({next_search_entity: entity_description})
                    else:
                        next_search_entity_status = self.model(self.tp.entity_analysis(memory_for_entity_analysis, next_search_entity, next_search_entity_info), [])

                    if "Yes" in next_search_entity_status:
                        next_search_entity_status = "Yes"
                    elif "No" in next_search_entity_status:
                        next_search_entity_status = "No"
                    else:
                        continue
                    # print(">>>>>>>>>>>>>>>>", next_search_entity_status)
                    current_record = {"route": current_route_record, "entity": record["entity"].copy(), "description": record["description"].copy()}
                    if next_search_entity_status == "Yes":

                        self.knowledge_route.append(current_record)
                    else:
                        recursion_calls.append((current_record, next_search_entity))

            if len(recursion_calls) > 0:
                for call in recursion_calls:
                    self.search(*call)

    def __call__(self):
        # for online if there is image for question
        if "Online" in self.mode and self.tp.images != "":
            question_description = self.model(self.tp.question_image_understanding(), self.tp.images)
            self.tp.perception = question_description

        if self.tp.images != "":
            topic_entity = self.model(self.tp.topic_entity_selection(), self.tp.images).replace("\n", "")
        else:
            topic_entity = self.model(self.tp.topic_entity_selection(), []).replace("\n", "")

        # Evaluation for topic entity
        topic_entity_info = entity_info_construction(topic_entity, self.entity_aggregation, self.mode)
        if topic_entity_info == "No Name":
            return self.knowledge_route

        status_topic_entity = self.model(self.tp.entity_analysis("", topic_entity, topic_entity_info), [])
        # print(status_topic_entity)

        if status_topic_entity == "Yes":
            self.knowledge_route.append({"route": [topic_entity], "entity": self.entity_aggregation.copy(), "description": {}})
            return self.knowledge_route

        self.search({"route": [topic_entity], "entity": self.entity_aggregation.copy(), "description": {}}, topic_entity)

        return self.knowledge_route


