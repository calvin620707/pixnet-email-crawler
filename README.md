# Setup
Install required libraries.

`pip install -r requirements.txt`

# Usage
1. Run CLI

    `python cli.py get [start]`
    
    You can use `start` to filter email start from which floor.
    Example:
    If you want emails which started from #100 comment (exclude #100 comment), you can run `python cli.py 100` and `emails.txt` will only include emails after #100 comment. 

2. Check `out/emails.txt` for email address in comments.

3. Check `out/scraped.json` for errors. 