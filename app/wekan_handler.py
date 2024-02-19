from wekan import WekanClient
from wekan.card import Card
from wekan.board import Board
from wekan.wekan_list import List
from wekan.swimlane import Swimlane
import os

WEKAN_BASE_URL = os.environ["WEKAN_BASE_URL"]
WEKAN_LOGIN = os.environ["WEKAN_LOGIN"]
WEKAN_PASSWORD = os.environ["WEKAN_PASSWORD"]

client = WekanClient(
    base_url=WEKAN_BASE_URL, username=WEKAN_LOGIN, password=WEKAN_PASSWORD
)

board: Board = client.list_boards(regex_filter="GRAD")[0]
swimlane: Swimlane = board.list_swimlanes()[0]

backlog_list: List = board.list_lists(regex_filter="BACKLOG")[0]
todo_list: List = board.list_lists(regex_filter="TO DO (dev.this.release)")[0]


def create_new_card(list: List, description="", title="") -> str:
    new_card: Card = list.add_card(
        title=title, swimlane=swimlane, description=description
    )
    return f"{client.base_url}/b/{board.id}/{board.slug}/{new_card.id}"  # url to the created card
