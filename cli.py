from pathlib import Path

import fire
import subprocess

import json


class Crawler:
    """Crawler to get emails from pixnet's comments"""

    scraped_ret_file = 'out/scraped.json'
    emails_file = 'out/emails.txt'
    errors_file = 'out/errors.json'

    def get(self, url=None, start=0):
        s_path = Path(self.scraped_ret_file)
        if s_path.is_file():
            print("Clean up {}".format(s_path))
            s_path.unlink()

        print("Start scraping...")
        cmd = ['scrapy', 'runspider', '--nolog', 'spider.py', '-o', self.scraped_ret_file]
        if url:
            cmd += ['-a', 'url={}'.format(url)]
        subprocess.call(cmd)
        print("Finish scraping.")

        with s_path.open() as f:
            data = json.load(f)

            if start:
                data = list(filter(lambda x: x['floor']> start, data))

            emails = [d['email'] for d in data if d['email']]
            errors = [d for d in data if not d['email']]

        print("Filter scraped data...")
        e_path = Path(self.emails_file)
        with e_path.open('w') as f:
            for e in emails:
                f.write(e + '\n')

        print("Export errors...")
        err_path = Path(self.errors_file)
        with err_path.open('w') as f:
            json.dump(errors, f, indent=2, ensure_ascii=False)

        print("All done.")


if __name__ == '__main__':
    fire.Fire(Crawler)