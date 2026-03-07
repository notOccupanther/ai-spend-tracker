#!/usr/bin/env python3
"""
update_models.py — Check OpenAI for new GPT models vs our tracked list.
Does NOT auto-add models. Flags new ones for human review only.
"""

import json
import re
import os
import urllib.request
import urllib.error
from datetime import date

MODELS_JSON = os.path.join(os.path.dirname(__file__), '..', 'public', 'models.json')
OPENCLAW_CONFIG = os.path.expanduser('~/.openclaw/openclaw.json')


def get_openai_key():
    try:
        with open(OPENCLAW_CONFIG, 'r') as f:
            content = f.read()
        match = re.search(r'(sk-proj-[A-Za-z0-9_\-]{20,})', content)
        if match:
            return match.group(1)
    except Exception as e:
        print(f'[WARN] Could not read OpenAI key from {OPENCLAW_CONFIG}: {e}')
    return None


def load_models_json():
    with open(MODELS_JSON, 'r') as f:
        return json.load(f)


def save_models_json(data):
    with open(MODELS_JSON, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


def fetch_openai_models(api_key):
    req = urllib.request.Request(
        'https://api.openai.com/v1/models',
        headers={
            'Authorization': 'Bearer ' + api_key,
            'User-Agent': 'ai-spend-tracker/1.0',
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = json.loads(resp.read().decode())
    return [m['id'] for m in body.get('data', [])]


def main():
    print('=== AI Model Checker ===')
    print(f'Date: {date.today()}')
    print()

    # Load our current tracked models
    data = load_models_json()
    our_models = [m['model'].lower() for m in data.get('models', [])]
    print(f'Tracked models: {len(our_models)}')
    for m in data.get('models', []):
        print(f'  - {m["model"]} ({m["provider"]})')
    print()

    # Get API key
    api_key = get_openai_key()
    if not api_key:
        print('[ERROR] No OpenAI API key found. Skipping API check.')
        return

    # Fetch OpenAI models
    print('Fetching OpenAI model list...')
    try:
        openai_models = fetch_openai_models(api_key)
    except urllib.error.HTTPError as e:
        print(f'[ERROR] OpenAI API error: {e.code} {e.reason}')
        return
    except Exception as e:
        print(f'[ERROR] Failed to fetch OpenAI models: {e}')
        return

    print(f'OpenAI models available: {len(openai_models)}')

    # Filter to GPT models only (skip fine-tuned, embeddings, whisper, etc.)
    gpt_models = sorted([m for m in openai_models if m.startswith('gpt-')])
    print(f'GPT models found: {len(gpt_models)}')
    print()

    # Find new ones not in our list
    new_models = [m for m in gpt_models if m.lower() not in our_models]

    if not new_models:
        print('✅ No changes — all current GPT models are already tracked or expected.')
    else:
        print(f'⚠️  {len(new_models)} new GPT model(s) found — review and add manually if needed:')
        for m in new_models:
            print(f'  + {m}')

    # Update last_checked timestamp (not last_updated — don't claim data changed)
    data['last_checked'] = str(date.today())
    save_models_json(data)
    print()
    print(f'Updated last_checked timestamp in models.json: {date.today()}')


if __name__ == '__main__':
    main()
