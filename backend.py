import json
import requests
import os
import openai
import streamlit as st

# make sure you specify .env
OPENAI_KEY = os.environ["OPENAI_KEY"]
# COHERE_KEY = os.environ["COHERE_KEY"]
# GOOSEAI_KEY = os.environ["GOOSEAI_KEY"]
# GPTJ_KEY = os.environ["GPTJ_KEY"]
LABELSTUDIO_ENDPOINT = os.environ["LABELSTUDIO_ENDPOINT"]
LABELSTUDIO_API_TOKEN = os.environ["LABELSTUDIO_API_TOKEN"]


def openai_inference_request(input_text, temperature=0.9, number_of_completions=1):

    loading = st.info(f"Running prediction request ...")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    n = number_of_completions
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input_text,
        temperature=temperature,
        max_tokens=6,
        n=n,
        stream=True,
    )
    response["choices"][0]["text"]

    loading.empty()

    return response["choices"][0]["text"]


def import_to_labelstudio(
    input_text, project_id, predicted_labels, predicted_scores, model_name=""
):

    url = f"{LABELSTUDIO_ENDPOINT}/api/projects/{project_id}/tasks/bulk/"

    auth_token = f"Token {LABELSTUDIO_API_TOKEN}"

    payload = [
        {
            "data": {"text": input_text, "meta_info": {"model_name": model_name}},
            "annotations": [
                {
                    "result": [
                        {
                            "from_name": "category",
                            "to_name": "content",
                            "type": "choices",
                            "value": {"choices": predicted_labels},
                        }
                    ],
                }
            ],
        }
    ]

    print(payload)
    headers = {"Content-Type": "application/json", "Authorization": auth_token}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
