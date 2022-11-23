#TWARC CLI commands and script order

Organize accounts by directory. Use Twarc to download timelines to <handle>.json. Limitations: account handles that end with "_conversations" or "_replycontexts" will confuse the baseline script.

1. Download full timeline using search if on Academic, otherwise omit "--use-search" parameter to download most recent ~3k tweets:

`twarc2 timeline --use-search "scholarslab" slab/scholarslab.jsonl`

2. Build top-level thread/conversation ids into thread_ids.txt from all TWARC tweet jsonls in specified directory:

`python3 toplevel_threads.py slab`

3. Download full conversations from thread_id produced from toplevel_threads.py:

`twarc2 conversations --archive --no-context-annotations slab/thread_ids.txt slab/toplevel_conversations.jsonl`

4. Download media for the specified tweets .jsonl (can run parallel to API rate-limited scripts):

`python3 media.py slab/scholarslab.jsonl`

5. Download reply contexts (upstream tweets to replies) for specified tweets .jsonl:

`python3 replycontexts.py slab/scholarslab.jsonl`