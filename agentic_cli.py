#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import subprocess
import sys
import re
import os

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "coder11v/mycode1" 

def pull_model():
    print(f"📥 Pulling {MODEL_NAME} from Ollama if necessary...")
    try:
        subprocess.run(["ollama", "pull", MODEL_NAME], check=True)
        print("✅ Model ready!\n")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to pull the model {MODEL_NAME}. Is Ollama running?")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 'ollama' command not found. Please ensure Ollama is installed and in your PATH.")
        sys.exit(1)

def chat_with_agent(messages):
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }
    
    req = urllib.request.Request(
        OLLAMA_URL, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['message']
    except urllib.error.URLError as e:
        print(f"❌ Error connecting to Ollama: {e}")
        print("Please ensure the Ollama server is running (ollama serve).")
        sys.exit(1)

def main():
    print("🚀 Initializing Agentic CLI...")
    
    pull_model()
    
    print("🤖 Agentic CLI is ready! Type 'exit' to quit.")
    print("------------------------------------------------")
    
    messages = []
    
    while True:
        try:
            user_input = input("\n🧑‍💻 You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
            
        if user_input.strip().lower() in ['exit', 'quit']:
            break
            
        if not user_input.strip():
            continue
            
        messages.append({"role": "user", "content": user_input})
        
        while True:
            # print("🤖 Agent is thinking...")
            message = chat_with_agent(messages)
            content = message.get('content', '')
            
            messages.append(message)
            
            # Look for command requests
            match = re.search(r'<run_command>(.*?)</run_command>', content, re.DOTALL)
            
            if match:
                command = match.group(1).strip()
                pre_text = content[:match.start()].strip()
                
                if pre_text:
                    print(f"\n🤖 Agent: {pre_text}")
                    
                print(f"\n⚡ Proposed Command: {command}")
                confirm = input("Run this command? [Y/n]: ").strip().lower()
                if confirm == 'n':
                    print("⚠️ Command aborted by user.")
                    messages.append({"role": "user", "content": "Command Output:\nUser denied permission to run this command. What is your next step or try a different approach?"})
                    continue
                    
                print(f"⚡ Executing...")
                try:
                    result = subprocess.run(
                        command, 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        timeout=60
                    )
                    stdout = result.stdout.strip()
                    stderr = result.stderr.strip()
                    
                    output = []
                    if stdout:
                        output.append(stdout)
                    if stderr:
                        output.append(f"ERROR:\n{stderr}")
                        
                    output_str = "\n".join(output) if output else "Command executed successfully with no output."
                    
                    # Print truncated output to user
                    display_out = output_str[:1000] + ('\n...[truncated]' if len(output_str) > 1000 else '')
                    print(f"📄 Result:\n{display_out}")
                    
                    messages.append({
                        "role": "user", 
                        "content": f"Command Output:\n{output_str}\n\nWhat is your next step?"
                    })
                    
                except subprocess.TimeoutExpired:
                    print("⚠️ Command timed out.")
                    messages.append({"role": "user", "content": "Command Output:\nTimed out after 60 seconds."})
                except Exception as e:
                    print(f"⚠️ Error executing command: {e}")
                    messages.append({"role": "user", "content": f"Command Error:\n{e}"})
            else:
                # No commands, just regular output
                print(f"\n🤖 Agent: {content}")
                break

if __name__ == "__main__":
    main()
