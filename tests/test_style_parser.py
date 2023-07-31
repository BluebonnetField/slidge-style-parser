from slidge_style_parser import format_body

MATRIX_FORMATS = {
    "_": ("<em>", "</em>"),
    "*": ("<strong>", "</strong>"),
    "~": ("<strike>", "</strike>"),
    "`": ("<code>", "</code>"),
    "```": ("<pre><code>", "</code></pre>"),
    ">": ("<blockquote>", "</blockquote>"),
    "||": ("<span data-mx-spoiler>", "</span>")
}

def test_basic():
    assert(format_body("_underline_", MATRIX_FORMATS) == "<em>underline</em>")
    assert(format_body("*bold*", MATRIX_FORMATS) == "<strong>bold</strong>")
    assert(format_body("~strikethrough~", MATRIX_FORMATS) == "<strike>strikethrough</strike>")
    assert(format_body("`code span`", MATRIX_FORMATS) == "<code>code span</code>")
    assert(format_body("```code\nblock```", MATRIX_FORMATS) == "<pre><code>code\nblock</code></pre>")
    assert(format_body("||spoiler||", MATRIX_FORMATS) == "<span data-mx-spoiler>spoiler</span>")

def test_quotes():
    assert(format_body(">single", MATRIX_FORMATS) == "<blockquote>single</blockquote>")
    assert(format_body(">single\n>grouped", MATRIX_FORMATS) == "<blockquote>single\ngrouped</blockquote>")
    assert(format_body(">>double", MATRIX_FORMATS) == "<blockquote><blockquote>double</blockquote></blockquote>")
    assert(format_body(">>double\n>grouped single", MATRIX_FORMATS) == "<blockquote><blockquote>double</blockquote>\ngrouped single</blockquote>")
    assert(format_body(">>>tripple\n>single\n>>double", MATRIX_FORMATS) == "<blockquote><blockquote><blockquote>tripple</blockquote></blockquote>\nsingle\n<blockquote>double</blockquote></blockquote>")

def test_escaped():
    assert(format_body("\\_no underline_", MATRIX_FORMATS) == "_no underline_")
    assert(format_body("\\\\_no underline_", MATRIX_FORMATS) == "\\_no underline_")
    assert(format_body(">>>tripple\n\\>none\n>>double", MATRIX_FORMATS) == "<blockquote><blockquote><blockquote>tripple</blockquote></blockquote></blockquote>\n>none\n<blockquote><blockquote>double</blockquote></blockquote>")

def test_nested():
    assert(format_body("`*~_code span_~*`", MATRIX_FORMATS) == "<code>*~_code span_~*</code>")
    assert(format_body("*_~`code span`~_*", MATRIX_FORMATS) == "<strong><em><strike><code>code span</code></strike></em></strong>")
    assert(format_body(">*_~`code span`~_*", MATRIX_FORMATS) == "<blockquote><strong><em><strike><code>code span</code></strike></em></strong></blockquote>")
    assert(format_body("*bold star >*< star bold*", MATRIX_FORMATS) == "<strong>bold star >*< star bold</strong>")
    assert(format_body("*_bold*_", MATRIX_FORMATS) == "<strong>_bold</strong>_")
    assert(format_body("__underlined__", MATRIX_FORMATS) == "<em><em>underlined</em></em>")

def test_no_changes():
    assert(format_body("", MATRIX_FORMATS) == "")
    assert(format_body("~~ empty `````` styles **", MATRIX_FORMATS) == "~~ empty `````` styles **")
    assert(format_body("this is not an empty string", MATRIX_FORMATS) == "this is not an empty string")
    assert(format_body("arrow ->", MATRIX_FORMATS) == "arrow ->")
    assert(format_body("  > no quote", MATRIX_FORMATS) == "  > no quote")
    assert(format_body("_not underlined", MATRIX_FORMATS) == "_not underlined")
    assert(format_body("|not a spoiler|", MATRIX_FORMATS) == "|not a spoiler|")
    assert(format_body("`no code\nblock here`", MATRIX_FORMATS) == "`no code\nblock here`")

def test_assorted():
    assert(format_body("at the ```end```", MATRIX_FORMATS) == "at the <pre><code>end</code></pre>")
    assert(format_body("in the ~middle~ here", MATRIX_FORMATS) == "in the <strike>middle</strike> here")
    assert(format_body("_underline_ *bold* ~strikethrough~ >not quote ||spoiler||\n>quote\nnothing\nnothing\n>>>>another quote with ||~_*```four```*_~||", MATRIX_FORMATS) == "<em>underline</em> <strong>bold</strong> <strike>strikethrough</strike> >not quote <span data-mx-spoiler>spoiler</span>\n<blockquote>quote</blockquote>\nnothing\nnothing\n<blockquote><blockquote><blockquote><blockquote>another quote with <span data-mx-spoiler><strike><em><strong><pre><code>four</code></pre></strong></em></strike></span></blockquote></blockquote></blockquote></blockquote>")

def test_weird_utf8():
    assert(format_body("❤️💓💕💖💗 ```💙💚💛💜🖤``` 💝💞💟❣️", MATRIX_FORMATS) == "❤️💓💕💖💗 <pre><code>💙💚💛💜🖤</code></pre> 💝💞💟❣️")
    assert(format_body("👨‍👩‍👧‍👧 _underline_👩‍👩‍👦‍👧", MATRIX_FORMATS) == "👨‍👩‍👧‍👧 <em>underline</em>👩‍👩‍👦‍👧")
    assert(format_body("\u202eRight to left", MATRIX_FORMATS) == "\u202eRight to left")
    assert(format_body(">\u202eRight to left quote?", MATRIX_FORMATS) == "<blockquote>\u202eRight to left quote?</blockquote>")
    assert(format_body("_Invisible\u200bseparator_", MATRIX_FORMATS) == "<em>Invisible\u200bseparator</em>")
    assert(format_body("~\u200b~", MATRIX_FORMATS) == "<strike>\u200b</strike>")

LIMITED_FORMATS = {
    "_": ("<em>", "</em>"),
    "~": ("<strike>", "</strike>"),
    "`": ("<code>", "</code>"),
    "||": ("<span data-mx-spoiler>", "</span>")
}

def test_limited():
    assert(format_body("_underline_ *bold* ~strikethrough~ >not quote ||spoiler||\n>quote\nnothing\nnothing\n>>>>another quote with ||~_*```four```*_~||", LIMITED_FORMATS) == "<em>underline</em> *bold* <strike>strikethrough</strike> >not quote <span data-mx-spoiler>spoiler</span>\n>quote\nnothing\nnothing\n>>>>another quote with <span data-mx-spoiler><strike><em>*```four```*</em></strike></span>")
