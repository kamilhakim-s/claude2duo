#!/usr/bin/env python3
"""Drive GitLab Duo Chat via the GraphQL aiAction API to run the validation question set
against each context-pack variant.

EXPERIMENTAL — run this INSIDE your corporate network against your on-prem GitLab.
Requires: GitLab 16.9+ with Duo Chat enabled, and a personal access token with the
`api` scope (some versions want `ai_features`). The API cannot attach files like the
IDE does, so pack content is inlined into the first message; this validates content
quality, not IDE attachment behaviour.

Usage:
  export GITLAB_URL=https://gitlab.yourcompany.internal
  export GITLAB_TOKEN=glpat-...
  python3 duo_chat_runner.py --pack ../sample-app/docs/context-pack-v1 --out results-v1.md
  # repeat per variant, then score the transcripts per validation-plan.md Stage 2

If aiAction is rejected on your instance, use the manual protocol in validation-plan.md.
"""

import argparse
import os
import sys
import time
from pathlib import Path

import requests

QUESTIONS = [
    "What does this service do and what are its main flows?",
    "List all REST endpoints with their purpose.",
    # Adapt the bracketed questions to the sample app, then keep identical across variants:
    "Where is [chosen endpoint] implemented and what is its response shape?",
    "How do I add a new field to [chosen entity], including the migration?",
    "What is the error response format and which class produces it?",
    "Which existing utility should I reuse to [something CONVENTIONS covers]?",
    "How do I run only the integration tests?",
    "What are the riskiest parts of this codebase I should be careful with?",
]

AI_ACTION = """
mutation($content: String!) {
  aiAction(input: { chat: { content: $content } }) {
    requestId
    errors
  }
}
"""

# Duo Chat responses are asynchronous; poll the message history for our requestId.
AI_MESSAGES = """
query($requestIds: [ID!]) {
  aiMessages(requestIds: $requestIds) {
    nodes { requestId role content errors }
  }
}
"""


def gql(session, url, query, variables):
    r = session.post(f"{url}/api/graphql", json={"query": query, "variables": variables}, timeout=60)
    r.raise_for_status()
    body = r.json()
    if body.get("errors"):
        raise RuntimeError(f"GraphQL errors: {body['errors']}")
    return body["data"]


def ask(session, url, content, timeout_s=120):
    data = gql(session, url, AI_ACTION, {"content": content})
    action = data["aiAction"]
    if action["errors"]:
        raise RuntimeError(f"aiAction errors: {action['errors']}")
    request_id = action["requestId"]

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(3)
        data = gql(session, url, AI_MESSAGES, {"requestIds": [request_id]})
        for node in data["aiMessages"]["nodes"]:
            if node["role"].lower() == "assistant" and node["content"]:
                return node["content"]
    raise TimeoutError(f"No Duo response for requestId {request_id} within {timeout_s}s")


def load_pack(pack_dir):
    files = sorted(Path(pack_dir).glob("*.md"))
    if not files:
        sys.exit(f"No .md files found in {pack_dir}")
    parts = [f"===== {f.name} =====\n{f.read_text(encoding='utf-8')}" for f in files]
    return "\n\n".join(parts), [f.name for f in files]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pack", required=True, help="Path to a context-pack-vN directory")
    ap.add_argument("--out", required=True, help="Markdown transcript output file")
    args = ap.parse_args()

    url = os.environ.get("GITLAB_URL", "").rstrip("/")
    token = os.environ.get("GITLAB_TOKEN", "")
    if not url or not token:
        sys.exit("Set GITLAB_URL and GITLAB_TOKEN environment variables.")

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"

    pack_text, file_names = load_pack(args.pack)
    print(f"Loaded pack ({len(file_names)} files, ~{len(pack_text) // 4} tokens): {', '.join(file_names)}")

    transcript = [f"# Duo validation transcript — {args.pack}\n"]

    primer = (
        "The following files describe a Spring Boot microservice. Treat them as your source "
        "of truth about this codebase and follow any AI-WORKFLOW instructions they contain. "
        "Reply only 'Context loaded.' for now.\n\n" + pack_text
    )
    print("Sending pack as primer message...")
    reply = ask(session, url, primer)
    transcript.append(f"## Primer\n\n> Context inlined ({len(file_names)} files)\n\n**Duo:** {reply}\n")

    for i, q in enumerate(QUESTIONS, 1):
        print(f"Q{i}: {q}")
        reply = ask(session, url, q)
        transcript.append(f"## Q{i}: {q}\n\n**Duo:** {reply}\n")

    Path(args.out).write_text("\n".join(transcript), encoding="utf-8")
    print(f"Wrote transcript to {args.out} — score it per validation-plan.md Stage 2.")


if __name__ == "__main__":
    main()
