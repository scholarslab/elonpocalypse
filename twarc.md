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

5. Build reply conversation IDs for specified tweets .jsonl:

`python3 reply_contexts.py slab`

6. Download reply conversations with twarc:

`twarc2 conversations --archive --no-context-annotations slab/scholarslab_reply_thread_ids.txt slab/scholarslab_replycontexts.jsonl`

7. Build top-level quote-retweet ID query file:

`python3 qrt_threads.py slab`

8. Download top-level quote-retweets:

`twarc2 searches --combine-queries --archive --no-context-annotations slab/qrt/scholarslab_thread_ids.txt slab/qrt/scholarslab_qrt.jsonl`

9. Download followers and followings:

`twarc2 followers scholarslab slab/scholarslab/followers.jsonl; twarc2 following scholarslab slab/scholarslab/following.jsonl`

