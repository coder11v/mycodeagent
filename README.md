# MyCode Agentic CLI

A blazing fast, simple coding agent that runs securely on your local machine using [Ollama](https://ollama.com). Powered by the `coder11v/mycode1` model, this CLI can execute shell commands, read files, write code, and assist you with debugging—all from your terminal.

## Requirements

- Python 3
- [Ollama](https://ollama.com) installed and running locally.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/coder11v/mycodeagent.git
   cd mycodeagent
   ```

2. Make the script executable:
   ```bash
   chmod +x agentic_cli.py
   ```

## Usage

Simply run the agent script. It will automatically pull the `coder11v/mycode1` model from Ollama if you don't already have it installed.

```bash
./agentic_cli.py
```

### Safety Features
Before executing any shell command, the agent will prompt you to confirm. You can type `Y` to run the command or `n` to abort it and let the agent know you denied the command so it can adapt.

## Features
- **Fast Execution**: Operates with 0.0 temperature and minimal conversational overhead for snappy performance.
- **Auto-Pulling Model**: Built-in support to grab `coder11v/mycode1` on the first run.
- **Context-Aware**: Uses context to adapt to command outputs continuously.
