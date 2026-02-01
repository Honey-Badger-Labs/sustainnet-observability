"""
HRAIM Slack Integration Module
- Webhooks receiver
- Decision notifications
- Kill-switch alerts
- Daily standup summaries
"""

import os
import json
import hmac
import hashlib
import time
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
import httpx
import asyncio

app = FastAPI(title="HRAIM Slack Integration")

# ============================================================================
# CONFIGURATION
# ============================================================================

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
SLACK_CHANNEL = '#hraim-mvp'

# ============================================================================
# SLACK SIGNATURE VERIFICATION
# ============================================================================

def verify_slack_signature(request_body: bytes, timestamp: str, signature: str) -> bool:
    """
    Verify that the request came from Slack
    Using HMAC-SHA256
    """
    if abs(time.time() - int(timestamp)) > 300:
        return False  # Request older than 5 minutes
    
    sig_basestring = f'v0:{timestamp}:{request_body.decode("utf-8")}'
    my_signature = f"v0={hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()}"
    
    return hmac.compare_digest(my_signature, signature)

# ============================================================================
# SLACK API CLIENTS
# ============================================================================

async def send_slack_message(text: str, thread_ts: str = None) -> str:
    """Send message to #hraim-mvp channel"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://slack.com/api/chat.postMessage',
            headers={'Authorization': f'Bearer {SLACK_BOT_TOKEN}'},
            json={
                'channel': SLACK_CHANNEL,
                'text': text,
                'thread_ts': thread_ts
            }
        )
    
    data = response.json()
    if not data.get('ok'):
        raise Exception(f"Slack API error: {data.get('error')}")
    
    return data.get('ts')  # Message timestamp

async def send_slack_blocks(blocks: list, text: str = "HRAIM Notification") -> str:
    """Send formatted message with Block Kit"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://slack.com/api/chat.postMessage',
            headers={'Authorization': f'Bearer {SLACK_BOT_TOKEN}'},
            json={
                'channel': SLACK_CHANNEL,
                'text': text,
                'blocks': blocks
            }
        )
    
    data = response.json()
    if not data.get('ok'):
        raise Exception(f"Slack API error: {data.get('error')}")
    
    return data.get('ts')

# ============================================================================
# NOTIFICATION FORMATTERS
# ============================================================================

def format_cm_created_notification(actor_name: str, decision_statement: str, entry_id: str) -> list:
    """Format Slack blocks for new decision"""
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📝 New Decision Created",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Actor*\n{actor_name}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Time*\n{datetime.utcnow().strftime('%H:%M:%S')}"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Decision*\n```{decision_statement}```"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Deliberation"
                    },
                    "value": entry_id,
                    "action_id": f"deliberate_{entry_id}"
                }
            ]
        }
    ]

def format_cm_ratified_notification(actor_name: str, decision_statement: str, entry_id: str) -> list:
    """Format Slack blocks for ratified decision"""
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "✅ Decision Ratified",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Confirmed By*\n{actor_name}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Time*\n{datetime.utcnow().strftime('%H:%M:%S')}"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Decision*\n```{decision_statement}```"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Entry ID: `{entry_id}`"
                }
            ]
        }
    ]

def format_kill_switch_notification(actor_name: str, reason: str, event_id: str) -> list:
    """Format Slack blocks for kill-switch activation"""
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🛑 KILL-SWITCH ACTIVATED",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Triggered By*\n{actor_name}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Time*\n{datetime.utcnow().strftime('%H:%M:%S')}"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Reason*\n{reason}"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Event ID: `{event_id}`"
                }
            ]
        }
    ]

def format_daily_standup(stats: dict) -> list:
    """Format Slack blocks for daily standup"""
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📊 HRAIM Phase 1 Daily Standup",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Total Decisions*\n{stats.get('total_decisions', 0)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Ratified*\n{stats.get('ratified_decisions', 0)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Deliberations*\n{stats.get('deliberation_count', 0)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Avg Deliberation*\n{stats.get('avg_duration_ms', 0)}ms"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Audit Trail*\n{stats.get('audit_entries', 0)} operations logged"
            }
        }
    ]

# ============================================================================
# SLACK EVENT HANDLERS
# ============================================================================

@app.post("/slack/events")
async def handle_slack_events(request: Request):
    """Handle Slack event subscriptions"""
    body = await request.body()
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    
    # Verify signature
    if not verify_slack_signature(body, timestamp, signature):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    payload = json.loads(body)
    
    # Handle URL verification challenge
    if payload.get('type') == 'url_verification':
        return {'challenge': payload.get('challenge')}
    
    # Handle message events
    if payload.get('type') == 'event_callback':
        event = payload.get('event', {})
        
        if event.get('type') == 'message':
            # Process incoming message
            await handle_message(event)
    
    return {'ok': True}

async def handle_message(event: dict):
    """Process incoming Slack message"""
    text = event.get('text', '')
    ts = event.get('thread_ts') or event.get('ts')
    
    # Commands
    if text.startswith('!standup'):
        # Send daily standup summary
        stats = {
            'total_decisions': 5,
            'ratified_decisions': 3,
            'deliberation_count': 5,
            'avg_duration_ms': 2100,
            'audit_entries': 25
        }
        await send_slack_blocks(
            format_daily_standup(stats),
            "Daily Standup Report"
        )

# ============================================================================
# INCOMING WEBHOOKS (from Backend)
# ============================================================================

@app.post("/slack/webhook/decision-created")
async def webhook_decision_created(data: dict):
    """Webhook from SN1MA backend when decision is created"""
    blocks = format_cm_created_notification(
        actor_name=data.get('actor_name'),
        decision_statement=data.get('decision_statement'),
        entry_id=data.get('entry_id')
    )
    
    await send_slack_blocks(blocks, "New Decision")
    return {'ok': True}

@app.post("/slack/webhook/decision-ratified")
async def webhook_decision_ratified(data: dict):
    """Webhook from SN1MA backend when decision is ratified"""
    blocks = format_cm_ratified_notification(
        actor_name=data.get('actor_name'),
        decision_statement=data.get('decision_statement'),
        entry_id=data.get('entry_id')
    )
    
    await send_slack_blocks(blocks, "Decision Ratified")
    return {'ok': True}

@app.post("/slack/webhook/kill-switch-triggered")
async def webhook_kill_switch(data: dict):
    """Webhook from SN1MA backend when kill-switch is activated"""
    blocks = format_kill_switch_notification(
        actor_name=data.get('actor_name'),
        reason=data.get('reason'),
        event_id=data.get('event_id')
    )
    
    await send_slack_blocks(blocks, "KILL-SWITCH ACTIVATED")
    return {'ok': True}

# ============================================================================
# SCHEDULING
# ============================================================================

# TODO: Use APScheduler for daily standup at 5 PM SAST
# async def scheduled_standup():
#     await send_slack_blocks(format_daily_standup(...))

# ============================================================================
# HEALTH
# ============================================================================

@app.get("/slack/health")
async def slack_health():
    """Check Slack integration health"""
    return {
        "status": "ok",
        "slack_configured": bool(SLACK_BOT_TOKEN),
        "channel": SLACK_CHANNEL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3002)
