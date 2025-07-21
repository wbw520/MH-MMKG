import base64
import os
import anthropic
import google.generativeai as genai
from openai import OpenAI
import cv2


def model_selection(model_name):
    if "gpt" in model_name:
        return GPT4(model_name)
    elif "claude" in model_name:
        return Claude(model_name)
    elif "gemini" in model_name:
        return Gemini(model_name)

os.environ['OPENAI_API_KEY'] = 'sk-proj-a4kV7LXxBy625HUi7agET3BlbkFJPSFs9AAK0Fl3771uzdME'
client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class GPT4:
    def __init__(self, model_name):
        self.mode_name = model_name
        # gpt-4o-mini-2024-07-18
        # gpt-4o-2024-11-20

    # combine both text and images
    def make_content(self, text, images):
        image_paths = images
        content = [
            {
                            "type": "text",
                            "text": text,
                        }
        ]
        for image_path in image_paths:
            image_path = compress_image(image_path)
            base64_image = encode_image(image_path)
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                }
            )
        return content


    def __call__(self, text, images):
        content = self.make_content(text, images)
        response = client.chat.completions.create(
            model=self.mode_name,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            temperature=0,
            top_p=1,
        )

        return response.choices[0].message.content


def ensure_dir_exists(file_path):
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)


def compress(input_path, output_path, scale=0.5):
    img = cv2.imread(input_path)
    height, width = img.shape[:2]
    new_size = (int(width * scale), int(height * scale))
    resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    ensure_dir_exists(output_path)
    cv2.imwrite(output_path, resized_img)
    file_size = os.path.getsize(output_path)
    if file_size > 3 * 1024 * 1024:
        scale = 0.4
        new_size = (int(width * scale), int(height * scale))
        resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(output_path, resized_img)


def compress_image(root, name=""):

    if "gemini" in name or "claude" in name:
        new_root = root.replace("D:\PycharmProjects\MM-KG", "D:\PycharmProjects\MM-KG\Compress Source Gemini")
        scale = 0.3
    else:
        new_root = root.replace("D:\PycharmProjects\MM-KG", "D:\PycharmProjects\MM-KG\Compress Source")
        scale = 0.5

    if os.path.exists(new_root):
        return new_root
    else:
        compress(root, new_root, scale)
        return new_root


client2 = anthropic.Anthropic(
    api_key="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",
)

class Claude:
    def __init__(self, model_name):
        self.mode_name = model_name
        # claude-3-7-sonnet-20250219
        # claude-3-5-sonnet-20241022
        # claude-3-5-haiku-20241022

    def make_content(self, text, images):
        image_paths = images
        content = [
            {
                            "type": "text",
                            "text": text,
                        }
        ]
        for image_path in image_paths:
            image_path = compress_image(image_path, self.mode_name)
            base64_image = encode_image(image_path)
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",  # 根据图像类型调整
                        "data": base64_image
                    }
                }
            )
        return content

    def __call__(self, text, images):
        content = self.make_content(text, images)
        response = client2.messages.create(
            model=self.mode_name,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            temperature=0,
            top_p=1,
        )

        return response.content[0].text

genai.configure(api_key="AIzaSyAMCjd5yeqxxcI8Z6xYpBU0fBQ6W1jcUis")

class Gemini:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)
        # gemini-1.5-pro-002
        # gemini-2.0-flash-001
        # gemini-2.5-flash-preview-04-17
        # gemini-2.5-pro-preview-05-06

    def make_content(self, text, images):
        image_paths = images
        content = [text]
        for image_path in image_paths:
            image_path = compress_image(image_path, self.model_name)
            base64_image = encode_image(image_path)
            content.append({"mime_type": "image/png", "data": base64_image})
        return content

    def __call__(self, text, images):
        content = self.make_content(text, images)
        response = self.model.generate_content(content)

        return response.text
