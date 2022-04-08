import json
import requests
import os
from utils import *
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# make sure you specify .env
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# COHERE_API_KEY = os.environ["COHERE_API_KEY"]
# GOOSEAI_API_KEY = os.environ["GOOSEAI_API_KEY"]
# GPTJ_API_KEY = os.environ["GPTJ_API_KEY"]
LABELSTUDIO_API_TOKEN = os.environ["LABELSTUDIO_API_TOKEN"]
LABELSTUDIO_ENDPOINT = os.environ["LABELSTUDIO_ENDPOINT"]


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


def check_toxicity(completions):
    results = []
    for completion in completions:
        url = "https://3ed0-35-185-109-155.ngrok.io/api"
        payload = {"data": [[completion]]}
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, json=payload, headers=headers)
        results.append(response.json()['data'][0])
    return results


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
