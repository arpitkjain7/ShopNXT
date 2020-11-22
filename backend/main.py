from api.route import app
import uvicorn
import os


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
