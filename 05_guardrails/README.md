# Basic Search with Guardrails

This is my basic search agent from my very first agent example, but with guardrails implemented via Granite Guardian, Llama Guard, and ShieldGemma.

Toggle which safeguard LLM model(s) to use on the user prompt and model response:
```python
ENABLE_GRANITE_GUARDIAN_PROMPT = True
ENABLE_LLAMA_GUARD_PROMPT      = False
ENABLE_SHIELDGEMMA_PROMPT      = False

ENABLE_GRANITE_GUARDIAN_RESPONSE = True
ENABLE_LLAMA_GUARD_RESPONSE      = False
ENABLE_SHIELDGEMMA_RESPONSE      = False
```

I chose Granite-3.3 Guardian as the default because it was the most recent (Aug 2025) safeguard model available at the time of writing. Llama Guard 3 (July 2024) and ShieldGemma (July 2024) both work well, but neither one on its own performed as well as Granite Guardian did in my small sample size of test prompt.

You can choose to enable more than one safeguard model to yield better risk assessment results at the expense of latency (and cost if you're deploying to a cloud service).


## Requirements
You will need [Ollama](https://ollama.com/) to host these models on your local machine.
