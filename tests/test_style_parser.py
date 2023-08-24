from slidge_style_parser import format_body

MATRIX_FORMATS = {
    "_": ("<em>", "</em>"),
    "*": ("<strong>", "</strong>"),
    "~": ("<strike>", "</strike>"),
    "`": ("<code>", "</code>"),
    "```": ("<pre><code>", "</code></pre>"),
    "```language": ("<pre><code class=\"language-{}\">", "</code></pre>"),
    ">": ("<blockquote>", "</blockquote>"),
    "||": ("<span data-mx-spoiler>", "</span>"),
    "\n": ("<br>", "")
}

def test_basic():
    test = "_underline_"
    formatted_body = "<em>underline</em>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "*bold*"
    formatted_body = "<strong>bold</strong>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "~strikethrough~"
    formatted_body = "<strike>strikethrough</strike>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "`code span`"
    formatted_body = "<code>code span</code>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = """
    ```python
        def test_basic():
            test = "_underline_"
            formatted_body = "<em>underline</em>"
            assert(format_body(test, MATRIX_FORMATS) == formatted_body)
    ```
    """
    formatted_body = test = """<pre><code class="language-python">def test_basic():<br>        test = "_underline_"<br>        formatted_body = "<em>underline</em>"<br>        assert(format_body(test, MATRIX_FORMATS) == (test, formatted_body))</pre></code><br>"""
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "```\ncode block\n```"
    formatted_body = "<pre><code>code block</code></pre>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "||this message contains a spoiler||"
    formatted_body = "<span data-mx-spoiler>this message contains a spoiler</span>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

def test_quotes():
    test = ">single"
    formatted_body = "<blockquote>single</blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">single arrow ->"
    formatted_body = "<blockquote>single arrow -></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">single\n>grouped"
    formatted_body = "<blockquote>single<br>grouped</blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>double"
    formatted_body = "<blockquote><blockquote>double</blockquote></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>double\n>>double"
    formatted_body = "<blockquote><blockquote>double<br>double</blockquote></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>double\n&>not quote"
    formatted_body = "<blockquote><blockquote>double</blockquote></blockquote><br>&>not quote"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>double\n>grouped single"
    formatted_body = "<blockquote><blockquote>double</blockquote><br>grouped single</blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>>tripple\n>single\n>>double"
    formatted_body = "<blockquote><blockquote><blockquote>tripple</blockquote></blockquote><br>single<br><blockquote>double</blockquote></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

def test_code_blocks():
    test = "```\nhacker\ncode\n```"
    formatted_body = "<pre><code>hacker<br>code</code></pre>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "```python\nhacker code\n```"
    formatted_body = "<pre><code class=\"language-python\">hacker code</code></pre>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "```python\nhacker code\n```\nnormal text"
    formatted_body = "<pre><code class=\"language-python\">hacker code</code></pre><br>normal text"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">```java\n>why are you quoting a code block\n>```"
    formatted_body = "<blockquote><pre><code class=\"language-java\">why are you quoting a code block</code></pre></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>```\n>>double quote code block\n>single quote not in code block\nnormal text"
    formatted_body = "<blockquote><blockquote><pre><code>double quote code block</code></pre></blockquote><br>single quote not in code block</blockquote><br>normal text"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">```\n>please stop trying to break my parser ;-;"
    formatted_body = "<blockquote><pre><code>please stop trying to break my parser ;-;</code></pre></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>```\n>>>>double quote code block\n>single quote not in code block\nnormal text"
    formatted_body = "<blockquote><blockquote><pre><code>>>double quote code block</code></pre></blockquote><br>single quote not in code block</blockquote><br>normal text"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "_```_ignored\ninvalid code block\n```"
    formatted_body = "<em>```</em>ignored<br>invalid code block<br>```"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)


def test_escaped():
    test = "\\_no underline_"
    formatted_body = "_no underline_"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "\\\\_no underline_"
    formatted_body = "\\_no underline_"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">>>tripple\n\\>none\n>>double"
    formatted_body = "<blockquote><blockquote><blockquote>tripple</blockquote></blockquote></blockquote><br>>none<br><blockquote><blockquote>double</blockquote></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

def test_nested():
    test = "`*~_code span_~*`"
    formatted_body = "<code>*~_code span_~*</code>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "*_~`code span`~_*"
    formatted_body = "<strong><em><strike><code>code span</code></strike></em></strong>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">*_~`code span`~_*"
    formatted_body = "<blockquote><strong><em><strike><code>code span</code></strike></em></strong></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "*bold star >*< star bold*"
    formatted_body = "<strong>bold star >*< star bold</strong>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "*_bold*_"
    formatted_body = "<strong>_bold</strong>_"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "__underlined__"
    formatted_body = "<em><em>underlined</em></em>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

def test_no_changes():
    test = ""
    formatted_body = ""
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "~~ empty `````` styles **"
    formatted_body = "~~ empty `````` styles **"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "this is not an empty string"
    formatted_body = "this is not an empty string"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "arrow ->"
    formatted_body = "arrow ->"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = " > no quote"
    formatted_body = " > no quote"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "_not underlined"
    formatted_body = "_not underlined"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "|not a spoiler|"
    formatted_body = "|not a spoiler|"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "||\nalso\nnot\na\nspoiler||"
    formatted_body = "||<br>also<br>not<br>a<br>spoiler||"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "`no code\nblock here`"
    formatted_body = "`no code<br>block here`"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "invalid ```\ncode block\n```"
    formatted_body = "invalid ```<br>code block<br>```"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "```\ncode block\ninvalid```"
    formatted_body = "```<br>code block<br>invalid```"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "```\ncode block\n```invalid"
    formatted_body = "```<br>code block<br>```invalid"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

def test_assorted():
    test = "\n"
    formatted_body = "<br>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "at the ||end||"
    formatted_body = "at the <span data-mx-spoiler>end</span>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "in the ~middle~ here"
    formatted_body = "in the <strike>middle</strike> here"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "_underline_ *bold* ~strikethrough~ >not quote ||spoiler||\n>quote\nnothing\nnothing\n>>>>another quote with ||~_*```four```*_~||"
    formatted_body = "<em>underline</em> <strong>bold</strong> <strike>strikethrough</strike> >not quote <span data-mx-spoiler>spoiler</span><br><blockquote>quote</blockquote><br>nothing<br>nothing<br><blockquote><blockquote><blockquote><blockquote>another quote with <span data-mx-spoiler><strike><em><strong>```four```</strong></em></strike></span></blockquote></blockquote></blockquote></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">```\n>do be do be dooo ba do be do be do ba\n>>>"
    formatted_body = "<blockquote><pre><code>do be do be dooo ba do be do be do ba<br>>></code></pre></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "\n\n>```\n>do be do be dooo ba do be do be do ba\na\n\n\naoeu\n"
    formatted_body = "<br><br><blockquote><pre><code>do be do be dooo ba do be do be do ba</code></pre></blockquote><br>a<br><br><br>aoeu<br>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">```\n>do be do be dooo ba do be do be do ba\n>\n>\n>aoeu"
    formatted_body = "<blockquote><pre><code>do be do be dooo ba do be do be do ba<br><br><br>aoeu</code></pre></blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">```\n>code block\n>```invalid end\n"
    formatted_body = "<blockquote><pre><code>code block<br>```invalid end</code></pre></blockquote><br>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "invalid ```\ncode block\n*bold*\n```"
    formatted_body = "invalid ```<br>code block<br><strong>bold</strong><br>```"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

def test_weird_utf8():
    test = "❤️💓💕💖💗 ||💙💚💛💜🖤|| 💝💞💟❣️"
    formatted_body = "❤️💓💕💖💗 <span data-mx-spoiler>💙💚💛💜🖤</span> 💝💞💟❣️"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "👨‍👩‍👧‍👧 _underline_👩‍👩‍👦‍👧"
    formatted_body = "👨‍👩‍👧‍👧 <em>underline</em>👩‍👩‍👦‍👧"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "\u202eRight to left"
    formatted_body = "\u202eRight to left"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = ">\u202eRight to left quote?"
    formatted_body = "<blockquote>\u202eRight to left quote?</blockquote>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "_Invisible\u200bseparator_"
    formatted_body = "<em>Invisible\u200bseparator</em>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

    test = "~\u200b~"
    formatted_body = "<strike>\u200b</strike>"
    assert(format_body(test, MATRIX_FORMATS) == formatted_body)

LIMITED_FORMATS = {
    "_": ("<em>", "</em>"),
    "~": ("<strike>", "</strike>"),
    "`": ("<code>", "</code>")
}

def test_limited():
    test = "_underline_ *bold* ~strikethrough~ >not quote ||spoiler||\n>quote\nnothing\nnothing\n>>>>another quote with ||~_*```four```*_~||"
    formatted_body = "<em>underline</em> *bold* <strike>strikethrough</strike> >not quote ||spoiler||\n>quote\nnothing\nnothing\n>>>>another quote with ||<strike><em>*```four```*</em></strike>||"
    assert(format_body(test, LIMITED_FORMATS) == formatted_body)
