import json
import datetime


class CDEKSerializable:
    @property
    def fields(self):
        return self.__dict__


class CDEKEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, CDEKSerializable):
            return self._filter_none(o.fields)
        elif isinstance(o, datetime):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, list):
            if len(o) == 0:
                return ''
        elif o is None:
            return ''
        return super(CDEKEncoder, self).default(o)

    def encode(self, o):
        return super(CDEKEncoder, self).encode(o)

    def _filter_none(self, value: dict):
        return dict(filter(lambda x: x[1] is not None, value.items()))