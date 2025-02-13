# DeepSeek Ollama

## Goals

- [ ] Install ollama
- [ ] Run deepseek models locally in terminal
- [ ] Understand (roughly) how it works
- [ ] Integrate with avante.nvim

## Tutorial

1. Install ollama

https://ollama.com/

2. Pull model

```bash
ollama --help
ollama list

# https://ollama.com/library/deepseek-r1
ollama pull deepseek-r1:1.5b
ollama list

# Where models are stored
ls ~/.ollama
du -sh ~/.ollama/models
```

3. Use model locally

```bash
# Keep an eye on CPU
htop -F "ollama"

MODEL=deepseek-r1:1.5b
ollama show $MODEL
ollama run $MODEL
ollama ps

ollama stop $MODEL
```

4. Run ollama

```bash
ollama serve

lsof -i :11434
lsof -i :11434 | llm 'explain this output in a few bullet points'
```

5. Use with `avante.nvim`

```bash
vim ~/.config/nvim

# https://github.com/yetone/avante.nvim/wiki/Custom-providers#ollama
```

6. Use with `llm` cli tool

```bash
llm install llm-ollama

# https://github.com/taketwo/llm-ollama
```


