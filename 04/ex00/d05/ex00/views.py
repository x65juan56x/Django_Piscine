from django.shortcuts import render


def index(request):
    markdown_data = {
        "Headings": [
            "Use <code>#</code> to <code>######</code> for heading levels 1 to 6."
        ],
        "Emphasis": [
            "<em>Italic</em> with <code>*text*</code> or <code>_text_</code>.",
            "<strong>Bold</strong> with <code>**text**</code> or <code>__text__</code>."
        ],
        "Lists": [
            "Unordered: <code>- item</code>, <code>* item</code>, <code>+ item</code>.",
            "Ordered: <code>1. item</code>."
        ],
        "Links and Images": [
            "Link: <code>[label](https://example.com)</code>.",
            "Image: <code>![alt text](image_url)</code>."
        ],
        "Code": [
            "Inline code: <code>`print(\"hello\")`</code>.",
            "Code block: use triple backticks before and after the block."
        ],
        "Quotes": [
            "Blockquote: <code>&gt; quoted text</code>."
        ],
        "Horizontal Rule": [
            "Use <code>---</code>, <code>***</code> or <code>___</code>."
        ],
        "Tables": [
            "<pre>| Col A | Col B |\n|---|---|\n| A1 | B1 |</pre>"
        ],
        "Task Lists (GitHub flavored)": [
            "<pre>- [x] done\n- [ ] pending</pre>"
        ],
        "Escaping": [
            "Escape special characters with backslash, e.g. <code>\\*</code>."
        ]
    }
    return render(request, 'ex00/index.html', {'cheatsheet': markdown_data})
