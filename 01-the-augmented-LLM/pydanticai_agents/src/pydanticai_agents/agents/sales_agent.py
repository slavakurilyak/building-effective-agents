from .base_agent import Agent, RunContext, ModelRetry
from pydantic_ai.result import RunResult

from dataclasses import dataclass
from typing import Dict, List, Optional

from ..clients.db_client import DBClient
from pydanticai_agents.tools.twitter_tools import (
    search_prospects_twitter,
    send_dm_twitter,
    check_inbox_twitter
)
from ..models.db_models import LeadRecord, MessageRecord

@dataclass
class SalesDependencies:
    """
    Dependencies needed by the Sales Agent.
    This includes an ICP filter definition and a DB client for storing leads, messages, etc.
    """
    icp_filters: Dict[str, str]
    db: DBClient

def add_icp_info(ctx: RunContext[SalesDependencies]) -> str:
    """
    A dynamic system prompt or utility to clarify the ICP filter.
    Returns a string that can be used in a system prompt or for logging.
    """
    filters_str = ', '.join(f"{k}={v}" for k, v in ctx.deps.icp_filters.items())
    return f"The ICP filters are: {filters_str}"

SalesAgent = Agent[SalesDependencies, str](
    model="openai:gpt-3.5-turbo",
    base_system_prompt=(
        "You are a sales agent. You will identify leads on Twitter that match the provided ICP filters, "
        "send them a helpful DM, and watch for responses. "
        "Only send one initial DM, do not continue messaging if the user responds (positive or negative)."
    ),
    deps_type=SalesDependencies,
    result_type=str,
)

@SalesAgent.system_prompt
def include_icp_details(ctx: RunContext[SalesDependencies]) -> str:
    """
    Add dynamic system prompt info about the ICP.
    """
    return add_icp_info(ctx)

@SalesAgent.tool
def find_leads(ctx: RunContext[SalesDependencies], count: int) -> List[LeadRecord]:
    """
    Calls Twitter to search for prospects based on ICP filters, up to 'count' leads,
    then stores them in the DB. Returns the leads for reference.
    """
    found = search_prospects_twitter(ctx.deps.icp_filters, max_results=count)
    leads = []
    for prospect in found:
        lead = LeadRecord(
            twitter_handle=prospect['twitter_handle'],
            bio=prospect['bio'],
            followers=prospect['followers'],
            icp_match=prospect['icp_match'],
            last_message_sent=None,
            replied=False
        )
        # Store in DB
        ctx.deps.db.store_lead(lead)
        leads.append(lead)
    return leads

@SalesAgent.tool
def outreach_lead(ctx: RunContext[SalesDependencies], twitter_handle: str, message: str) -> bool:
    """
    Sends a DM to the given twitter_handle with the provided message.
    Logs it in the DB as an outbound message. Returns True if successful.
    """
    success = send_dm_twitter(twitter_handle, message)
    if success:
        msg_rec = MessageRecord(
            twitter_handle=twitter_handle,
            direction="outbound",
            content=message
        )
        ctx.deps.db.store_message(msg_rec)
        ctx.deps.db.update_lead_last_message_sent(twitter_handle)
    return success

@SalesAgent.tool
def check_responses(ctx: RunContext[SalesDependencies]) -> List[MessageRecord]:
    """
    Checks the inbox for new responses, stores them in the DB, sets 'replied' for the relevant lead,
    and returns the list of inbound messages.
    """
    inbound = check_inbox_twitter()
    messages = []
    for msg in inbound:
        msg_rec = MessageRecord(
            twitter_handle=msg['sender_handle'],
            direction="inbound",
            content=msg['text']
        )
        ctx.deps.db.store_message(msg_rec)
        ctx.deps.db.update_lead_replied(msg['sender_handle'])
        messages.append(msg_rec)
    return messages

@SalesAgent.result_validator
def ensure_output(ctx: RunContext[SalesDependencies], result: Optional[str]) -> str:
    """
    A basic validator that ensures we return a valid string result.
    If the model tries to provide empty or None, we could raise a ModelRetry,
    but let's just default to a message.
    """
    if not result or not isinstance(result, str):
        raise ModelRetry("The output must be a non-empty string. Try again.")
    return result