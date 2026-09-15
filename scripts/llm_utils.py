import anthropic
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

# Client initialization
with open('secrets/anthropic_api_key.txt', 'r') as f:
    CLIENT = anthropic.Anthropic(api_key=f.read().strip())

# Model constants
MODEL_OPUS = 'claude-opus-5'
MODEL_SONNET = 'claude-sonnet-5'
MODEL_HAIKU = 'claude-haiku-4-5'

DEFAULT_MAX_TOKENS = 4000


@retry(wait=wait_random_exponential(min=10, max=120), stop=stop_after_attempt(10),
       retry=retry_if_exception_type(anthropic.RateLimitError))
def query_llm(messages, max_tokens=DEFAULT_MAX_TOKENS, model=MODEL_OPUS):
    """Query Anthropic API with retry logic. Messages can include role='system'."""
    system = None
    api_messages = []
    for msg in messages:
        if msg['role'] == 'system':
            system = msg['content']
        else:
            api_messages.append(msg)

    kwargs = dict(
        model=model,
        messages=api_messages,
        max_tokens=max_tokens,
    )
    # Adaptive thinking on current Opus/Sonnet; Haiku 4.5 does not support it.
    if model != MODEL_HAIKU:
        kwargs['thinking'] = {"type": "adaptive"}
        kwargs['output_config'] = {"effort": "medium"}
    if system:
        kwargs['system'] = system

    response = CLIENT.messages.create(**kwargs)
    return next(b.text for b in response.content if b.type == "text")


def query_llm_simple(system_prompt, user_input, max_tokens=DEFAULT_MAX_TOKENS,
                     model=MODEL_OPUS, debug_label=""):
    """Convenience wrapper: system + user string -> response text."""
    try:
        return query_llm([
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input},
        ], max_tokens=max_tokens, model=model)
    except Exception as e:
        if debug_label:
            print(f"ERROR in query_llm ({debug_label}): {type(e).__name__}: {e}")
        raise


_WEB_TOOLS = [
    {"type": "web_fetch_20260209", "name": "web_fetch", "allowed_callers": ["direct"]},
    {"type": "web_search_20260209", "name": "web_search", "max_uses": 3, "allowed_callers": ["direct"]},
]


@retry(wait=wait_random_exponential(min=10, max=120), stop=stop_after_attempt(10),
       retry=retry_if_exception_type(anthropic.RateLimitError))
def _web_fetch_loop(system_prompt, user_prompt, model=MODEL_OPUS, max_tokens=DEFAULT_MAX_TOKENS):
    """Run a web_fetch + web_search agent loop, handling pause_turn. Returns last text block."""
    messages = [{"role": "user", "content": user_prompt}]
    for turn in range(10):
        print(f'  web_fetch turn {turn + 1}, stop_reason: ...', end='')
        kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            tools=_WEB_TOOLS,
            messages=messages,
        )
        if model != MODEL_HAIKU:
            kwargs['thinking'] = {"type": "adaptive"}
            kwargs['output_config'] = {"effort": "medium"}
        response = CLIENT.messages.create(**kwargs)
        print(f'\r  web_fetch turn {turn + 1}, stop_reason: {response.stop_reason}, usage: {response.usage}')
        for block in response.content:
            if block.type == "text":
                print(f'  [text] {block.text[:200]}')
            elif block.type == "server_tool_use":
                print(f'  [tool_use] {block.name}({block.input})')
            elif block.type == "web_search_tool_result":
                print(f'  [web_fetch_result]')
        if response.stop_reason == "end_turn":
            break
        messages = [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response.content},
        ]
    text_blocks = [b.text for b in response.content if b.type == "text"]
    return "".join(text_blocks) if text_blocks else "Error: no text in response"


def web_fetch_summarize(url, system_prompt, title=None, model=MODEL_OPUS, max_tokens=DEFAULT_MAX_TOKENS):
    """Fallback for podcast: fetch URL and return bullet point summary.

    The title (from the CSV) is passed when available so the model can
    verify it has the right story and search for alternative sources by
    title if the original URL is blocked.
    """
    print('  newspaper download failed, falling back to web_fetch tool...')
    title_line = f"Story title: {title}\n" if title else ""
    user_prompt = (
        f"{title_line}URL: {url}\n\n"
        "Fetch the URL and summarize the story. If the URL is blocked, "
        "paywalled, or inaccessible, search for the story by title and fetch "
        "another reputable source covering the same story — but only use a "
        "source that is clearly about the same story as the title above.\n\n"
        "Tool-call budget: at most 4 fetches/searches.\n\n"
        "In your final message, output ONLY the bullet point summary in "
        "markdown, nothing else."
    )
    return _web_fetch_loop(system_prompt, user_prompt, model=model, max_tokens=max_tokens)


def web_fetch_article_summary(url, title=None, model=MODEL_OPUS):
    """Fallback for newsletter: return a detailed summary of the story at the URL.

    Used when direct article extraction fails (paywall, block, parse error). The
    summary is fed downstream to generate a one-sentence newsletter excerpt, so
    it must preserve concrete facts (names, numbers, dates, quotes) rather than
    a high-level overview. The title (from the CSV) is passed when available so
    the model can verify the right story and search by title if the URL is
    blocked.
    """
    print(f'  newspaper download failed for {url}, falling back to web_fetch tool...')
    system_prompt = (
        "You research news stories and produce detailed factual summaries. "
        "Preserve concrete details — names, organizations, numbers, dates, "
        "direct quotes, and specific claims — over high-level framing."
    )
    title_line = f"Story title: {title}\n" if title else ""
    user_prompt = (
        f"{title_line}URL: {url}\n\n"
        "Produce a detailed summary of this story. First try fetching the URL "
        "directly. If it's blocked, paywalled, or inaccessible, search for the "
        "story by title and fetch other reputable sources covering the same "
        "story — but only use a source that is clearly about the same story.\n\n"
        "Tool-call budget: at most 4 fetches/searches.\n\n"
        "In your final message, output ONLY the summary in plain prose "
        "(no headers, no bullet lists, no preamble). Begin with the story "
        "title on the first line, then a blank line, then the summary. "
        "Include all important specifics a reader would need to understand "
        "what happened — do not write a teaser or high-level overview.\n\n"
        "If you could not access any usable source, output exactly: "
        "'EXTRACTION_FAILED: <one-line reason>'."
    )
    return _web_fetch_loop(system_prompt, user_prompt, model=model, max_tokens=DEFAULT_MAX_TOKENS)
