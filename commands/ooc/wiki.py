import re
from django.db.models import Q
# inherit from your game's base command class
from commands.command import MuxCommand
from wiki.models import Article

_RE_WIKILINKS = re.compile(r'\[\[(.*)\]\]')
_RE_MDLINKS = re.compile(r'\[([^\[\]]+?)\]\(([^\)]+?)\)')


class CmdWiki(MuxCommand):
    """
    Read an article from the wiki

    Usage:
      wiki <text>

    The command will search for articles on the game's wiki where the title or content
    contain the entered text.

    Example:
      wiki getting started
    """

    key = "wiki"
    locks = "cmd:all()"

    def func(self):
        """Main command func"""
        self.args = self.args.strip()

        if not self.args:
            self.msg("Read which wiki page?")
            return

        if res := self.search_article(self.args):
            title, text = res
            self.msg(f"{title}\n\n{text}")

    def search_article(self, search_term):
        """
        Access function for searching for an article.

        Args:
          search_term (str) -  the text to search for

        Returns:
          (title, text) or None
        """
        results = self._build_query(search_term)

        return self.handle_results(results)

    def _build_query(self, search_term):
        """
        Builds a queryset based on the search arg

        Args:
          search_term (str) -  the string to look up

        Returns:
          articles (QuerySet)
        """
        # TODO: filter by read permissions?

        # check exact title match first
        if articles := Article.objects.filter(
            Q(current_revision__title__iexact=search_term)
        ):
            return articles

        # then, check by title
        if articles := Article.objects.filter(
            Q(current_revision__title__icontains=search_term)
        ):
            return articles

        # then and only then, check by contents
        articles = Article.objects.filter(
            Q(current_revision__content__icontains=search_term)
        )

        # this result gets handed back regardless of whether it's empty or not
        return articles

    def handle_results(self, results):
        """
        Handles the query set of matched articles, including error messaging.

        Args:
            results (QuerySet) -  The Articles which matched the input.

        Returns:
            (title, text) or None
        """
        match len(results):
            case 0:
                return self._no_matches()
            case 1:
                res = results[0]
                title = self.format_title(str(res))
                text = self.format_content(res)
                return (title, text)
            case _:
                return self._multiple_matches(results)

    def format_title(self, title):
        """Format the title text"""
        return f"# {title}"

    def format_content(self, article):
        """Format the article content text."""
        text = article.current_revision.content
        return self._parse_links(text)

    def _parse_links(self, text):
        """Replaces wikilinks with clickable wiki commands"""
        text = _RE_WIKILINKS.sub(r'\|lc\1\|lt\1\|le', text)
        text = _RE_MDLINKS.sub(r'\|lu\2\|lt\1\|le', text)

        return text

    def _no_matches(self):
        """Command feedback for no matches"""
        self.msg(f"There are no wiki pages matching '{self.args}'.")

    def _multiple_matches(self, results):
        """
        Command feedback for multiple matches

        Messages a list of matches, up to the top 5
        """
        article_list = []
        for res in results[:5]:
            name = str(res)
            name = f"- |lcwiki {name}|lt{name}|le"
            article_list.append(name)

        self.msg(f"Multiple articles match '{self.args}':\n" + "\n".join(article_list))
