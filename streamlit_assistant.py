import speech_recognition as sr
import pyttsx3
import subprocess
import os
import webbrowser
import requests
import datetime
from openai import AzureOpenAI
from dotenv import load_dotenv
import streamlit as st

# load environment variables
load_dotenv()

# Note: For ease of work one can try mentioning all the respective values for below variables in string.
api_key= os.getenv("azure_openai_api_key") # Here you have to mention your azure openai api key.
api_version= os.getenv("azure_api_version") # Here you have to mention your azure openai api version.
azure_endpoint= os.getenv("azure_endpoint") # Here you have to mention your azure openai endpoint.
azure_deployment= os.getenv("azure_deployment_name") # Here you have to mention your azure openai deployment name.