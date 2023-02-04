import click
import datetime
from core.generate_blogpost import AIBlogpost
from typing import List


@click.command()
@click.option('--release', help='Plan your release of the post e.g. "2022-12-30T00:00:00"',
              required=False, default=None)
@click.option('--categories', help='List of categories', required=False, multiple=True, default=[2])
@click.option('--tags', help='List of tags', required=False, multiple=True, default=[3])
@click.option('--sticky', help='Sticky post', required=False, default=False)
@click.option('--search_console', help='Send post to search console', is_flag=True)
@click.option('--picture', help="Search query for the picture at unsplash.com", required=False)
@click.option('--faq', help="Add FAQ's with Schema-Markup to blogpost", is_flag=True)
@click.argument('topic')
def create_blogpost(topic: str, categories: List[str], tags: List[str], sticky: bool,
                    release: datetime.datetime | None, search_console: bool, picture: str, faq: bool) -> None:
    """Simple CLI tool that uses AI (GPT-3) to generate a WordPress blogpost from a prompt."""
    from core.wordpress_controller import WordpressController, Blogpost
    from core.generate_blogpost import blogpost_wordpress
    from utils.google_search_console import GoogleSearchConsole
    from utils.temporary_file import Tempfile
    from core.unsplash import Unsplash
    from core.peoplealsoask import PeopleAlsoAsk
    from database.database import Database
    from database.models import Post

    ai_post = AIBlogpost(topic=topic)
    print(ai_post.contents)
    # print(ai_post.sources)
    print(ai_post.html_contents)
    status = 'publish' if release is None else 'future'
    date = datetime.datetime.now() if release is None else release
    # upload media
    wordpress = WordpressController()
    unsplash = Unsplash()
    picture_query = picture if picture else topic
    image_unsplash = unsplash.search_by_keyword(picture_query)
    if image_unsplash is not None:
        tempfile = Tempfile(image_unsplash['photo_url'])
        image_id_wordpress = wordpress.upload_media(image_path=tempfile.file.name, title=picture_query,
                                                    caption=picture_query, alt_text=picture_query)
        tempfile.delete()
    post = Blogpost(content=blogpost_wordpress(ai_post.merged_html), categories=categories,  # type: ignore
                    tags=tags, date=release,    # type: ignore
                    status=status, sticky=sticky, title=ai_post.topic,
                    meta={'_yoast_wpseo_metadesc': ai_post.meta_desc,
                          '_yoast_wpseo_title': ai_post.meta_title},
                    featured_media=image_id_wordpress if image_unsplash is not None else None)
    if faq:
        paa = PeopleAlsoAsk(topic)
        post.content = post.content + paa.to_schema_markup  # type: ignore
    wordpress.create_post(blogpost=post)
    if search_console:
        console = GoogleSearchConsole(to_index_url=wordpress.get_all_posts()[0]['link'])
        console.send_index_request()
    if release is None:
        release = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  # type: ignore # noqa
    db = Database()
    db.add(Post(title=ai_post.topic, content=blogpost_wordpress(ai_post.merged_html),
                release=datetime.datetime.strptime(str(release), "%Y-%m-%dT%H:%M:%S"),
                generated=datetime.datetime.now(), wordcount=ai_post.wordcount, costs_in_dollar=ai_post.token_costs))

    click.echo(f'A post about {topic} will be drafted and released at {date}')


if __name__ == '__main__':
    create_blogpost()
