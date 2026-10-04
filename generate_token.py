"""
Utility script to generate LiveKit client tokens for testing.
Usage:
    python generate_token.py [room_name] [identity]
"""
import sys
import datetime
from livekit.api import AccessToken, VideoGrants

def generate(room_name="test-room", identity="tester"):
    api_key = "devkey"
    api_secret = "secretkeyphrase123456789012345632523532"

    grant = VideoGrants(
        room_join=True,
        room=room_name,
        can_publish=True,
        can_subscribe=True,
        can_publish_data=True
    )
    token = (
        AccessToken(api_key, api_secret)
        .with_identity(identity)
        .with_name(identity.title())
        .with_grants(grant)
        .with_ttl(datetime.timedelta(hours=24))
        .to_jwt()
    )
    return token

if __name__ == "__main__":
    room = sys.argv[1] if len(sys.argv) > 1 else "test-room"
    user = sys.argv[2] if len(sys.argv) > 2 else "user-test"
    token = generate(room, user)
    print("\n=== LiveKit Meet Connection Details ===")
    print(f"Server URL: ws://localhost:7880")
    print(f"Room:       {room}")
    print(f"Token:\n{token}\n")
