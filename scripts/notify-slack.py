#!/usr/bin/env python3
"""
Send Slack notification
"""
import argparse
import json
import os
import sys
try:
    import requests
except ImportError:
    print("requests not installed, skipping")
    sys.exit(0)

def send_slack(webhook_url, payload):
    """Send to Slack"""
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

def format_message(status, cost, image, commit, actor, branch):
    """Format message"""
    
    emoji_map = {
        'success': ':white_check_mark:',
        'failure': ':x:',
        'cancelled': ':warning:'
    }
    emoji = emoji_map.get(status.lower(), ':question:')
    
    color_map = {
        'success': '#36a64f',
        'failure': '#ff0000',
        'cancelled': '#ffaa00'
    }
    color = color_map.get(status.lower(), '#808080')
    
    payload = {
        "text": f"{emoji} Deployment {status.upper()}",
        "attachments": [{
            "color": color,
            "fields": [
                {"title": "Status", "value": status.upper(), "short": True},
                {"title": "Cost", "value": f"${cost}/month", "short": True},
                {"title": "Image", "value": f"`{image}`", "short": False},
                {"title": "Commit", "value": f"`{commit[:8]}`", "short": True},
                {"title": "Branch", "value": branch, "short": True},
                {"title": "Actor", "value": actor, "short": True}
            ],
            "footer": "Golden Path CI/CD"
        }]
    }
    
    return payload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--status', required=True)
    parser.add_argument('--cost', required=True)
    parser.add_argument('--image', required=True)
    parser.add_argument('--commit', default='unknown')
    parser.add_argument('--actor', default='unknown')
    parser.add_argument('--branch', default='unknown')
    
    args = parser.parse_args()
    
    webhook = os.getenv('SLACK_WEBHOOK')
    if not webhook:
        print("SLACK_WEBHOOK not set")
        return 0
    
    payload = format_message(
        args.status, args.cost, args.image,
        args.commit, args.actor, args.branch
    )
    
    success = send_slack(webhook, payload)
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())