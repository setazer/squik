from urllib.parse import urlparse

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_mng import bot, send_message, send_chat_action
from lxml.cssselect import CSSSelector
from lxml import html
import requests

iqdb_url = "http://iqdb.org/?url={}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class IqdbResults:
    data = None

    def __init__(self, raw_data):
        self.data = self._parse_results(raw_data)

    def _parse_results(self, raw_data):
        retval = []
        el_pages = CSSSelector('div.pages')(html.fromstring(raw_data))
        for page in el_pages:
            results = CSSSelector('table')(page)
            retval.extend(IqdbResult(item) for item in results)
        return retval

    def as_button_data(self):
        return [{'text': f"{item.similarity}% {iqdb_services.get(urlparse(url).netloc, 'Unknown')}", 'url': url}
                for item in self.data for url in item.service_urls]

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]


class IqdbResult:
    description = None
    image_url = None
    service_urls = None
    dimensions = None
    rating = None
    similarity = None
    source = False

    def __init__(self, el):
        self._parse(el)

    def _parse(self, el):
        result_headers = CSSSelector('th')(el)
        self.description = result_headers[0].text if result_headers else ""
        if self.description == 'Your image':
            self.source = True
            return
        links = CSSSelector('a')(el)
        self.service_urls = [link.attrib['href'] for link in links]
        for i, link in enumerate(self.service_urls[:]):
            if link.startswith('//'):
                self.service_urls[i] = f'https:{link}'
        body_el = CSSSelector('td')(el)
        self.image_url = CSSSelector('a')(body_el[0])[0][0].attrib['src']
        self.dimensions, self.rating = body_el[2].text[:-1].split(' [')
        self.similarity = int(body_el[3].text.replace('% similarity', ''))


def gen_iqdb_markup(results: IqdbResults):
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(**item) for item in results.as_button_data()]
    markup.row_width = 2
    markup.add(*buttons)
    return markup


@bot.callback_query_handler(lambda call: call.data.startswith('iqdb:'))
def iqdb_handler(call):
    url = call.data.replace('iqdb:', '', 1)
    bot.send_chat_action(call.message.chat.id,'upload_photo')
    req = requests.get(iqdb_url.format(url), headers=headers)
    parsed = IqdbResults(req.text)
    send_message(call.message.chat.id, "IQDB lookup results", reply_markup=gen_iqdb_markup(parsed))


iqdb_services = {'gelbooru.com': 'Gelbooru',
                 'danbooru.donmai.us': 'Danbooru',
                 'chan.sakakucomplex.com': 'Sankakucomplex',
                 'e-shuushuu.net': 'E-shuushuu',
                 'anime-pictures.net': 'Anime-pictures',
                 'yande.re': 'Yandere',
                 'www.zerochan.net': 'Zerochan',
                 'konachan.com': 'Konachan.com',
                 }