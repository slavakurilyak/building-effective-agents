from typing import List, Dict
import time

from pydanticai_agents.models.db_models import LeadRecord, MessageRecord

class DBClient:
    """
    A simple in-memory DB client to store leads and messages.
    In production, you'd implement real SQLite or libSQL integration.
    """
    def __init__(self):
        self.leads: Dict[str, LeadRecord] = {}
        self.messages: List[MessageRecord] = []

    def store_lead(self, lead: LeadRecord):
        self.leads[lead.twitter_handle] = lead

    def store_message(self, message: MessageRecord):
        self.messages.append(message)

    def update_lead_last_message_sent(self, twitter_handle: str):
        if twitter_handle in self.leads:
            self.leads[twitter_handle].last_message_sent = time.strftime("%Y-%m-%d %H:%M:%S")

    def update_lead_replied(self, twitter_handle: str):
        if twitter_handle in self.leads:
            self.leads[twitter_handle].replied = True

    def get_all_leads(self) -> List[LeadRecord]:
        return list(self.leads.values())

    def get_all_messages(self) -> List[MessageRecord]:
        return self.messages
