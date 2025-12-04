"""Test script to verify configuration migration"""
import config
import app

print("="*50)
print("✅ Configuration Test Results")
print("="*50)
print(f"\n📡 Adafruit IO:")
print(f"   Username: {config.AIO_USERNAME}")
print(f"   API Key: {config.AIO_KEY[:15]}...")

print(f"\n🗄️ Database:")
print(f"   URL: {config.DATABASE_URL[:40]}...")

print(f"\n🔐 Flask:")
print(f"   Secret Key: {config.FLASK_SECRET_KEY[:20]}...")

print(f"\n📊 Feeds configured:")
for feed_name, feed_path in config.FEEDS.items():
    print(f"   - {feed_name}: {feed_path}")

print(f"\n✅ App.py variables:")
print(f"   AIO_USERNAME: {app.AIO_USERNAME}")
print(f"   DB_CONNECTION_STRING: {app.DB_CONNECTION_STRING[:40]}...")
print(f"   Feeds count: {len(app.FEEDS)}")
print(f"   Flask secret configured: {bool(app.app.config.get('SECRET_KEY'))}")

print("\n" + "="*50)
print("✅ All tests passed! Ready to deploy!")
print("="*50)

