import argparse

from .agents.sales_agent import SalesAgent, SalesDependencies
from .clients.db_client import DBClient

def main():
    parser = argparse.ArgumentParser(description="Run the Sales Agent to find and message leads.")
    parser.add_argument("--role", type=str, default="CEO", help="Role filter for ICP.")
    parser.add_argument("--region", type=str, default="US", help="Region filter for ICP.")
    parser.add_argument("--count", type=int, default=3, help="Number of leads to fetch.")
    args = parser.parse_args()

    db_client = DBClient()
    deps = SalesDependencies(icp_filters={"role": args.role, "region": args.region}, db=db_client)

    print("=== Starting Sales Agent ===")
    # 1) Run find_leads tool
    result1 = SalesAgent.run_sync(
        deps,
        function_call={
            "name": "find_leads",
            "arguments": {
                "count": args.count
            }
        }
    )
    print(f"Find leads result => {result1.data}")

    # 2) For each lead, let's do a quick outreach
    leads = db_client.get_all_leads()
    for lead in leads:
        outreach_message = f"Hi {lead.twitter_handle}, we have a great tip for {args.role}s in {args.region}. Interested?"
        SalesAgent.run_sync(
            deps,
            function_call={
                "name": "outreach_lead",
                "arguments": {
                    "twitter_handle": lead.twitter_handle,
                    "message": outreach_message
                }
            }
        )

    # 3) Check for responses
    SalesAgent.run_sync(
        deps,
        function_call={
            "name": "check_responses",
            "arguments": {}
        }
    )

    print("All leads who replied so far:")
    for l in db_client.get_all_leads():
        if l.replied:
            print(f"Lead {l.twitter_handle} has replied!")

if __name__ == "__main__":
    main()
