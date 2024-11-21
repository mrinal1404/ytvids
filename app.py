from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = "your_openai_api_key"

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    try:
        data = request.json
        resume_text = data.get("resume_text", "")
        role = data.get("role", "")

        if not resume_text or not role:
            return jsonify({"error": "Resume text and role are required."}), 400

        # Analyze the resume using OpenAI GPT
        prompt = (f"Analyze the following resume:\n\n{resume_text}\n\n"
                  f"Does this resume match the role '{role}'? "
                  "Respond with Yes or No, and explain why.")
        
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        analysis = response.choices[0].text.strip()

        if "Yes" in analysis:
            return jsonify({"match": True, "analysis": analysis})
        else:
            # Suggest YouTube videos
            videos = suggest_youtube_videos(role)
            return jsonify({"match": False, "analysis": analysis, "videos": videos})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def suggest_youtube_videos(role):
    # Example video suggestions (replace with actual YouTube API logic if needed)
    video_links = {
        "Data Scientist": [
            "https://www.youtube.com/watch?v=ua-CiDNNj30",
            "https://www.youtube.com/watch?v=5iT3KY8AC8g"
        ],
        "Software Engineer": [
            "https://www.youtube.com/watch?v=VfhYu5IlVbw",
            "https://www.youtube.com/watch?v=zOjov-2OZ0E"
        ]
    }
    return video_links.get(role, ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"])

if __name__ == '__main__':
    app.run(debug=True)
