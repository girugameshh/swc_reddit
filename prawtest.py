from flask import Flask, render_template, request
import praw

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    reddit = praw.Reddit(
        client_id="A6k4kNua82Sf779YcrDuEw",
        client_secret="2OqQsCBo3AFC0V7JuAlo8lHQ3BUQDQ",
        user_agent="windows:v1.0 (by /u/banozica)",
    )

    subreddit_name = request.args.get('subreddit', 'all')
    if subreddit_name == '':
        subreddit_name = 'all'

    subreddit = reddit.subreddit(subreddit_name)

    time_filter = request.args.get('time_filter', 'all')

    threads = []
    for submission in subreddit.top(limit=10, time_filter=time_filter):
        thread = {
            'title': submission.title,
            'score': submission.score,
            'num_comments': submission.num_comments,
            'subreddit': submission.subreddit.display_name,
            'url': submission.permalink,
        }
        threads.append(thread)

    sort_order = request.args.get('sort', 'score')
    threads.sort(key=lambda t: t[sort_order], reverse=True)

    return render_template('index.html', threads=threads, sort_order=sort_order)


if __name__ == '__main__':
    app.run(debug=True)
