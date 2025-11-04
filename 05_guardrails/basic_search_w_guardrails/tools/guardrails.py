import httpx
import json
import re

from typing import Tuple, Optional


#-------------------
# settings
#-------------------
GRANITE_GUARDIAN_URL = "http://localhost:11434"
LLAMA_GUARD_URL      = "http://localhost:11434"
SHIELDGEMMA_URL      = "http://localhost:11434"

MLCOMMONS_TAXONOMY_HAZARDS = {
    "S1": "Violent Crimes",
    "S2": "Non-Violent Crimes",
    "S3": "Sex-Related Crimes",
    "S4": "Child Sexual Exploitation",
    "S5": "Defamation",
    "S6": "Specialized Advice",
    "S7": "Privacy",
    "S8": "Intellectual Property",
    "S9": "Indiscriminate Weapons",
    "S10": "Hate",
    "S11": "Suicide and Self-Harm",
    "S12": "Sexual Content",
    "S13": "Elections"
}


#--------------------------
# guardrail functions
#--------------------------
def query_granite_guardian(model: str, input: str, criteria_id: str = "harm", think: bool = False, stream: bool = False) -> str:
    """Sends a request to the ShieldGemma endpoint for checking 

    Args:
        model: The model name (e.g., "ibm/granite3.3-guardian:8b").
        input: The input to send to the model (this can be the input prompt or output response)
        criteria_id: Type of risk detection (prompt/response text, RAG groundness/relevancy, Function Calling halucination)
        think: Whether to turn on thinking (enabling thinking increases time to arrive at score)
        stream: Whether to stream the response (False for a single response object).

    Returns:
        str: Either a 'yes' (violates policy)
             or 'no' (content is safe)
    """
    url = f"{GRANITE_GUARDIAN_URL}/api/generate"  # GRANITE_GUARDIAN_URL is just pointing to Ollama
    
    # The payload matches the JSON data in your curl command
    # https://github.com/ollama/ollama/blob/main/docs/api.md
    # NOTE: for Guardian models, "temperature" much be set to zero
    #       to ensure accurate assessment and scoring
    payload = {
        "model": model,
        "think": think,
        "guardian_config": {
            "criteria_id": criteria_id
        },
        "prompt": input,
        "stream": stream,
        "options": {
            "temperature": 0
        }
    }

    try:
        # httpx.post with the 'json' parameter handles the data encoding
        response = httpx.post(url, json=payload, timeout=None)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # The Ollama API returns JSON, so we can use response.json()
        result = response.json()

        # Check if the 'response' key exists and return its value
        if "response" in result:
            try:
                value = json.dumps(result["response"])
                match = re.search(r'<score>\s*(.*?)\s*</score>', value, re.DOTALL)

                if match:
                    # stripping the tags, retrieving only the value
                    gg_response = match.group(1).strip()

                    return gg_response
                else:
                    print("Error: 'score' tag not found")
                    return None
            except KeyError:
                print("Error")
                return None

    except httpx.RequestError as e:
        print(f"An error occurred while requesting from {e.request.url!r}: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Error {e.response.status_code} while requesting {e.request.url!r}: {e}")
        print(f"Response text: {e.response.text}")
        return None


def query_llama_guard(model: str, input: str, stream: bool = False) -> Tuple[str, Optional[str]]:
    """Sends a request to the Llama Guard endpoint for checking 

    Args:
        model: The model name (e.g., "llama-guard3:8b").
        input: The input to send to the model (this can be the input prompt or output response)
        stream: Whether to stream the response (False for a single response object).

    Returns:
        tuple: Status of the input's safety ('safe' or 'unsafe'),
               and the hazard category (S1 to S13) if it is 'unsafe'
    """
    url = f"{LLAMA_GUARD_URL}/api/generate"
    
    payload = {
        "model": model,
        "prompt": input,
        "stream": stream
    }

    try:
        response = httpx.post(url, json=payload, timeout=None)
        
        response.raise_for_status()
        
        result = response.json()
        
        if "response" in result:
            try:
                lg_response = json.dumps(result["response"])
                lines = lg_response.split('\\n')

                if len(lines) == 2:
                    status, code = lines
                    status = status.strip('"')
                    code = code.strip('"')
                    violation = f"{code} - {MLCOMMONS_TAXONOMY_HAZARDS[code]}"
                    return status, violation
                elif len(lines) == 1:
                    line = lines[0].strip('"')
                    return line, None
                else:
                    print("Error: Unexpected number of lines.")
                    return None, None
            except KeyError:
                print("Error")
                return None, None

    except httpx.RequestError as e:
        print(f"An error occurred while requesting from {e.request.url!r}: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Error {e.response.status_code} while requesting {e.request.url!r}: {e}")
        print(f"Response text: {e.response.text}")
        return None


def query_shieldgemma(model: str, input: str, stream: bool = False) -> str:
    """Sends a request to the ShieldGemma endpoint for checking 

    Args:
        model: The model name (e.g., "shieldgemma:9b").
        input: The input to send to the model (this can be the input prompt or output response)
        stream: Whether to stream the response (False for a single response object).

    Returns:
        str: Either a 'Yes' (violates safety policy)
             or 'No' (content is safe)
    """
    url = f"{SHIELDGEMMA_URL}/api/generate"
    
    payload = {
        "model": model,
        "prompt": input,
        "stream": stream
    }

    try:
        response = httpx.post(url, json=payload, timeout=None)
        
        response.raise_for_status()
        
        result = response.json()
        
        if "response" in result:
            try:
                sg_response = json.dumps(result["response"])

                # respose of "Yes" or "No" includes double-quotes
                # so I'm stripping them
                return sg_response.strip('"')
            except KeyError:
                print("Error")
                return None

    except httpx.RequestError as e:
        print(f"An error occurred while requesting from {e.request.url!r}: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Error {e.response.status_code} while requesting {e.request.url!r}: {e}")
        print(f"Response text: {e.response.text}")
        return None
