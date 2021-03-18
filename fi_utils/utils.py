import json
import logging
import logging.handlers
import os
import re
import subprocess
import urllib.parse
import urllib.request
from contextlib import contextmanager
from typing import *

import requests
import sqlalchemy as sqla


def init_logger(logfile_path: str, **kwargs: Any) -> None:
    backupCount = kwargs.pop("backupCount", 20)
    format = kwargs.pop(
        "format",
        "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
    )
    level = kwargs.pop("level", logging.DEBUG)

    if not os.path.exists(logfile_path):
        logfile_dir = os.path.dirname(logfile_path)
        os.makedirs(logfile_dir, exist_ok=True)
        open(logfile_path, "w").close()
    else:
        handler = logging.handlers.RotatingFileHandler(
            logfile_path, backupCount=backupCount
        )
        handler.doRollover()

    logging.basicConfig(
        filename=logfile_path,
        format=format,
        level=level,
    )


def create_sqla_engine_str(
    username: str, password: str, host: str, port: str, database: Optional[str] = None
) -> sqla.engine.base.Engine:
    s = f"mysql+pymysql://{username}:{password}@{host}:{port}"
    s += f"/{database}" if database is not None else ""
    return s


def open_mysql_conn(mysql_config: dict) -> sqla.engine.Connection:
    engine_str = create_sqla_engine_str(
        username=mysql_config["username"],
        password=mysql_config["password"],
        host=mysql_config["host"],
        port=mysql_config["port"],
        database=mysql_config["database"],
    )
    engine = sqla.create_engine(
        engine_str, json_serializer=lambda x: json.dumps(x, default=str)
    )
    return engine.connect()


@contextmanager
def create_ssh_tunnel(
    db_host: str,
    db_port: str,
    ssh_username: str,
    ssh_host: str,
    ssh_port: str = "22",
    localport: str = "33306",
    key_path: str = "~/.ssh/id_rsa",
):
    """Generates a "smart" ssh tunnel to a given host,
    in our case a database host (this is arbitrary, however).
    "smart" in the sense that when used in conjunction with the
    "with" clause, the tunnel, and all child processes thereof,
    will gracefully close when exited.

    Args:
        db_host (str): remote host granted access by the ssh host.
        db_port (str): port of the above.
        ssh_username (str): username of the ssh host.
        ssh_host (str):  ssh host that is granted access to the db_host.
        localport (str): local port that is forwarded to the db_host.
        key_path (str): ssh key path.
    """
    open_session = [
        "ssh",
        ssh_host,
        "-p",
        ssh_port,
        "-M4fNi",
        key_path,
        "-S",
        "/tmp/session1",
        "-L",
        f"{localport}:{db_host}:{db_port}",
        "-l",
        ssh_username,
    ]

    close_session = ["ssh", "-S", "/tmp/session1", "-O", "exit", " "]

    tunnel = subprocess.Popen(open_session)
    tunnel.wait()

    yield tunnel

    subprocess.Popen(close_session)


def url_components(url: str) -> Dict[str, List[str]]:
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)


def update_url_params(url: str, params: dict) -> str:
    url_obj = urllib.parse.urlparse(url)
    params.update(urllib.parse.parse_qsl(url_obj.query))

    query = urllib.parse.urlencode(params)

    url_obj = urllib.parse.ParseResult(
        url_obj.scheme,
        url_obj.netloc,
        url_obj.path,
        url_obj.params,
        query,
        url_obj.fragment,
    )

    return url_obj.geturl()


def url_get_json(url: str) -> Optional[Any]:
    try:
        return requests.get(url).json()
    except Exception as e:
        print(f"Exception found: {e}")
        return None


def better_dumps(
    obj: Any, default: Callable[[Any], str] = lambda x: str(x)
) -> Optional[str]:
    if obj is None:
        return None
    elif isinstance(obj, (dict, list, tuple)):
        return json.dumps(obj, default=default)
    else:
        return str(obj)


def dict_update_nulls(
    dict1: dict,
    dict2: dict,
    pred: Optional[Callable[[Any, Any], bool]] = None,
) -> dict:
    if pred is None:
        pred = lambda key, value: dict1.get(key) is None
    dict1 = dict(dict1)

    for key, value in dict2.items():
        if pred(key, value):
            dict1[key] = value

    return dict1


def list_concat(
    in_list: List[List[Any]], pred: Optional[Callable[[List[Any]], bool]] = None
) -> List[Any]:
    if pred is None:
        pred = lambda x: True

    out_list: List[Any] = []
    for i in in_list:
        if pred(i):
            out_list += i

    return out_list


def concat_non_empty(in_list: List[List[Any]]):
    return list_concat(in_list, lambda x: len(x) > 0)


def get_multiple(d: dict, *keys: Iterable[str]) -> dict:
    return {key: d.get(key) for key in keys}


def normalize_whitespace(s: str) -> str:
    RE_WHITESPACE = re.compile("\s+")

    s = re.sub(RE_WHITESPACE, " ", s)
    return s.strip()


def quote_value(value: str, quote: str = "`") -> str:
    if re.match(re.compile(quote + "(.*)" + quote), value) is not None:
        return value
    else:
        return f"{quote}{value}{quote}"


def file_components(filepath: str) -> Tuple[str, str, str]:
    if os.path.isdir(filepath):
        return ("", filepath, "")
    else:
        dirpath = os.path.dirname(os.path.realpath(filepath))
        filename, ext = os.path.splitext(os.path.basename(filepath))
        return (dirpath, filename, ext)