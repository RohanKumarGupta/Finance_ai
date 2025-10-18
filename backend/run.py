import os
import sys
import uvicorn

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if cmd == "serve":
        # Support both development and deployment environments
        host = os.getenv("HOST", "127.0.0.1")
        port = int(os.getenv("PORT", 8000))
        reload = os.getenv("RELOAD", "true").lower() == "true"

        # Since this script lives in the backend/ directory, target the "app" package directly
        uvicorn.run("app.main:app", host=host, port=port, reload=reload)
    elif cmd == "seed":
        # Import seed within the backend package context
        from app.seed.seed_data import run_seed
        import asyncio
        asyncio.run(run_seed())
        print("Seed complete.")
    else:
        print("Unknown command. Use: serve | seed")
