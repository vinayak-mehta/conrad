# -*- coding: utf-8 -*-

LATEST = "2"

_v1 = {
    "name": {"type": "string", "minlength": 1, "required": True},
    "url": {"type": "string", "minlength": 1, "required": True},
    "city": {"type": "string", "minlength": 1, "required": True},
    "state": {"type": "string", "required": True, "nullable": True},
    "country": {"type": "string", "minlength": 1, "required": True},
    "cfp_open": {"type": "boolean", "required": True},
    "cfp_end_date": {"is_date": True, "type": "string", "required": True},
    "start_date": {"is_date": True, "type": "string", "required": True},
    "end_date": {"is_date": True, "type": "string", "required": True},
    "source": {"type": "string", "minlength": 1, "required": True},
    "tags": {"type": "list", "minlength": 1, "required": True},
    "kind": {"type": "string", "allowed": ["conference", "meetup"], "required": True},
    "by": {"type": "string", "allowed": ["human", "bot"], "required": True},
}

_v2 = {
    "name": {"type": "string", "minlength": 1, "required": True},
    "url": {"type": "string", "minlength": 1, "required": True},
    "city": {"type": "string", "required": True, "nullable": True},
    "state": {"type": "string", "required": True, "nullable": True},
    "country": {"type": "string", "required": True, "nullable": True},
    "location": {"type": "string", "required": True, "nullable": True},
    "cfp_open": {"type": "boolean", "required": True},
    "cfp_end_date": {"is_date": True, "type": "string", "required": True},
    "start_date": {"is_date": True, "type": "string", "required": True},
    "end_date": {"is_date": True, "type": "string", "required": True},
    "source": {"type": "string", "minlength": 1, "required": True},
    "tags": {"type": "list", "minlength": 1, "required": True},
    "kind": {"type": "string", "allowed": ["conference", "meetup"], "required": True},
    "by": {"type": "string", "allowed": ["human", "bot"], "required": True},
}
