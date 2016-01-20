#

def _extractString(tag):
    return tag.find(string=True)


def tengriNews(soap):
    paragraph_tags = soap\
                        .find('div', class_='text')\
                        .find_all('p', string=True, recursive=False, limit=3)
    paragraphs = map(_extractString, paragraph_tags)
    return {
        'source': 'Tengrinews.kz',
        'date_created': None,
        'title': soap.find('div', class_='data').h1.string,
        'body':  '\n'.join(paragraphs)
    }

def nurKz(soap):
    paragraph_tags = soap\
                        .find('div', class_='c__article_text')\
                        .find_all('p', string=True, recursive=False, limit=3)
    paragraphs = map(_extractString, paragraph_tags)

    raw_date = soap.find('div', class_='c__article_data').span.string
    return {
        'source': 'Nur.kz',
        'date_created': None,
        'title': soap.find('h1', class_='c__article_caption').string,
        'body':  '\n'.join(paragraphs)
    }

def default(soap):
    def getDescriptionUsingMeta():
        try:
            d = soap.find('meta', attrs={'name': 'description'}).get('content')
            if d:
                return d;
        except Exception as e:
            pass

        for s in ["twitter:description", "og:description"]:
            try:
                ret = soap.find('meta', attrs={'property': s}).get('content')
                if ret:
                    return ret
            except Exception as e:
                pass
        return None

    def getTitleUsingMeta():
        for s in ["twitter:title", "og:title"]:
            try:
                ret = soap.find('meta', attrs={'property': s}).get('content')
                if ret:
                    return ret
            except Exception as e:
                pass
        return None

    def getSourceUsingMeta():
        for s in ["al:ios:app_name", "al:android:app_name", "twitter:app:name:iphone", "og:site_name"]:
            try:
                ret = soap.find('meta', attrs={'property': s}).get('content')
                if ret is not None:
                    return ret
            except Exception as e:
                pass
        return None

    def getTitle():
        funcs = {
            'getFromTitleTag': lambda: soap.title.string,
            'getFromHeaderTags': lambda: soap.find(['h1', 'h2', 'h3', 'h4'], string=True).string,
            'getFromMeta': getTitleUsingMeta
        }
        for func_name, func in funcs.iteritems():
            try:
                title = func()
            except Exception as e:
                title = None
            if title is not None:
                return title
        return None

    def getDescriptionFromParagraphs():
        paragraph_tags = soap\
                            .find('p', string=True)\
                            .find_next_sibling('p', string=True)
        paragraphs = map(_extractString, paragraph_tags)
        return '\n'.join(paragraphs)

    def getDescription():
        funcs = {
            'getDescriptionUsingMeta': getDescriptionUsingMeta,
            'getFromParagraphs': getDescriptionFromParagraphs
        }
        for func_name, func in funcs.iteritems():
            try:
                title = func()
            except Exception as e:
                print e
                title = None
            if title is not None:
                return title
        return None


    return {
        'source': getSourceUsingMeta(),
        'date_created': None,
        'title': getTitle(),
        'body': getDescription()
    }
