from typing import IO, TypedDict

from bs4 import BeautifulSoup, Tag


class Test(TypedDict):
    code: str
    stdin: str
    stdout: str
    extra: str
    display: str


class RawQuestion(TypedDict):
    name: str
    type: str
    prompt: str
    preload: str
    answer: str
    globalextra: str
    tests: list[Test]


def parse(f: IO) -> list[RawQuestion]:
    soup = BeautifulSoup(f, "xml")
    return [
        parse_question(question)
        for question in soup.find_all("question", type="coderunner")
        if not question.find("name").text.strip().startswith("PROTOTYPE")
    ]


def parse_question(tag: Tag) -> RawQuestion:
    return {
        "name": tag.find("name").text.strip(),
        "type": tag.find("coderunnertype").text.strip(),
        "prompt": BeautifulSoup(
            tag.find("questiontext", format="html").text,
            "html.parser",
        ).text.strip(),
        "preload": tag.find("answerpreload").text.strip(),
        "answer": tag.find("answer").text.strip(),
        "globalextra": tag.find("globalextra").text.strip(),
        "tests": [parse_test(test) for test in tag.find_all("testcase")]
    }


def parse_test(tag: Tag) -> Test:
    return {
        "code": tag.find("testcode").text.strip(),
        "stdin": tag.find("stdin").text.strip(),
        "stdout": tag.find("expected").text.strip(),
        "extra": tag.find("extra").text.strip(),
        "display": tag.find("display").text.strip(),
    }
