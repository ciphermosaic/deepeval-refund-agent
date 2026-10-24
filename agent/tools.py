from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s "
)

@tool
def get_user_purchase_history(user: str) -> dict:
    """this tool takes the user username and return a dict of the user purchase history if
    the user exists"""
    logging.info(f"using get_user_purchase_history tool on user: {user}")
    if users_data.get(user):
        return users_data[user]
    return {"status": "there was no username found"}

@tool
def calculate_right_refund(user:str, items:list[PurchaseItem])-> str:
    """this tool takes a list of the items to be returned and the username and
    will return how much the refund is worth"""

    logging.info(f"using calculate_right_refund tool to get user's: {user} refund")

    if users_data.get(user):

        total_refund = 0

        for item in items:
            if users_data[user].get(item.name):
                total_refund += users_data[user][item.name]["price"]

        return f"the value of the refund is: {total_refund}"

    return {"status": "there was no username found"}

@tool
def issue_refund_ticket(user:str, refund_amount: int) -> str:
    """this tool will send a ticket to the right team to return the refund"""

    logging.info(f"using issue_refund_ticket for user: {user}")
    return f"a refund ticket has been issued successfully with the amount of {refund_amount}"

@tool
def get_today_date() -> str:
    """Return today's date in YYYY-MM-DD format
    This tool takes no arguments
    only use if a user exist and an item is present for refund"""
    logging.info(f"using the date tool")
    return date.today().isoformat()

# print(get_user_purchase_history.invoke("user123"))
# book = PurchaseItem(name="book")
# pen = PurchaseItem(name="pen")
# print(calculate_right_refund.invoke({"user":"user123",
#                                     "items":[book,pen]}))
# print(issue_refund_ticket.invoke({"user":"user123",  "refund_amount":30}))
# print(get_today_date.invoke("user123"))