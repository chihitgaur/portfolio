import os

from django.shortcuts import render
from myportfolio import settings
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from django.views.decorators.csrf import csrf_exempt
from rapidfuzz import process
from django.utils.timezone import now

openai_api_key = os.environ.get("OPENAI_API_KEY")

def home(request):
    context = {
        "profile_image_path": settings.PROFILE_IMAGE_PATH
    }
    return render(request, 'portfolio/home.html', context)

chihit_data = {
    "experience": [
{
            "company": "Corro Health",
            "title": "AI Engineer",
            "duration": "April 2025 – Present"
        },
        {
            "company": "EMP Claims",
            "title": "Executive Developer / RPA Developer",
            "duration": "Sept 2022 – March 2025"
        },
        {
            "company": "ONGC",
            "title": "Intern",
            "duration": "June 2022 – August 2022"
        }
    ],
    "tech_stack": {
        "Languages": ["Python", "JavaScript"],
        "AI/ML": ["GPT", "BERT", "Ollama", "LangChain", "Azure AI", "Hugging Face"],
        "RPA Tools": ["UiPath", "Power Automate", "Selenium"],
        "Testing Tools": ["Selenium", "Appium"],
        "Frameworks": ["Django", "Flask"],
        "Frontend": ["HTML", "TailwindCSS"],
        "Databases": ["SQL"],
        "DevOps": ["Docker", "Kubernetes", "Jenkins", "Azure DevOps"],
        "Tools": ["Postman", "Git", "GitHub"],
        "Libraries": ["TensorFlow", "Pandas", "NumPy", "PyTorch", "PyMuPDF", "Tesseract OCR"]
    },
    "education": "B.Tech in Information Technology from Krishna Engineering College (2019–2023), CGPA: 7.20",
    "certifications": [
        "Microsoft Certified PL-500 - Power Automate RPA Developer Associate",
        "Python Programming – IIT Kanpur (2022)",
        "AI and Cognitive Technologies – IBM Skills Build (2021)"
    ],
    "awards": [
        "Best Performer – Software Team (Jan 2024)",
        "Innovator Award (Oct 2023)"
    ],
    "intro": (
    "A passionate and performance-driven AI & Automation Engineer with over 2 years of experience blending intelligent automation with cutting-edge AI technologies. With a background in Information Technology and a deep love for solving complex problems, I specialize in transforming manual processes into smart, efficient, and scalable systems—driven by a mix of logic, creativity, and innovation."
    )
}

intent_keywords = {
    "experience": ["experience", "job", "roles", "companies", "positions", "worked", "career"],
    "tech_stack": ["tech stack", "tools", "technologies", "frameworks", "languages", "skills","Testing Tools"],
    "education": ["education", "college", "university", "degree", "graduation"],
    "certifications": ["certifications", "courses", "certified", "learning", "training"],
    "awards": ["awards", "achievements", "recognition", "honors", "reward"],
    "intro": ["who is", "about", "bio", "background", "summary", "intro"]
}

# Optional synonym aliases for tech_stack categories
tech_category_aliases = {
    "devops": ["devops", "cloud tools", "cloud stack", "ci/cd", "deployment tools"],
    "rpa tools": ["rpa tools", "automation tools", "workflow automation", "rpa"],
    "ai/ml": ["ai", "machine learning", "ml", "llm", "genai", "ai models"],
    "testing tools": ["testing tools", "qa tools", "test automation", "selenium", "appium"],
    "frontend": ["frontend", "ui", "user interface", "html", "css"],
    "frameworks": ["frameworks", "django", "flask"],
    "languages": ["languages", "programming languages", "code"],
    "databases": ["databases", "sql", "storage", "data storage"],
    "tools": ["tools", "utilities", "postman", "git", "github"],
    "libraries": ["libraries", "python libraries", "ml libraries", "data libraries"]
}



def get_intent(prompt: str):
    prompt = prompt.lower()
    scores = {
        intent: max(
            [process.extractOne(prompt, kws, score_cutoff=60)[1] if process.extractOne(prompt, kws,
                                                                                       score_cutoff=60) else 0]
        )
        for intent, kws in intent_keywords.items()
    }
    best_match = max(scores.items(), key=lambda x: x[1])
    return best_match[0] if best_match[1] > 0 else None


def handle_chihit_query(prompt: str):
    intent = get_intent(prompt)
    prompt_lower = prompt.lower()

    if intent == "experience":
        return "\n".join([f"{e['title']} at {e['company']} ({e['duration']})" for e in chihit_data["experience"]])

    elif intent == "tech_stack":
        # First try exact and alias-based category matching
        for category, aliases in tech_category_aliases.items():
            for alias in aliases:
                if alias in prompt_lower:
                    category_title = next((k for k in chihit_data["tech_stack"] if k.lower() == category), None)
                    if category_title:
                        return f"{category_title}: {', '.join(chihit_data['tech_stack'][category_title])}"

        # If not found via aliases, try fuzzy match against actual keys
        best_match = process.extractOne(prompt_lower, chihit_data["tech_stack"].keys(), score_cutoff=70)
        if best_match:
            matched_category = best_match[0]
            return f"{matched_category}: {', '.join(chihit_data['tech_stack'][matched_category])}"

        # Default: return full tech stack
        return "\n".join([f"{k}: {', '.join(v)}" for k, v in chihit_data["tech_stack"].items()])

    elif intent == "education":
        return chihit_data["education"]

    elif intent == "certifications":
        return "Certifications:\n" + "\n".join(chihit_data["certifications"])

    elif intent == "awards":
        return "Awards & Achievements:\n" + "\n".join(chihit_data["awards"])

    elif intent == "intro":
        return chihit_data["intro"]

    else:
        return (
            "I can help with Chihit's experience, skills, education, certifications, or achievements. "
            "What would you like to know?"
        )


@csrf_exempt
def chatbot_view(request):
    response = ""
    if request.method == "POST":
        prompt = request.POST.get("prompt")

        # Check for Chihit-specific query
        if "chihit" in prompt.lower():
            response = handle_chihit_query(prompt)
        else:
            try:
                chat = ChatOpenAI(temperature=0, model="gpt-4o-mini",openai_api_key=openai_api_key)
                messages = [HumanMessage(content=prompt)]
                response = chat(messages).content
            except Exception as e:
                response = f"Error: {e}"
        # ✅ Log to Render console
        timestamp = now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] User: {prompt}")
        print(f"[{timestamp}] Bot: {response}")

    return render(request, 'portfolio/chatbot.html', {"response": response})

def technology(request):
    context = {
        "python_image_path": settings.PYTHON_IMAGE_PATH,
        "selenium_image_path": settings.SELENIUM_IMAGE_PATH,
        "powerautomate_image_path": settings.POWERAUTOMATE_IMAGE_PATH,
        "uipath_image_path": settings.UIPATH_IMAGE_PATH,
        "powerplatform_image_path": settings.POWERPLATFORM_IMAGE_PATH,
        "genai_image_path": settings.GENAI_IMAGE_PATH,
        "langchain_image_path": settings.LANGCHAIN_IMAGE_PATH,
        "bert_image_path": settings.BERT_IMAGE_PATH,
        "django_image_path": settings.DJANGO_IMAGE_PATH,
        "flask_image_path": settings.FLASK_IMAGE_PATH,
        "html_image_path": settings.HTML_IMAGE_PATH,
        "tailwind_image_path": settings.TAILWIND_IMAGE_PATH,
        "git_image_path": settings.GIT_IMAGE_PATH,
        "github_image_path": settings.GITHUB_IMAGE_PATH,
        "linux_image_path": settings.LINUX_IMAGE_PATH,
        "windows_image_path": settings.WINDOWS_IMAGE_PATH,
        "docker_image_path": settings.DOCKER_IMAGE_PATH,
        "kubernetes_image_path": settings.KUBERNETES_IMAGE_PATH,
        "jenkins_image_path": settings.JENKINS_IMAGE_PATH,
        "devops_image_path": settings.DEVOPS_IMAGE_PATH,
        "pandas_image_path": settings.PANDAS_IMAGE_PATH,
        "numpy_image_path": settings.NUMPY_IMAGE_PATH,
        "threading_image_path": settings.THREADING_IMAGE_PATH,
        "multiprocessing_image_path": settings.MULTIPROCESSING_IMAGE_PATH,
        "beautifulsoup_image_path": settings.BEAUTIFULSOUP_IMAGE_PATH,
        "tensorflow_image_path": settings.TENSORFLOW_IMAGE_PATH,
        "pillow_image_path": settings.PILLOW_IMAGE_PATH,
        "poppler_image_path": settings.POPPLER_IMAGE_PATH,
        "fitz_image_path": settings.FITZ_IMAGE_PATH,
        "postman_image_path": settings.POSTMAN_IMAGE_PATH
    }
    return render(request, 'portfolio/technology.html', context)


def projects(request):
    return render(request, 'portfolio/projects.html')


def contact(request):
    context = {
        "rpa_resume_path": settings.RPA_RESUME_PATH,
        "qa_resume_path": settings.QA_RESUME_PATH,
        "ai_resume_path": settings.AI_RESUME_PATH
    }
    return render(request, 'portfolio/contact.html', context)
