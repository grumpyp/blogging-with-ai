from tests.test_openai import Openai
from utils.configparser import parse_config
from typing import Any, Dict, List
import pypandoc


def clean_numerisch_geordnet(to_clean: str) -> Dict[str, str]:
    cleaned = {}
    for i in to_clean.split('\n'):
        print(i)
        try:
            cleaned[i.split(". ")[1]] = ""
        except Exception:
            pass
    return cleaned


def generate_html(contents: Dict[str, str]) -> Dict[str, str]:
    html = {}
    for n, (subtitle, content) in enumerate(contents.items()):
        if subtitle.startswith("https://"):
            html[f'<a href="{subtitle}" rel="nofollow">{subtitle}</a>'] = ""
        else:
            subtitle_html = pypandoc.convert_text(str(subtitle), 'html', format='md')
            content_html = pypandoc.convert_text(str(content), 'html', format='md')
            html[subtitle_html] = content_html
    return html


def blogpost_wordpress(contents: Dict[str, str]) -> str:
    blogpost = ""
    for subtitle, content in contents.items():
        blogpost += f"{subtitle}\n{content}\n"
    return blogpost


class AIBlogpost(Openai):
    def __init__(self, topic: str, api_key: str | None = None):
        super().__init__(api_key=api_key)
        self.topic = topic
        self.config = parse_config()
        self.token_usage: List[int] = []
        self.toc = self.generate_toc(prompt=f'Schreibe ein Inhaltsverzeichnis für einen AIBlogpost zum Thema '
                                            f'{self.topic} numerisch geordnet es sollte mindestens 15'
                                            f' Einträge lang sein')
        self.contents = self.generate_contents()
        self.sources = self.generate_sources()
        self.html_contents = generate_html(self.contents)
        self.html_sources = generate_html(self.sources)
        self.html_table = self.generate_html_table()
        self.merged_html: Dict[str, str] = {**self.html_table, **self.html_contents, **self.html_sources}
        self.meta_title = ""
        # not working yet
        self.meta_desc = ""

    def generate(self, prompt: str) -> Any:
        while True:
            response = self.make_request(prompt=prompt)
            if response.get('error', None) is not None:
                # print(f'OpenAI request was not successful: {response["error"]["message"]}')
                pass
            else:
                # print(f"OpenAI request: {prompt} was successful")
                self.token_usage.append(response['usage']['total_tokens'])
                return response['choices'][0]['text']

    @property
    def wordcount(self) -> int:
        blogpost_merged = blogpost_wordpress(self.merged_html)
        plain_blogpost = pypandoc.convert_text(blogpost_merged, 'plain', format='html')
        return len(plain_blogpost.replace("\n", "").split(" "))

    @property
    def token_costs(self) -> float:
        return (sum(self.token_usage) * 0.0200) / 1000

    def generate_toc(self, prompt: str) -> Dict[str, str]:
        request = self.generate(prompt=prompt)
        toc = clean_numerisch_geordnet(request)
        print("TOC generated, now generating contents")
        # toc = {'Die Geschichte von AI': '', 'Die Definition von AI': '', 'Die Vor- und Nachteile von AI': '',
        #        'Die Risiken von AI': '', 'Die ethischen Fragen von AI': '', 'Die politischen Fragen von AI': '',
        #        'Die wirtschaftlichen Fragen von AI': '', 'Die sozialen Fragen von AI': '',
        #        'Die künstliche Intelligenz in der Medizin': '', 'Die künstliche Intelligenz in der Bildung': '',
        #        'Die künstliche Intelligenz im Militär': '', 'Die künstliche Intelligenz in der Wissenschaft': '',
        #        'Die künstliche Intelligenz in der Gesellschaft': '', 'Die Zukunft von AI': '', 'Fazit': ''}
        return toc

    def generate_sources(self) -> Dict[str, str]:
        sources = self.generate(prompt=f'Nenne mir 10 Quellen zum Thema {self.topic}'
                                       f' numerisch geordnet nur Hyperlinks')
        return clean_numerisch_geordnet(sources)

    def generate_contents(self) -> Dict[str, str]:
        contents = {}
        for i in self.toc:
            contents[f"## {i}"] = self.generate(prompt=f'Schreibe eine Zusammenfassung zum Thema {i} für einen '
                                                       f'Blogartikel zum  Thema {self.topic}')
        print(contents)
        return contents

    def generate_html_table(self) -> Dict[str, str]:
        html_table = {"<h2>Informations-Tabelle</h2>":
                      self.generate(prompt=f"Erstelle eine HTML Tabelle zum Thema: {self.topic}").replace("\n", " ")}
        return html_table

    def __str__(self) -> str:
        return self.topic
