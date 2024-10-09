
from ..models.match_format import MatchFormat



def get_match_formats_list():
    match_format = MatchFormat.query.filter_by(status=1).all()
    return [format_item.type.lower() for format_item in match_format]
