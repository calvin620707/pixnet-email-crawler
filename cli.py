from pathlib import Path

import fire
import subprocess

import json


class Crawler:
    """Crawler to get emails from pixnet's comments"""

    scraped_ret_file = 'out/scraped.json'
    emails_file = 'out/emails.txt'

    def get(self, start=0):
        r_path = Path(self.scraped_ret_file)
        if r_path.is_file():
            r_path.unlink()

        subprocess.call(['scrapy', 'runspider', '--nolog', 'spider.py', '-o', self.scraped_ret_file])

        with r_path.open() as f:
            data = json.load(f)

            if start:
                data = list(filter(lambda x: x['floor']> start, data))

            emails = [d['email'] for d in data if d['email']]

        e_path = Path(self.emails_file)
        with e_path.open('w') as f:
            for e in emails:
                f.write(e + '\n')

if __name__ == '__main__':
    fire.Fire(Crawler)