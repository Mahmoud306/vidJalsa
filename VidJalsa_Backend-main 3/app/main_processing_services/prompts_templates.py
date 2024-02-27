summarize_prompt_text = """
   **Role:** you are a helpful AI assistant tasked with summarizing and creating blog content for a web page
    
   **Task:** Enhanced Summarization Task, where you'll transform a transcript collection into a captivating narrative tailored for web audiences. Your mission is to distill the essence of the material while infusing it with creativity, precision, and adherence to the following enhanced guidelines:
    Transcrript Colllection: {text}
   **Guidlines:**
   
        1. Unified Core Summarization:
            Craft a seamless narrative that integrates the main themes, critical points, and significant details from the transcript. Your goal is to ensure a logical flow from start to finish, preserving the informational richness of the original material.

        2. Narrative Enrichment:
            Enhance the narrative by incorporating relevant additional information where the transcript lacks detail or context. These enrichments should complement the core material, offering a comprehensive understanding of the subject.

        3. Focused Relevance:
            Maintain strict relevance to the subject matter of the transcript, excluding extraneous content. Every sentence should contribute to a deeper understanding or appreciation of the topic at hand.

        4. Audience-Centric Appropriateness:
            Tailor the summary to a broad spectrum of web users, ensuring universal accessibility and respectfulness. Avoid any material that could be deemed inappropriate or offensive, fostering an inclusive and informative environment.

        5. Verbal Content Emphasis:
            Focus solely on the informational essence of the verbal content, omitting non-verbal elements. This approach ensures clarity and accessibility without relying on visual or auditory cues.

        6. Inclusivity of Essential Insights:
            Weave all pivotal insights, arguments, and data from the transcript into the narrative. This inclusive approach provides readers with a full understanding of the topic without needing to reference the original video content.

        7. Diligent Content Review:
            Conduct a meticulous review for coherence, completeness, and alignment with the guidelines. The final piece should stand as a testament to quality, engaging and informing readers without prior knowledge of the original transcripts.
    
    
    **Handling Coding and Technical Content:**
        If the transcript contains coding or technical content, ensure that the summary maintains the technical accuracy and relevance of the original material. The summary should be accessible to a general audience while preserving the integrity of the technical concepts discussed. follow these rules to handel the technical content:
        
        **Rules:**
            1. Simplify complex technical concepts: 
                Simplify technical concepts into layman's terms, ensuring that the summary remains accessible to a broad audience.
            
            2. Add code blocks and examples:
                If the transcripys content is about coding or technical examples; generate a code block or technical example to the summary based on the transcript examples content.
            
            3. Clarify technical jargon:
                Clarify any technical jargon or acronyms used in the transcript, providing brief explanations to ensure reader comprehension.
    
   
    **Handling sports and entertainment content:**
        If the transcript contains sports or entertainment content, ensure that the summary captures the excitement and key highlights of the original material. The summary should convey the energy and enthusiasm of the content while providing a concise overview of the main points. follow these rules to handel the sports and entertainment content:
        
        **Rules:**
            1. Capture the Excitement and Energy:
                Infuse the summary with the excitement and energy of the original content, conveying the enthusiasm to the reader. Use dynamic language, vivid descriptions, and engaging storytelling techniques to immerse the audience in the world of sports or entertainment. Whether it's the thrill of a game-winning goal or the electrifying performance of a live concert, make sure the summary reflects the passion and intensity of the experience.

            2. Highlight Key Moments and Insights:
                Focus on highlighting the most memorable moments and insightful observations from the transcript. Whether it's a game-changing play in a sports event or a thought-provoking comment from a celebrity interview, ensure that these key moments are prominently featured in the summary. Use quotes, anecdotes, and descriptive language to bring these moments to life and emphasize their significance to the overall narrative.

            3. Celebrate Achievements and Performances:
                Celebrate the achievements and performances of athletes, entertainers, or artists mentioned in the transcript. Acknowledge their talent, dedication, and impact on their respective fields, and highlight any notable accomplishments or milestones. Whether it's a record-breaking athletic achievement or a critically acclaimed film or album, give credit where it's due and convey the importance of these achievements to the audience.

            4. Provide Context and Background Information:
                Offer context and background information to help readers understand the significance of the sports or entertainment content discussed in the transcript. This could include information about the history of a particular sports team or event, the background of a famous entertainer or artist, or the cultural context surrounding a specific performance or production. Providing this context enriches the reader's understanding and appreciation of the content.

            5. Engage the Audience with Interactive Elements:
                Enhance reader engagement by incorporating interactive elements such as polls, quizzes, or multimedia content related to the sports or entertainment topic. This not only makes the summary more interactive and entertaining but also encourages reader participation and interaction with the content. Whether it's asking readers to vote for their favorite sports moment or challenging them to guess the next plot twist in a popular TV show, interactive elements can make the summary more engaging and enjoyable for the audience.


        

    By adhering to these refined guidelines, you'll create a narrative that captivates, informs, and meets the high standards required for web content. Your dedication to crafting resonant and enriching narratives is appreciated, elevating the online experience for all readers.
"""
blog_quality_template ="""
    **Role:** you are a helpful AI assistant tasked with summarizing and creating blog content for a web page
    
    **Task:** given the summarized transcripts delimted in the triple  back ticks ```{text}```, you are to generate a captivating article based on the summarized content provided as follows:
    
    **Guidlines:**
        1. Paragraphing:
            Divide the combined summarized transcripts into an array of paragraphs. Each paragraph should encapsulate a distinct idea or aspect of the summary, maintaining a logical flow and engaging the reader with a tone that is both conversational and accessible. For example, if the transcript discusses the benefits of a particular diet plan, one paragraph could focus on the importance of balanced nutrition, while another paragraph could delve into specific meal suggestions.

        2. Adding Examples and Quotes:
            Enhance the article's engagement and informativeness by incorporating relevant examples and quotes. These additions should enrich the content and provide readers with practical insights. For instance, if the transcript mentions a success story of someone who implemented the discussed strategies, include a quote from that individual to illustrate the effectiveness of the approach.
            ##EXAMPLE:## for example, if a paragraph is about coding in python; try add an code example with proper syntax of the code 

        3. Handling Objections and Counterarguments:
            Anticipate potential objections or counterarguments to the main points discussed in the transcripts. Address these concerns within the article by providing counterpoints supported by evidence or expert opinions. This demonstrates a thorough understanding of the topic and enhances the article's credibility. For example, if the transcript discusses the benefits of a specific exercise routine, acknowledge common misconceptions or challenges associated with it and offer solutions or clarifications.
        
        4. Coherent Narrative Flow:
            Ensure that the article maintains a coherent and logical narrative flow. The paragraphs should transition smoothly from one to the next, guiding the reader through the content with clarity and purpose. Consider the overall structure and organization of the article to create a seamless reading experience.
        
        5. Optimization for SEO:
            Ensure that the article is optimized for search engines by incorporating relevant keywords and phrases naturally throughout the text. This helps improve the article's visibility and ranking in search engine results, making it easier for readers to discover and access the content. Additionally, optimize meta tags, headings, and image alt text to further enhance SEO performance.

        6. Proofreading and Editing:
            Before publishing the article, thoroughly proofread and edit the content to ensure clarity, coherence, and grammatical accuracy. Correct any spelling or punctuation errors, refine sentence structures for readability, and ensure consistency in tone and style throughout the article. A polished and error-free article reflects positively on the credibility and professionalism of the website.

   
    By incorporating these additional points into the article creation process, you can ensure that the final product is not only informative and engaging but also optimized for audience interaction and search engine visibility.

"""

blog_gen_prompt_text = """
    **Task: Generate a Medium-Style Article as a JSON Object**

    **Objective:** Create a captivating article based on the summarized content provided provided as follows: 
    {combined_summarized_transcript}
    
    The article must reflect the style of Medium publications, which are recognized for their engaging titles, thought-provoking questions, distinctive authorship, and coherent narrative flow. The output should be a JSON object that includes these elements derived from the given input.

    **Process Overview:**

    - **Input:** A single variable, combined summarized transcript, which contains summarized text on a contemporary topic.
    - **Output:** A JSON object structured with four key components: Title, Question, Author, and Paragraphs.

    **Detailed Instructions for JSON Structure:**

    1. **Title:** Generate a compelling title that captures the essence of the summarized text. The title must be eye-catching and reflective of the content’s core message.

    2. **Question:** Craft a thought-provoking question pertinent to the article's theme. This question should spark curiosity and motivate the reader to explore the topic further.

    3. **Author:** Invent an author name that incorporates "AI" in uppercase, indicating the AI-enhanced creation of the article. Ensure that this name is plausible and fits within the context of authorship on Medium. Ensure also that they are real names for humans and contain a first and last name.

    4. **Paragraphs:** Divide the combined summarized transcripts into an array of paragraphs. Each paragraph should encapsulate a distinct idea or aspect of the summary, maintaining a logical flow and engaging the reader with a tone that is both conversational and accessible.

    **Output Formatting Requirement:**

    The output must be formatted as a JSON object as follows:

    ```json
    {{
        "Title": "Generated Title Based on Summary",
        "Question": "Generated Question Based on Summary",
        "Author": "Generated Author Name Including AI",
        "Paragraphs": [
            "First paragraph of the article...",
            "Second paragraph of the article...",
            "...additional paragraphs as derived from the summarized text"
        ]
    }}
    ```
    
    The content generation process should be strictly based on the input summary, without requiring any additional inputs. The JSON structure is designed to organize the content neatly, facilitating its direct application or web deployment.
"""

image_generation_prompt = """
    "Task": "Generate an Illustrative Image Based on a Given Title",
    "Objective": "Create an image that directly represents the provided title.",
    "Title": "Title of the Video: {video_title}",
    "Instructions":
        "1": "Ensure the image depicts elements relevant to the topic mentioned in the title.",
        "2": "Use simple and clear imagery that conveys the central theme of the title.",
        "3": "Focus on accuracy and clarity rather than artistic creativity.",
        "4": "Maintain a straightforward composition that aligns with the title's subject matter.",
        "5": "Avoid embellishments or unnecessary details that may distract from the main message.",
        "6": "Choose colors and tones that suit the tone and context of the title.",
        "7": "Consider using symbols or icons directly related to the topic to enhance understanding.",
        "8": "Ensure the image is easily recognizable and understandable to the intended audience.",
        "9": "Opt for a clean and professional design that effectively communicates the title's message.",
        "10": "Verify that the image effectively complements the title without overshadowing it.",
        "11": "Keep the image format and style in line with the platform or medium where it will be displayed.",
        "12": "Use imagery that aligns with the target audience's expectations and preferences.",
        "13": "Consider using charts, graphs, or diagrams if the title involves data or statistics.",
        "14": "If the title suggests a process or sequence, consider depicting it step by step in the image.",
        "15": "Ensure the image size and resolution are suitable for the intended use and platform.",
        "16": "Test the image with a sample audience to ensure it effectively communicates the title's message.",
        "17": "Avoid clichés or overused imagery that may dilute the impact of the title.",
        "18": "If applicable, incorporate recognizable landmarks or objects associated with the topic.",
        "19": "Strive for clarity and simplicity in the image's composition to facilitate quick comprehension.",
        "20": "Ensure the image is free from any potentially confusing or misleading elements.",
        "21": "Consider incorporating relevant text or captions directly related to the title to reinforce the message.",
        "22": "Use visual metaphors or analogies if they enhance understanding and engagement with the title.",
        "23": "Ensure the image is culturally sensitive and appropriate for diverse audiences.",
        "24": "Consider the context in which the image will be viewed and adjust the content accordingly.",
        "25": "Ensure the image is accessible to individuals with visual impairments by following accessibility guidelines.",
        "26": "Avoid using copyrighted material unless it falls under fair use or has proper licensing.",
        "27": "Consider the emotional impact of the image and adjust elements accordingly to evoke desired responses.",
        "28": "Strive for a balance between realism and abstraction in the image's representation of the title.",
        "29": "Iterate on the design to refine details and enhance the overall effectiveness of the image."
    """
