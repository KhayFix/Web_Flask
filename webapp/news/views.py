from flask import abort, Blueprint, current_app, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.news.forms import CommentForm
from webapp.news.models import Comment, News
from webapp.weather import weather_by_city
from webapp.utils import get_redirect_target

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
@blueprint.route('/home')
def index():
    title = "Новости Python"
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    page = request.args.get('page', 1, type=int)
    news = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).paginate(
        page, 7, False)

    # news = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()
    # часть кода отвечающая за отображения колличества новостей на странице
    next_url = url_for('news.index', page=news.next_num) \
        if news.has_next else None
    prev_url = url_for('news.index', page=news.prev_num) \
        if news.has_prev else None

    return render_template('news/index.html', page_title=title, weather=weather, news_lists=news,
                           next_url=next_url, prev_url=prev_url)


@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()

    if not my_news:
        abort(404)
    comment_form = CommentForm(news_id=my_news.id)
    return render_template('news/single_news.html', page_title=my_news.title,
                           news_lists=my_news, comment_form=comment_form)


@blueprint.route('/news/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment_text.data, news_id=form.news_id.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен!')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())
