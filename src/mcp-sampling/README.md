# Run demo with fast-agent

## Install

```bash
cd agent
uv venv -p 3.13                 # need python>=3.13 for fast-agent GPT-5 support
uv pip install fast-agent-mcp   # install fast-agent dependency to .venv
```


## Run

```bash
cd agent
uv run agent.py                 # optional pass model here, e.g. --model "sonnet"
```

## Prompt

```text
plot <full_path_to_csv>
```

