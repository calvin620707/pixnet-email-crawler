import scrapy
import re


class EmailsSpider(scrapy.Spider):
    name = "emails"
    start_urls = [
        'http://pattydraw.pixnet.net/blog/post/274202089?comment_page=2'
    ]
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        prev_floor = 0

        for comment in response.css('ul.single-post'):
            if 'secret' in comment.root.classes:
                floor = prev_floor + 1
                prev_floor += 1
                yield self._result(floor, None, errors=['is secret'])
                continue

            prev_floor = floor = int(comment.css('li.post-info').css('span.floor::text').get()[1:])
            text_item = comment.css('li.post-text')
            email_domain = text_item.xpath('a/text()').get()
            raw_text = text_item.get()
            raw_text = raw_text.replace(' ', '')
            raw_text = raw_text.replace('\n', '')

            if email_domain:
                raw_text = re.sub(r'<atarget=.*</a>', '@' + email_domain, raw_text)

            email_ptn = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
            matched = email_ptn.search(raw_text)

            if not matched:
                yield self._result(floor, None, errors=['email not found'])
                continue

            yield self._result(floor, matched[0])

    def _result(self, floor, email, raw_text=None, errors=None):
        ret = {
            'floor': floor,
            'email': email
        }

        if raw_text:
            ret['text'] = raw_text

        if errors:
            ret['errors'] = errors

        return ret
