# Ollama API

- example:
```sh
curl http://localhost:11434/api/generate -d '{
  "model": "llama-guard3:8b",
  "prompt": "This burger is the bomb!",
  "stream": false
}'
```

## Comparing Llama Guard 3-8B vs ShieldGemma 1-9B
You will need to have downloaded these two models in your Ollama, but afterwards, uncomment some of the `user_prompt` examples I have at the bottom of `guardrails.py` and see the results for yourself. Most notably in the example about Pete Rose and Wayne Gretzky being in a gay, ShieldGemma says this is safe. Even though these are famous sports celebrities, Gemma doesn't seem to know who they are, but if you claim that the POTUS is gay, then it does violate its safety policy. 
