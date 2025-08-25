from gradio_client import Client

try:
    print("🔄 Connecting to Hugging Face Space...", flush=True)
    client = Client("https://rathod31-kannada-english-sim.hf.space")
    print("✅ Connected.", flush=True)

    apis = client.view_api()
    print("📌 Available APIs:", apis, flush=True)

except Exception as e:
    print("❌ Error:", str(e), flush=True)
