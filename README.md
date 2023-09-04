[Github](https://github.com/BluebonnetField/slidge-style-parser)

[PyPi](https://pypi.org/project/slidge-style-parser/)

A parsing library for [Slidge](https://sr.ht/~nicoco/slidge). Supports parsing these attributes:

"\_underline_"

"\*bold*"

"\~strikethrough~"

"\`code span`"

"\```language

code block

\```"

"\>quote"

"\|\|spoiler||"

"\\\_escape style_"

Most of them correspond to [XEP-0393: Message Styling](https://xmpp.org/extensions/xep-0393.html).

Methods: 


format_for_telegram(body: String) -> (body: String, Vec<(format: String, offset: usize, length: usize, language: String)>)

format_for_matrix(body: String) -> body: String

format_body(body: String, new_tags: HashMap<String, (String, String)>) -> String

new_tags = {

    "_": ("<em>", "</em>"),
    
    "*": ("<strong>", "</strong>"),
    
    "~": ("<del>", "</del>"),
    
    "`": ("<code>", "</code>"),
    
    "```": ("<pre><code>", "</code></pre>"),
    
    "```language": ('<pre><code class="language-{}">', "</code></pre>"),
    
    ">": ("<blockquote>", "</blockquote>"),
    
    "||": ("<span data-mx-spoiler>", "</span>"),
    
    "\n": ("<br>", "")

}
