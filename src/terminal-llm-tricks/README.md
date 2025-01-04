# The awesome power of an LLM in your terminal

## Installation and setup

```bash
# Install
pip install llm

# Put in ~/.bashrc, ~/.zshrc or ~/.bash_profile
export OPENAI_API_KEY=

# Verify and test
llm "tell me something that I'll never forget"
llm -c "summarize this in a few words"

llm models
llm -m gpt-4o "evaluate the integral of y = 6*x^2 + 4"
llm -m gpt-4o "evaluate the integral of y = 6*x^2 + 4" -s "show your work"

llm logs
```

## Examples

### Command-line assistance

#### Print current date

```bash
llm 'linux print date. only output command'
llm -c 'as a timestamp'
```

#### Get help with file permissions

**Command:**
```bash
ls -l | llm 'output these file permissions in human readable format line by line'
```

#### Parse data
```bash
llm 'I have a CSV file like this and I need to detemine the smallest date (dt) column. Use a bash command.

dt,url,device_name,country,sessions,instances,bounce_sessions,orders,revenue,site_type
20240112,https://example.com/folder/page?num=5,,,2,0,1,,,web
20240209,https://example.com/,,,72,0,29,,,mobile
20240111,https://exmaple.com/page,,,1,0,1,,,web
'
```

#### Setup ufw
```bash
llm 'Give me a ufw command to open port 8081'
llm -c 'Do I need to restart it after?'
```

#### Log parsing

**Command:**
```bash
llm "I have a log file and want to extract all IPv4 addresses that appear more than 5 times"
llm -c "can you break down the command and explain each part?"
```

### Code Commenting and Documentation

#### Generating Function Documentation

**Scenario:** Create function docstrings and typehints.

**Command:**
```bash
cat ml_script.py | llm 'generate detailed docstrings and typehints for each function'
```

#### Documenting a Codebase

**Scenario:** Create documentation for an entire codebase.

**Command:**
```bash
# All python files in a folder
find . -name '*.py' | xargs cat | llm 'generate documentation for this codebase'

# All files committed to git
git ls-files | xargs -I {} sh -c 'echo "\n=== {} ===\n"; cat {}' | llm 'generate documentation for this codebase'

# e.g.
# /Users/alex/pro/zazencodes-courses/ml-quest-1-demand-forecasting/model
```

### Code Refactoring


#### Improving Readability

**Scenario:** Refactor code.

**Command:**
```bash
cat ml_script_messy.py | llm 'refactor this code and add comments to explain it'
```

#### Migrations

**Scenario:** Update legacy code.

**Command:**
```bash
cat py2_script.py | llm 'convert this to python3. Inlcude inline comments for every update you make'
cat py2_script.py | llm 'convert this to python3. Inlcude inline comments for every update you make'
```

### Debugging Assistance


#### Interpreting Error Messages

**Scenario:** Get suggestions for fixing a Python error.

**Command:**
```bash
llm "Explain this error and tell me how to fix it. Here's the python traceback:

[PASTE_TRACEBACK]
"

# e.g.
# python py2_script.py
```


#### Generating Test Cases

**Scenario:** Create units tests

**Command:**
```bash
cat ml_script.py | llm 'generate unit tests for each function'
```

**Example Output:**
```python
def test_calculate_area():
    # Test case 1: Normal values
    assert calculate_area(5, 10) == 50

    # Test case 2: Zero values
    assert calculate_area(0, 10) == 0
    assert calculate_area(5, 0) == 0

    # Test case 3: Negative values
    assert calculate_area(-5, 10) == -50
```


#### Analyzing Logs for Debugging

**Scenario:** Analyze logs to suggest potential causes of an issue.

**Command:**
```bash
cat docker_app.log | llm 'analyze these logs, summarize the errors and suggest potential causes'
```

### Boilerplate Code Generation


#### Setting Up a FastAPI app

**Scenario:** Generate api framework

**Command:**
```bash
llm "Generate boilerplate code for a FastAPI app with a single route. Only output the code" > app.py
llm -c "Add another route that accepts POST requests"
```


### Explaining Code

#### Explaining a Code Snippet

**Scenario:** You encounter an unfamiliar Python function and need a plain language explanation.

**Command:**
```bash
cat ml_script.py | llm "walk through this file and explain how it works. start with a summary and then go line-by-line through the most difficult sections."
```

#### Explaining a Full Project

**Scenario:** Provide a detailed breakdown of an entire codebase.

**Command:**
```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT

cat README.md | llm 'explain this project to me in one paragraph using bullet points'
find . -name "*.py" | xargs -I {} sh -c 'echo "\n=== {} ===\n"; cat {}' | llm -c 'given these files in the project, give me a more detailed explanation'
```

