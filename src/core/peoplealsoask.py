import people_also_ask
from tests.test_openai import Openai
from typing import List, Any
import json


class PeopleAlsoAsk:

    def __init__(self, question: str):
        self.question: str = question
        self.questions: List[str] = PeopleAlsoAsk._people_also_ask(self.question)
        self.answers: List[str] = []

    @staticmethod
    def _people_also_ask(question: str) -> Any:
        return people_also_ask.get_related_questions(question, 3)

    @property
    def to_schema_markup(self) -> str:
        openai = Openai()
        content_schema = '<div class="faq-container"><h2>Häufig gestellte Fragen</h2><br>'
        for question in self.questions:
            self.answers.append(openai.make_request(question)['choices'][0]['text'].strip())
        schema_markup = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": []
        }
        for question, answer in zip(self.questions, self.answers):
            schema_markup["mainEntity"].append({  # type: ignore
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer
                }
            })
            content_schema += f'<h3>{question}</h3>'
            content_schema += f'<div class="faq-answer">{answer}</div>'
        finalized_schema = content_schema + '<div>' + '<script type=\"application/ld+json\">' + \
            str(json.dumps(schema_markup)) + '</script>'
        if len(self.question) == 0:
            return ""
        return finalized_schema
