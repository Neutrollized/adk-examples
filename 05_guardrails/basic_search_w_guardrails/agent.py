import logging
import sys
import httpx
import json
from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from google.adk.tools import google_search

# used by callbacks
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional

from .tools.guardrails import (
    query_granite_guardian,
    query_llama_guard,
    query_shieldgemma,
)


#-------------------
# settings
#-------------------
model = "gemini-2.5-flash"

granite_guardian_model = "ibm/granite3.3-guardian:8b"
llama_guard_model      = "llama-guard3:8b"
shieldgemma_model      = "shieldgemma:9b"

ENABLE_GRANITE_GUARDIAN_PROMPT = True
ENABLE_LLAMA_GUARD_PROMPT      = False
ENABLE_SHIELDGEMMA_PROMPT      = False

ENABLE_GRANITE_GUARDIAN_RESPONSE = True
ENABLE_LLAMA_GUARD_RESPONSE      = False
ENABLE_SHIELDGEMMA_RESPONSE      = False


#-------------------
# callbacks
#-------------------
def query_before_model_guardrails(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """
    Inspects the LLM request
    """
    safety_score = 0
    safety_violation = ''

    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")
    print(f"[Callback] Invocataion ID: {callback_context.invocation_id}")
    print(f"[Callback] Callback state: {callback_context.state.to_dict()}")

    # Inspect the last user message in the request contents
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
         if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
            print(f"[Callback] Inspecting last user message: '{last_user_message}'")

    if ENABLE_GRANITE_GUARDIAN_PROMPT == True:
        score = query_granite_guardian(granite_guardian_model, last_user_message)
        if score == 'yes':
            safety_score += 1

    if ENABLE_LLAMA_GUARD_PROMPT == True:
        status, violation = query_llama_guard(llama_guard_model, last_user_message)
        if status == 'unsafe':
            safety_score += 2
            safety_violation = violation

    if ENABLE_SHIELDGEMMA_PROMPT == True:
        harmful_status = query_shieldgemma(shieldgemma_model, last_user_message)
        if harmful_status == 'yes':
            safety_score += 4

    if len(safety_violation) > 0:
        # Llama Guard detected a violation, respond with violation category
        print("[Callback] Harmful content detected. Skipping LLM call.")
        # Return an LlmResponse to skip the actual LLM call
        # LlmResponse is interpretted as the actual LLM response
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=f"I cannot comply with your request as it violates my security protocols: {violation}.")],
            )
        )
    elif safety_score > 0:
        # Granite Guardian and/or ShieldGemma flagged content
        print("[Callback] Harmful content detected. Skipping LLM call.")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="I cannot comply with your request as it violates my security protocols.")],
            )
        )
    elif safety_score == 0:
        print("[Callback] Query is safe.")
        return None


def check_response_after_model_guardrails(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    """
    Checks response produced by LLM
    """
    safety_score = 0
    safety_violation = ''

    agent_name = callback_context.agent_name
    print(f"[Callback] After model call for agent: {agent_name}")
    print(f"[Callback] Invocataion ID: {callback_context.invocation_id}")
    print(f"[Callback] Callback state: {callback_context.state.to_dict()}")

    original_text = ""
    if llm_response.content and llm_response.content.parts:
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
            print(f"[Callback] Inspecting response: '{original_text[:150]}...'")
    
            if ENABLE_GRANITE_GUARDIAN_RESPONSE == True:
                score = query_granite_guardian(granite_guardian_model, original_text)
                if score == 'yes':
                    safety_score += 1

            if ENABLE_LLAMA_GUARD_RESPONSE == True:
                status, violation = query_llama_guard(llama_guard_model, original_text)
                if status == 'unsafe':
                    safety_score += 2
                    safety_violation = violation

            if ENABLE_SHIELDGEMMA_RESPONSE == True:
                harmful_status = query_shieldgemma(shieldgemma_model, original_text)
                if harmful_status == 'yes':
                    safety_score += 4

            if len(safety_violation) > 0:
                # Llama Guard detected a violation, respond with violation category
                print("[Callback] Harmful content detected. Skipping response.")
                # Return an LlmResponse to skip the actual LLM call
                # LlmResponse is interpretted as the actual LLM response
                return LlmResponse(
                    content=types.Content(
                        role="model",
                        parts=[types.Part(text=f"I cannot return the response as it violates my security protocols: {violation}.")],
                    )
                )
            elif safety_score > 0:
                # Granite Guardian and/or ShieldGemma flagged content
                print("[Callback] Harmful content detected. Skipping response.")
                return LlmResponse(
                    content=types.Content(
                        role="model",
                        parts=[types.Part(text="I cannot return the response as it violates my security protocols.")],
                    )
                )
            elif safety_score == 0:
                print("[Callback] Response is safe.")
                return None

        elif llm_response.content.parts[0].function_call:
            print(f"[Callback] Inspected response: Contains function call '{llm_response.content.parts[0].function_call.name}'. No text modification.")
            return None # don't modify tool calls
        else:
            print("[Callback] Inspected response: No text content found.")
            return None
    elif llm_response.error_message:
        print(f"[Callback] Inspected response: Contains error '{llm_response.error_message}'. No modification.")
        return None
    else:
        print("[Callback] Inspected response: Empty LlmResponse.")
        return None


#-----------------
# agents
#-----------------
search_agent = LlmAgent(
    name="search_agent",
    model=model,
    description=(
        "Agent to answer questions using Google Search"
    ),
    instruction=(
        "I can answer your questions by searching the internet. Just ask me anything!"
    ),
    tools=[
        google_search,
    ],
    before_model_callback=query_before_model_guardrails,
    after_model_callback=check_response_after_model_guardrails,
)

root_agent = search_agent
