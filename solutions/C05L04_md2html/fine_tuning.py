import json

data = [
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "# Nagłówek1 "},
            {"role": "assistant", "content": "<h1>Nagłówek1</h1>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "## Nagłówek2 "},
            {"role": "assistant", "content": "<h2>Nagłówek1</h2>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "### Nagłówek3 "},
            {"role": "assistant", "content": "<h3>Nagłówek1</h3>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "**pogrubienie**"},
            {"role": "assistant", "content": '<span class="bold">pogrubienie</span>'},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_podkreślenie_"},
            {"role": "assistant", "content": "<u>podkreślenie</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_coś poszło nie tak_"},
            {"role": "assistant", "content": "<u>coś poszło nie tak</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_przykład za przykładem_"},
            {"role": "assistant", "content": "<u>przykład za przykładem</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_Co jeszcze mi powiesz?_"},
            {"role": "assistant", "content": "<u>Co jeszcze mi powiesz?</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_zwykle wystarczą trzy przykłady_"},
            {"role": "assistant", "content": "<u>zwykle wystarczą trzy przykłady</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_warto_"},
            {"role": "assistant", "content": "<u>warto</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_Oszczędzasz na cukrze_"},
            {"role": "assistant", "content": "<u>Oszczędzasz na cukrze</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_asdasdadas_"},
            {"role": "assistant", "content": "<u>asdasdadas</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_test_"},
            {"role": "assistant", "content": "<u>test</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_to zdanie będzie dłuższe_"},
            {"role": "assistant", "content": "<u>to zdanie będzie dłuższe</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_a to nie_"},
            {"role": "assistant", "content": "<u>a to nie</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "_wygenerujmy jeszcze kilka_"},
            {"role": "assistant", "content": "<u>wygenerujmy jeszcze kilka</u>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "*kursywa*"},
            {"role": "assistant", "content": "<em>kursywa</em>"},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "[AI Devs 3.0](https://aidevs.pl)"},
            {
                "role": "assistant",
                "content": '<a href="https://aidevs.pl">AI Devs 3.0</a>',
            },
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "1. Element listy\n2. Kolejny elementy"},
            {
                "role": "assistant",
                "content": "<ol>\n<li>Element listy</li>\n<li>Kolejny elementy</li>\n</ol>",
            },
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {
                "role": "user",
                "content": "# Machine Learning **Topics to Cover** *Supervised Learning* *Unsupervised Learning* [More Info](https://en.wikipedia.org/wiki/Machine_learning)",
            },
            {
                "role": "assistant",
                "content": '<h1>Machine Learning</h1> <span class="bold">Topics to Cover</span> <em>Supervised Learning</em> <em>Unsupervised Learning</em> <a href="https://en.wikipedia.org/wiki/Machine_learning">More Info</a>',
            },
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {
                "role": "user",
                "content": "# Contact Us **Email:** info@example.com *Phone:* 123-456-7890 [Website](http://example.com)",
            },
            {
                "role": "assistant",
                "content": '<h1>Contact Us</h1> <span class="bold">Email:</span> info@example.com <em>Phone:</em> 123-456-7890 <a href="http://example.com">Website</a>',
            },
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "**Witaj świecie**"},
            {"role": "assistant", "content": '<span class="bold">Witaj świecie</span>'},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "**Dzień dobry kocham Cię**"},
            {
                "role": "assistant",
                "content": '<span class="bold">Dzień dobry kocham Cię</span>',
            },
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "**Witam witam o zdrowie pytam**"},
            {
                "role": "assistant",
                "content": '<span class="bold">Witam witam o zdrowie pytam</span>',
            },
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "**Jak się masz**"},
            {"role": "assistant", "content": '<span class="bold">Jak się masz</span>'},
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "**Czy jest termin do doktora?**"},
            {
                "role": "assistant",
                "content": '<span class="bold">Czy jest termin do doktora?</span>',
            },
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "As an assistant you convert markdown to HTML. You pay attention to specific way of formatting bolding.",
            },
            {"role": "user", "content": "**Cześć**"},
            {"role": "assistant", "content": '<span class="bold">Cześć</span>'},
        ]
    },
]

with open("solutions/C05L04_md2html/data_set.jsonl", "w") as f:
    for item in data:
        json.dump(item, f)
        f.write("\n")
