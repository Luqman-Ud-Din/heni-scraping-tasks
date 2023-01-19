def clean_text_list(text_list):
    _text = []
    for text in text_list:
        text = (text or '').strip()
        if text:
            _text.append(text)

    return _text


def get_first(lst):
    return next(iter(lst), None)
