# This file records all the prompt templates for this project


class TP:
    def __init__(self, data_point, mode, use_name=True, use_extra=True):
        self.subgraph_options = ["Anjanath", "Azure Rathalos", "Barroth", "Bazelgeuse", "Brachydios", "Diablos", "Frostfang Barioth",
                            "Glavenus", "Kushala Daora", "Legiana", "Nergigante", "Rathalos", "Rathian", "Teostra", "Tigrex",
                            "Nargacuga", "Zinogre", "Pink Rathian", "Yian Garuga", "Radobaan", "Lunastra", "Stygian Zinogre"]
        self.data_point = data_point
        self.monster_name = self.data_point["Monster Name"]
        self.extra_info = self.data_point["Extra Information"]
        self.question = self.data_point["Question"]
        self.images = self.data_point["Images"]
        self.perception = data_point["Perception"]
        self.use_name= use_name
        self.use_extra = use_extra
        self.mode = mode
        self.temp1 = "You are a professional Monster Hunter player. You are playing 'Monster Hunter: World'."


    def temp2(self):
        if self.perception == "":
            temp = f"""
        Here is the 'Question' you need to answer:
        {self.question}
        """
        elif "Vision-needed" in self.mode:
            temp = f"""
        Based on the battle screen, here is the 'Question' you need to answer:
        {self.question}
            """
            temp = self.temp4() + temp
        else:
            temp = f"""
        The text description of the battle screen is:
        "{self.perception}"
        Based on the battle screen, here is the 'Question' you need to answer:
        "{self.question}"
        """
        return temp


    def temp3(self):
        # A template for monster name
        if self.use_name:
            temp = f" with {self.monster_name}"
        else:
            temp = ""
        return temp


    def temp4(self):
        # A template for single or multi images as input
        if len(self.images) == 1:
            temp = f"You will receive a image of battle screen{self.temp3()}."
        else:
            temp = f"You will receive consecutive video frames showing the battle screen{self.temp3()}."
        return temp


    def temp6(self, memory, entity):
        # A template for aggregating knowledge as memory
        if memory != "":
            temp = f"""
            The following contents are the knowledge you found so far (up to current entity: "{entity}"):
            ******
            {memory}
            ******
            """
        else:
            temp = ""
        return temp


    def temp7(self, images, memory):
        # A template for entity

        if "Online" in self.mode and images != "":
            if memory != "":
                temp = f"You have to decide whether visual and text information of this entity together with previous found knowledge is sufficient for answering this 'Question'."
            else:
                temp = f"You have to decide whether visual and text information of this entity is sufficient for answering this 'Question'."

            temp += f"""
            For sufficient analysis, your 'Answer' is 'Yes' or 'No'.
            Directly output your 'Response' as the combination of 'Answer' and 'Description', separating them directly by ';'.
            """
        else:
            if memory != "":
                temp = f"Your Response is to decide whether the information of this entity together with previous found knowledge is sufficient for perfectly answering this 'Question'."
            else:
                temp = f"Your Response is to decide whether the information of this entity is sufficient for perfectly answering this 'Question'."

            temp += f"""
            If it is 100% sufficient, directly output 'Yes'.
            If it is not sufficient, directly output 'No'.
            Note that you should be very careful for the sufficiency analysis.
            """
        return temp


    def temp8(self, entity_images, entity):
        if "Online" in self.mode and entity_images != "":
            if len(entity_images) == 1:
                temp = f"You will also receive a image of battle screen{self.temp3()} as visual information for current entity \"{entity}\"."
            else:
                temp = f"You will also receive consecutive video frames showing the battle screen{self.temp3()} as visual information for current entity \"{entity}\"."
            temp += "Make a 'Description' (do not affected by previous text description of the battle screen for the 'Question') for the battle screen as a part of your 'Response'. 'Description' should include monster's limb and body movements, mouth, surrounding and others details. Note that you should not give any assumptions for the 'Description'."
        else:
            temp = ""
        return temp


    def temp9(self):
        temp = f"""
                The text description of the battle screen is:
                "{self.perception}"
                Based on the battle screen, here is the 'Question' you need to answer:
                "{self.question}"
                """
        return temp


    def topic_entity_selection(self):
        # A template for select the topic entity based on the input question
        template_ = f"""
        You are a professional Monster Hunter player. Based on the input 'Question', try to find the most relevant monster name related to the question from all 'Options'.
        The input 'Question' is:
        "{self.question}"
        You will also receive a image of battle screen as visual information for this 'Question'.
        All possible monster names 'Options' are structured in a list format as follows:
        {self.subgraph_options}
        Note that your 'Response' is to directly output the name of the monster you are looking for. 
        Note that you should not output any information other than your 'Response'.
        Now, start to complete your task.
        Your 'Response':
        """
        # print(template_)
        return template_


    def question_image_understanding(self):
        # A template for translating input image or images into text description, only used for online version
        template_ = f"""
        {self.temp1}
        {self.temp4()}
        The input 'Question' for the battle screen is:
        "{self.question}"
        Make a 'Description' for the battle screen as your 'Response'. 'Description' should include monster's limb and body movements, mouth, surrounding and others details.
        Note that you should not give any assumptions for the 'Description'.
        Note that you should directly output your 'Response' and do not output any information other than your 'Response'.
        Now, start to complete your task.
        Your 'Response':
        """
        # print("PPPPPPPPPPPPPPPPP")
        # print(template_)
        return template_


    def question_answer(self, knowledge):
        if knowledge != "":
            temp_ = f"""
        Here is the 'Knowledge' you retrieved from a knowledge graph for this 'Question':
        ******
        {knowledge}
        ******
        Your 'Response' is to provide the answer for this 'Question' based on the retrieved Knowledge.
        """
        else:
            temp_ = """
        Your 'Response' is to provide the answer for this 'Question'.
        """

        template_ = f"""
        {self.temp1}
        {self.temp2()}
        {temp_}
        Note that you should not give any analysis.
        Note that you should not output any information other than your 'Response'.
        Now, start to complete your task.
        Your 'Response':
        """
        return template_


    def entity_selection(self, memory, current_entity, neighbor_entity):
        template_ = f"""
        {self.temp1}
        {self.temp9()}
        
        To answer the above question, you are now searching a knowledge graph to find the route towards relevant knowledge.
        {self.temp6(memory, current_entity)}
        You need to select the relevant 'Neighbor Entity' that may provide knowledge to answer the question.
        The relation and condition from current entity '{current_entity}' to all 'Neighbor Entity' are:
        ******
        {neighbor_entity}
        ******
        Your 'Response' is directly output the name of all relevant 'Neighbor Entity' and seperated them directly by ';'.
        If there is no relevant 'Neighbor Entity', directly output 'None'.
        Note that if the 'Neighbor Entity' is an attack action, always choose it (if it is not highly irrelevant).
        Note that if the 'Neighbor Entity' is a phase, you can only choose one.
        Note that you should not output any information other than your 'Response'.
        Now, start to complete your task.
        Your 'Response':
        """
        # print("SSSSSSSSSSSSSSSSSSSSSS")
        # print(template_)
        return template_


    def entity_analysis(self, memory, entity, entity_info, entity_images=""):
        if entity_info != "":
            temp = f"""
            And here is some information of current entity:
            {entity_info}
            """
        else:
            temp = ""

        if self.perception == "":
            ttt = self.temp2()
        else:
            ttt = self.temp9()

        template_ = f"""
        {self.temp1}
        {ttt}
        
        To answer the above question, you are now searching a knowledge graph to find the route towards relevant knowledge.
        {self.temp6(memory, entity)}
        {temp}
        {self.temp8(entity_images, entity)}
        {self.temp7(entity_images, memory)}        
        Note that you should not output any information other than your 'Response'.
        Now, start to complete your task.
        Your 'Response':
        """
        # print("AAAAAAAAAAAAAAAAA")
        # print(template_)
        return template_


def offline_images_description(images, name, entity):
    if len(images) == 1:
        temp = f"You will receive a image of battle screen{name}"
    else:
        temp = f"You will receive consecutive video frames showing the battle screen{name}"

    template = f"""
    You are a professional Monster Hunter player. You are playing 'Monster Hunter: World'.
    {temp} as visual information for {entity}.
    Make a 'Description' for the battle screen as your 'Response'. 'Description' should include monster's limb and body movements, mouth, surrounding and others details.
    Note that you should not output any information other than your 'Response'.
    Now, start to complete your task.
    Your 'Response':
    """

    return template


def evaluation_temp(question, answer1, answer2):
    template = f"""
    You are a professional Monster Hunter player. You are playing 'Monster Hunter: World'.
    Here is a 'Question' need to be answered:
    {question} 
    There are also two answers for this 'Question':
    Answers 1: {answer1}
    Answers 2: {answer2}
    Your 'Response' is to decide whether the content of these two answers are similar.
    If similar directly output 'Yes'.
    If not similar directly output 'No'.
    Note that you may ignore the format difference.
    Ignore the difference of monster name before word, e.g., "Zinogre Leap Attack" and "Leap Attack" are with same meaning.
    
    Here are some samples for decide similarity:
    Sample 1:
    'Question': Tell me what is the specific name of attack action that Zinogre is performing?
    "Answer 1": Static Charge
    "Answer 2": Thunder Charge B
    "Response": No
    
    Sample 2:
    'Question': Start with counterattack, Zinogre released the attack action shown in the input battle screen. Tell me what is the next attack action?
    "Answer 1": \"Zinogre Back Slam\"
    "Answer 2": Back Slam
    "Response": Yes
    
    Sample 3:
    'Question': What attack action Brachydios is unleashing??
    "Answer 1": Brachydios is unleashing the \"Brachydios Ground Slime Explosion\" attack
    "Answer 2": Ground Slime Explosion
    "Response": Yes
    
    Note that you should not output any information other than your 'Response'.
    Now, start to complete your task.
    Your 'Response':
    """

    return template


def evaluation_temp_caption(truth, generated):
    template = f"""
    You are a professional Monster Hunter player. You are playing 'Monster Hunter: World'.
    Here are two text description of a monster attack action.
    Your 'Response' is to decide whether the content of these two text descriptions are similar.
    Your should focus on the details of movement and some key information that can help you to discriminate the action.
    If similar directly output 'Yes'.
    If not similar directly output 'No'.
    
    The First description is {truth}
    The Second description is {generated} 

    Note that you should not output any information other than your 'Response'.
    Now, start to complete your task.
    Your 'Response':
    """

    return template