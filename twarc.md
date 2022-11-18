#TWARC CLI commands and script order

Download full timeline using search (Academic API)
`twarc2 timeline --use-search "scholarslab" slab/tweets.jsonl`

Ingest tweets, output top-level thread/conversation ids into thread_ids.txt
`python3 baseline.py`

Download full conversations from thread IDs
`twarc2 conversations --archive --no-context-annotations slab/thread_ids.txt slab/toplevel_conversations.txt`