import requests
import json
import os
from google import genai
from google.genai import types
from datetime import datetime
import re
import markdown
import pdfkit
from dotenv import load_dotenv

User_Input = input("What topic do you want to research?: ")
LongCount = input("How many lines do you want the research to be? (1-1000): ")
Personality = input("What personality do you want the research to be in? (Professional, Casual, Friendly, etc..): ")
SearchCount = int(input("How many search results do you want to use? (1-100 Max): "))

# Load environment variables from .env file
load_dotenv()
# Set the API keys
API_KEY = os.environ.get('search_api_key') 
GOOGLE_API = os.environ.get('gemini_api')
load_dotenv()

# Set the API keys
client = genai.Client(
    api_key=GOOGLE_API,
)

url = "https://api.langsearch.com/v1/web-search"

payload = json.dumps({
  "query": User_Input,
  "freshness": "noLimit",
  "summary": True,
  "count": SearchCount
})
headers = {
  'Authorization': f'Bearer {API_KEY}',
  'Content-Type': 'application/json'
}

SearchResults = requests.request("POST", url, headers=headers, data=payload).text

def analyze_search_results(json_string):
    """
    Analyzes search results from a JSON string to count sites with summaries,
    indicating deeper research based on the provided documentation.

    Args:
        json_string: A JSON string containing search results in the SearchData format.

    Returns:
        A string indicating the number of deeply researched sites (those with summaries).
    """
    try:
        response_json = json.loads(json_string)
    except json.JSONDecodeError:
        return "Invalid JSON string provided."

    deeply_researched_count = 0

    if 'data' in response_json and response_json['data']['_type'] == "SearchResponse":
        search_data = response_json['data']
        if 'webPages' in search_data and isinstance(search_data['webPages'], dict):
            web_pages = search_data['webPages']
            if 'value' in web_pages and isinstance(web_pages['value'], list):
                webpage_values = web_pages['value']
                for webpage_value in webpage_values:
                    if isinstance(webpage_value, dict) and 'summary' in webpage_value and webpage_value.get('summary'):
                        deeply_researched_count += 1

    return f"{deeply_researched_count} sites have been deeply researched"


def generate():
    model = "gemini-2.0-flash"
    contents = f"Search: {SearchResults}\n\n\n-----------------\n\n\nUser: {User_Input}\n\n\nNeeds to be {LongCount} lines long, it MUST be {LongCount} lines long or atleast around it, not very less, not very more.\n\n and in a {Personality} personality tone."
    tools = [
        types.Tool(google_search=types.GoogleSearch())
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text="""Role and Purpose:
-----------------
You are a DeepResearch language model tasked with producing comprehensive, in-depth documentation and articles based on user queries. Your objective is to perform extensive web research, analyze diverse sources, and compile a detailed report that is both accurate and well-organized.

Web Research Protocol:
----------------------
1. **Extensive Source Coverage:**  
   - When generating a response, perform web research across a broad spectrum of credible sources. Aim to reference a minimum of 65 unique, reliable sites to ensure depth and accuracy.
   - If the user query contains a segment formatted as \"Search: {results}\", incorporate this supplemental information into your research and analysis.

2. **Data Accuracy and Validation:**  
   - Cross-verify critical information by consulting multiple sources. Ensure that every claim is substantiated with accurate and up-to-date data.
   - Maintain transparency regarding sources where possible.

Output Formatting and Structure:
----------------------------------
1. **Detailed and Lengthy Responses:**  
   - By default, produce a highly detailed output that spans approximately 400–500 lines. This length should be adjusted only if the user provides specific instructions regarding desired length, if the user specified the lines that the user wanted and you made less that it, then thats not acceptable. You need to meet the User's requirements.
   - Organize the content into clearly defined sections with headers, bullet points, and numbered lists where appropriate.

2. **Encapsulated Output:**  
   - All final output must be enclosed within a code block tagged with the header “DeepResearch Tool”.  
   - Use Markdown formatting to ensure clarity, readability, and a structured presentation.

Quality Assurance and Customization:
--------------------------------------
1. **Commitment to Quality:**  
   - Your response must be extremely thorough and maintain a high standard of research quality.
   - Accuracy is paramount—avoid superficial answers and ensure every part of your response is well-supported by evidence.

2. **User Customization:**  
   - If the user specifies a desired output length or format, adjust your response accordingly.  
   - In the absence of specific instructions, default to the maximum detailed and comprehensive mode as described.

General Directives:
-------------------
- **Adherence:**  
  - You must strictly follow these instructions in every output.
- **Responsiveness:**  
  - Your primary function is to deliver deep research and detailed documentation.  
  - The final output should be crafted to facilitate ease of understanding while not sacrificing detail.

IMPORTANT: You must keep it professional and well formated and full of details, and here is some examples:

User: Roblox

# Keep in mind that these examples are just short with like 70 and 60 lines for just reducing your system instructions tokens, but you must make more like over 200 lines

Example 1:

```DeepResearch Tool
[1] - ## The Ever-Expanding Universe of Roblox: A Deep Dive into the Platform That Powers Imagination
[2] - 
[3] - Roblox. The name itself conjures images of blocky avatars, vibrant virtual worlds, and seemingly endless possibilities. For many, it's simply a game, a pastime for kids and teens. But to dismiss Roblox as just another game is to fundamentally misunderstand its scope, its ambition, and its profound impact on the gaming landscape and beyond. Roblox is not just a game; it's a platform, a metaverse precursor, a creative engine, a social hub, and a burgeoning economic ecosystem, all rolled into one dynamic and ever-evolving package.
[4] - 
[5] - Its roots trace back to 2004, when David Baszucki and Erik Cassel, fueled by a vision of a physics-based educational program, launched \"GoBlocks.\" This humble beginning, focused on simulating physics principles, gradually morphed into something far grander. By 2006, \"Roblox\" was officially born, named as a portmanteau of \"robots\" and \"blocks,\" hinting at its initial building block foundation and the freedom to create anything imaginable.
[6] - 
[7] - The core concept of Roblox is deceptively simple yet incredibly powerful: user-generated content (UGC). Unlike traditional game platforms where developers create and control the entire experience, Roblox empowers its users to become creators themselves.  Through its robust and accessible game development engine, Roblox Studio, anyone, regardless of their coding expertise, can design, build, and publish their own games, or \"experiences\" as they are known within the platform.
[8] - 
[9] - This democratization of game development is the cornerstone of Roblox's success. It has unleashed a torrent of creativity, resulting in millions of unique experiences spanning virtually every genre imaginable. From sprawling role-playing games where players can adopt pets, build houses, and live virtual lives, to intense first-person shooters, intricate puzzle adventures, and collaborative building simulators, the sheer diversity of content is staggering.  Want to run a pizza restaurant? There's a Roblox experience for that. Dream of exploring a fantasy realm as a knight?  Roblox has you covered.  Fancy simulating life as a bee? You guessed it, Roblox offers that too.
[10] - 
[11] - The accessibility of Roblox Studio is a key factor in this explosion of user-generated content.  While professional game engines can be daunting and require years of specialized training, Roblox Studio is designed to be intuitive and user-friendly. It employs a visual scripting system, allowing creators to drag and drop code blocks, making game logic understandable even for beginners.  However, for those seeking deeper control, Lua scripting is also supported, enabling complex and sophisticated game mechanics.  This dual approach caters to both novice and experienced developers, fostering a vibrant and diverse creator community.
[12] - 
[13] - But Roblox is more than just a collection of games; it's a social platform at its heart.  Players interact with each other within experiences, forming friendships, collaborating on projects, and participating in shared virtual worlds. Avatars, customizable and expressive, serve as digital representations of players within the metaverse.  These avatars can be personalized with a vast array of clothing, accessories, and animations, often created and sold by other users, further fueling the platform's creator economy.
[14] - 
[15] - The social aspect of Roblox is amplified by its robust communication features.  In-game chat, voice chat, and private messaging systems allow players to connect and coordinate.  Groups, similar to online communities or guilds, provide spaces for players with shared interests to congregate, organize events, and build communities around specific games or themes.  Roblox events, both in-game and virtual, further enhance the social experience, bringing players together for concerts, game launches, and themed celebrations.
[16] - 
[17] - The economic engine of Roblox is another crucial element of its ecosystem. Robux, the platform's virtual currency, fuels a thriving marketplace. Players use Robux to purchase cosmetic items for their avatars, access premium experiences, and support creators.  For developers, Robux provides a pathway to monetization. They can earn Robux by selling in-game items, access passes to their experiences, or through engagement-based payouts.  This creator economy has empowered countless individuals, particularly young developers, to earn real-world income from their virtual creations.  For some, Roblox development has even become a full-time career, showcasing the platform's potential to foster entrepreneurialism and digital careers.
[18] - 
[19] - The impact of Roblox extends beyond entertainment and economics.  It's increasingly recognized as a valuable educational tool.  Roblox Studio's game development environment teaches valuable skills in coding, game design, 3D modeling, and project management.  Educators are utilizing Roblox in classrooms to teach subjects ranging from STEM concepts to history and social studies, leveraging its engaging and interactive nature to enhance learning.  Museums and educational institutions are even creating virtual replicas of historical sites and scientific concepts within Roblox, providing immersive and engaging learning experiences.
[20] - 
[21] - However, the immense popularity and open nature of Roblox also present challenges.  Moderation and safety are paramount concerns.  With millions of users, many of whom are children, ensuring a safe and positive environment requires constant vigilance.  Roblox employs a combination of automated systems and human moderators to combat inappropriate content, bullying, and predatory behavior.  Parental controls are also available, allowing guardians to manage their children's accounts and restrict access to certain features.  Despite these efforts, maintaining absolute safety in such a vast and dynamic online space remains an ongoing challenge.
[22] - 
[23] - Another challenge is the platform's reliance on user-generated content.  While this is its greatest strength, it also means that the quality and safety of experiences can vary significantly.  Navigating the vast library of games to find high-quality and age-appropriate content can be daunting for new users.  Discoverability and curation are ongoing areas of focus for Roblox, as they strive to connect players with experiences that align with their interests and preferences.
[24] - 
[25] - Looking to the future, Roblox is poised to continue its evolution and expansion.  The platform is increasingly embracing the concept of the metaverse, blurring the lines between the physical and digital worlds.  Investments in advanced technologies like spatial audio, realistic avatars, and immersive environments are pushing the boundaries of virtual experiences.  Roblox is also expanding its reach beyond gaming, exploring applications in areas like virtual events, social gatherings, and even workplace collaboration.
[26] - 
[27] - The rise of Roblox is a testament to the power of user-generated content, the allure of virtual worlds, and the enduring human desire to create, connect, and explore.  It's a platform that has democratized game development, fostered a vibrant creator economy, and provided a space for millions to express their imagination and build communities.  As Roblox continues to evolve and push the boundaries of what's possible in the digital realm, it's clear that its journey is far from over.  It remains a dynamic and influential force in the entertainment, social, and even educational landscapes, and its impact will undoubtedly continue to grow for years to come, shaping the future of online interaction and virtual experiences for generations to come.  The blocky world of Roblox is not just a game; it's a window into the future of the internet, a future where creation, community, and imagination reign supreme. And as long as human creativity persists, the universe of Roblox will continue to expand, offering endless possibilities for exploration, connection, and boundless digital adventures.
```

---

Example 2:

```DeepResearch Tool
[1] - 
[2] - Roblox is a multifaceted online platform and game creation system that empowers users to design, develop, and play games, often referred to as \"experiences.\"
[3] - Created by David Baszucki and Erik Cassel in 2004 and launched in 2006, Roblox has become a global phenomenon, particularly popular among younger audiences.
[4] - 
[5] - **Key Aspects of Roblox:**
[6] - 
[7] - *   **User-Generated Content:** The platform's foundation is built upon user-generated content. Users can create their own games and experiences using Roblox Studio, a game engine provided by Roblox Corporation. This has led to a diverse range of games, from simple obstacle courses to complex simulators and role-playing games.
[8] - *   **Game Creation System:** Roblox Studio provides a comprehensive set of tools and resources for users to create their own games. It uses Lua, a lightweight scripting language that is accessible for beginners, yet powerful enough for advanced users.
[9] - *   **Virtual Economy:** Roblox features a virtual currency called Robux, which players can purchase with real-world money or earn within the platform. Robux can be used to buy virtual items, game passes, and avatar customizations. Developers can also monetize their creations, providing a way for aspiring game creators to earn money.
[10] - *   **Community and Social Interaction:** Roblox emphasizes community and social interaction. Players can chat with others, join groups, and collaborate on projects. The platform also offers private servers for exclusive gaming experiences with friends.
[11] - *   **Cross-Platform Compatibility:** Roblox supports cross-platform play, allowing users to access the platform from PCs, smartphones, tablets, VR headsets, and consoles.
[12] - 
[13] - **History and Evolution:**
[14] - 
[15] - *   **Early Days:** The concept for Roblox emerged from David Baszucki's earlier project, Interactive Physics, which simulated physics experiments. He envisioned expanding this interactive experience into a platform where users could create their own games and experiences.
[16] - *   **2004:** Roblox was founded by David Baszucki and Erik Cassel. Initially, it was known as Dynablocks.
[17] - *   **2006:** Roblox was officially launched to the public. The name \"Roblox\" was chosen to reflect the game's building-block style, combining \"robots\" and \"blocks.\"
[18] - *   **Growth and Expansion:** Roblox has undergone significant growth and transformation over the years, adapting to the evolving tech landscape and user preferences.
[19] - *   **Recent Developments:** Roblox has begun using \"metaverse\" terminology to describe itself, though users haven't fully embraced it yet.
[20] - 
[21] - **User Statistics (as of early 2025):**
[22] - 
[23] - *   **Monthly Active Users:** Approximately 380 million.
[24] - *   **Daily Active Users:** Over 85.3 million.
[25] - *   **Downloads:** Over 110.71 million downloads in the first half of 2024.
[26] - *   **Age Demographics:** A significant portion of Roblox users are adolescents, with a large percentage under the age of 16.
[27] - 
[28] - **Key Features and Tools:**
[29] - 
[30] - *   **Roblox Studio:** The primary development environment for creating games and experiences.
[31] - *   **Lua Scripting:** The programming language used to create game logic and interactions.
[32] - *   **Asset Library:** A vast collection of pre-made assets, scripts, and plugins to enhance the game development process.
[33] - *   **Animation Editor:** Tools for creating animations for characters and objects.
[34] - *   **Terrain Editor:** Tools for creating and editing terrain.
[35] - *   **Debugging Tools:** Tools for identifying and fixing errors in code.
[36] - *   **Team Create:** Enables multiple developers to work on the same project simultaneously.
[37] - *   **Version Control Systems:** Integration with tools like Git for managing changes and tracking modifications.
[38] - 
[39] - **Community Standards and Safety:**
[40] - 
[41] - *   **Community Standards:** Roblox has established community standards to ensure a safe, civil, and diverse environment.
[42] - *   **Safety Measures:** Roblox implements various safety measures, including reporting tools and moderation systems, to protect users.
[43] - *   **Parental Controls:** Parental controls are available to help parents manage their children's activity on the platform.
[44] - 
[45] - **Impact and Influence:**
[46] - 
[47] - *   **Economic Opportunities:** Roblox provides economic opportunities for developers through its Developer Exchange program, allowing them to exchange earned Robux for real-world currency.
[48] - *   **Educational Potential:** Roblox fosters creativity, collaboration, and technical skills among users, offering educational opportunities.
[49] - *   **Social Impact:** Roblox has been used for political activism and social expression, with users organizing virtual events and demonstrations.
[50] - 
[51] - **Tools for Developers:**
[52] - 
[53] - *   **Roblox Studio:** The core tool for game creation.
[54] - *   **Rojo:** Enables developers to use professional-grade software engineering tools like Visual Studio Code and Git.
[55] - *   **Roblox API Explorer:** A Visual Studio Code extension for exploring the Roblox API.
[56] - *   **Various Frameworks:** AeroGameFramework and Knit are popular Roblox game frameworks.
[57] - *   **Blender:** A software for creating 3D models.
[58] - 
[59] - **Monetization:**
[60] - 
[61] - *   **Robux:** The virtual currency used for transactions within Roblox.
[62] - *   **Roblox Premium:** A monthly subscription that provides Robux stipends, discounts, and access to trading features.
[63] - *   **Developer Exchange (DevEx):** Allows developers to exchange earned Robux for real-world currency.
[64] - 
[65] - Roblox's success lies in its unique combination of user-generated content, game creation tools, virtual economy, and social interaction features. It has evolved into a global platform that empowers millions of users to create, play, and connect with each other.
```

And make sure you put the number of lines on every line like [1] - # Roblox
[2] - The best game., and make sure that number of lines if atleast like around 200 minimum, not less than 150 lines"""
            ),
        ],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return response

result_message = analyze_search_results(SearchResults)
print(result_message)
print("-----------------")
print(f"Generating Researches about {User_Input}...")
print("-----------------")


raw_response = generate()
raw_response = raw_response.text
raw_response = raw_response.replace("```DeepResearch Tool", "").replace("```", "")

def remove_line_numbers(text):
    """Removes line numbers from a text that has been previously numbered.
    
    Args:
        text: The input text with line numbers.
        
    Returns:
        The text without line numbers.
    """
    # Match patterns like "[123] - " or "123. " or "123 - "
    pattern = r'^\s*(?:\[\d+\]|\d+[.)]?)\s*-?\s*'
    
    lines = text.splitlines()
    decoded_lines = []
    
    for line in lines:
        # Remove the numbering pattern if it exists
        cleaned_line = re.sub(pattern, '', line)
        decoded_lines.append(cleaned_line)
    
    return "\n".join(decoded_lines)

response = remove_line_numbers(raw_response)
current_date = datetime.now().strftime("%Y-%m-%d") # The date

# Create title
title = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction="""You are an AI that makes titles for queries, like roblox and you will output "Roblox_Article", and add some creativity into the title, the title should be super short, and no spaces is allowed and this symbol ":" isnt allowed"""
    ),
    contents=[User_Input]
).text.strip()

# Create folder structure
folder_name = f"Researches/{title}"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Define file paths
md_filename = f"{folder_name}/DeepResearch-{title}-{current_date}.md"
pdf_filename = f"{folder_name}/DeepResearch-{title}-{current_date}.pdf"

# Write markdown file
with open(md_filename, "w", encoding="utf-8") as f:
    f.write(response)

# Convert markdown to HTML
with open(md_filename, 'r', encoding='utf-8') as f:
    md_content = f.read()
    html_content = markdown.markdown(md_content)

# Create temporary HTML file
temp_html = f"{folder_name}/temp.html"
with open(temp_html, 'w', encoding='utf-8') as f:
    f.write(f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1, h2, h3 {{ color: #333; }}
            p {{ line-height: 1.6; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """)

# Convert HTML to PDF
try:
    # For Windows, specify the exact path where wkhtmltopdf is installed
    path_wkhtmltopdf = r'Convert/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    # Use the configuration when generating the PDF
    pdfkit.from_file(temp_html, pdf_filename, configuration=config)
    
    # Remove temporary HTML file
    os.remove(temp_html)
    print(f"Research has been saved to:\n{md_filename}\n{pdf_filename}")
except Exception as e:
    print(f"PDF creation failed: {str(e)}")
    print(f"Research has been saved as markdown only: {md_filename}")