import os
import json
import random

def generate_dataset():
    categories = {
        "tweet": {
            "topics": ["AI taking over", "drinking too much coffee", "debugging code", "Monday mornings", "new smartphone launch", "imposter syndrome", "learning Python", "open source contributions", "tech layoffs", "server crashes"],
            "templates": {
                "casual": "Just another day dealing with {topic}. Anyone else feel the same way? 😅",
                "professional": "The recent trends regarding {topic} require careful consideration from industry professionals.",
                "sarcastic": "I just love how {topic} ruins my perfectly good afternoon. Simply wonderful.",
                "enthusiastic": "Absolutely thrilled to see the progress in {topic}!! Let's go! 🚀",
                "formal": "It is imperative that we address the ongoing developments in {topic}.",
                "humorous": "Me: I'm going to sleep early. Also me at 3 AM: researching {topic}. 🤡",
                "urgent": "Start paying attention to {topic} NOW before it's too late!",
                "persuasive": "If you haven't looked into {topic} yet, you are falling behind. Trust me on this.",
                "informative": "A quick thread on {topic}: It's fundamentally changing how we approach problem-solving.",
                "empathetic": "I know {topic} can be overwhelming, but remember to take breaks and breathe. You've got this."
            }
        },
        "linkedin post": {
            "topics": ["my ML internship", "getting AWS certified", "attending a tech conference", "failing my first project", "the future of remote work", "mentoring junior devs", "launching a new feature", "improving communication skills", "work-life balance", "the importance of diversity in tech"],
            "templates": {
                "casual": "Super happy to share some thoughts on {topic}. It's been a wild ride but totally worth it! 💼",
                "professional": "I am pleased to share my recent insights into {topic}. Continuous learning is key in our industry.",
                "sarcastic": "Because what LinkedIn really needs is another long post about {topic}, right? Here we go.",
                "enthusiastic": "I couldn't wait to share this! Diving into {topic} has been an absolute game changer! 🔥",
                "formal": "The following post outlines critical reflections regarding {topic} and its broader implications.",
                "humorous": "They say the real treasure was the {topic} we made along the way. But seriously, it's been intense.",
                "urgent": "If your network isn't discussing {topic} today, you need a new network. Action is required immediately.",
                "persuasive": "You MUST prioritize {topic} in your career development plan this year. The ROI is undeniable.",
                "informative": "Here are 3 actionable takeaways from my experience with {topic}. Bookmark this for later.",
                "empathetic": "Navigating {topic} is incredibly tough. If anyone wants to chat about it, my DMs are always open."
            }
        },
        "summarization": {
            "topics": ["the plot of The Matrix", "the benefits of solar energy", "how a combustion engine works", "the history of the Roman Empire", "a long meeting about quarterly goals", "the rules of chess", "the plot of Romeo and Juliet", "the process of photosynthesis", "the 2008 financial crisis", "the theory of relativity"],
            "templates": {
                "casual": "Basically, {topic} boils down to this: stuff happens and things change.",
                "professional": "An executive summary of {topic} indicates significant paradigm shifts across multiple sectors.",
                "sarcastic": "To sum up {topic}: everything you thought you knew is wrong, and it takes hours to explain anyway.",
                "enthusiastic": "The most amazing TL;DR of {topic} ever: it is mind-blowing from start to finish!!",
                "formal": "Abstract: A comprehensive overview of {topic} reveals three primary foundational principles.",
                "humorous": "Summarizing {topic} is easy: imagine a circus, but with less coordination.",
                "urgent": "The TL;DR on {topic} is critical to review by end of day to prevent cascading failures.",
                "persuasive": "Let me break down {topic} for you, and why understanding it will give you a massive competitive edge.",
                "informative": "In summary, {topic} involves several historical and scientific interconnected phases.",
                "empathetic": "I know trying to understand {topic} is draining, but the short version is that patience is key."
            }
        },
        "Q&A": {
            "topics": ["What is the capital of France?", "How do you boil an egg?", "What is object-oriented programming?", "Who wrote Hamlet?", "What causes a rainbow?", "How far is the moon?", "What is the speed of light?", "Why is the sky blue?", "How does a blockchain work?", "What is the largest mammal on Earth?"],
            "templates": {
                "casual": "Great question about '{topic}'! Simply put, it's pretty straightforward.",
                "professional": "Regarding your inquiry, '{topic}', the consensus in the field provides a clear answer.",
                "sarcastic": "Oh, '{topic}'? Let me Google that incredibly complex mystery for you.",
                "enthusiastic": "I LOVE answering '{topic}'! Let me tell you all the amazing details!",
                "formal": "The response to the query '{topic}' is thoroughly documented in academic literature.",
                "humorous": "If I had a dollar for every time someone asked '{topic}', I'd be retired. Anyway, here's the answer.",
                "urgent": "Answering '{topic}' is mission-critical. Read the following solution immediately.",
                "persuasive": "Once you hear the true answer to '{topic}', it will completely change your perspective.",
                "informative": "To answer '{topic}', we must look at the empirical data and established facts.",
                "empathetic": "Lots of people struggle with '{topic}'. Don't worry, the answer is simpler than you think!"
            }
        },
        "email writing": {
            "topics": ["cold email to a recruiter", "follow up after an interview", "asking for a deadline extension", "resigning from current position", "inviting a colleague to lunch", "complaining to customer service", "requesting a letter of recommendation", "announcing a new product launch", "welcoming a new team member", "canceling a subscription"],
            "templates": {
                "casual": "Hey there! Just dropping a quick note regarding {topic}. Talk soon!",
                "professional": "Dear recipient, I am writing to discuss {topic}. I look forward to your prompt response.",
                "sarcastic": "To whom it may concern, per my last email regarding {topic}, I eagerly await the impossible.",
                "enthusiastic": "Hello!! I am so incredibly excited to reach out about {topic} today! 🎉",
                "formal": "Dear Sir/Madam, please be advised of the following correspondence regarding {topic}.",
                "humorous": "Greetings from my chaotic inbox to yours! Wanted to briefly touch on {topic} before the coffee wears off.",
                "urgent": "URGENT: Please review the attached details regarding {topic} immediately.",
                "persuasive": "I'm reaching out about {topic} because I know this is an opportunity neither of us can afford to miss.",
                "informative": "I am providing an update on {topic}. Please find all the necessary contextual details below.",
                "empathetic": "I completely understand if you're swamped today, but I wanted to gently bump this note about {topic}."
            }
        },
        "product description": {
            "topics": ["noise-cancelling headphones", "smart coffee mug", "waterproof tent", "ergonomic office chair", "mechanical keyboard", "minimalist wallet", "powerful blender", "solar-powered power bank", "robotic vacuum cleaner", "stainless steel water bottle"],
            "templates": {
                "casual": "Check out this {topic}. It's super handy and looks great on your desk.",
                "professional": "The new {topic} is engineered for maximum performance and unparalleled reliability.",
                "sarcastic": "Behold the {topic}. Because clearly, the fifty other versions you bought weren't good enough.",
                "enthusiastic": "You will ABSOLUTELY ADORE this {topic}! It's the best thing we've ever launched! 😍",
                "formal": "Presenting the {topic}: crafted with premium materials to meet exacting specifications.",
                "humorous": "By buying this {topic}, you are essentially buying happiness. Or at least a brief distraction.",
                "urgent": "Buy this {topic} right now. Stock is running dangerously low and it will sell out today!",
                "persuasive": "You spend half your life working. You owe it to yourself to get this {topic} to drastically improve your day.",
                "informative": "This {topic} features a specialized design optimized for 20% greater efficiency than previous models.",
                "empathetic": "We know finding the right gear is frustrating, which is why we built this {topic} specifically with your comfort in mind."
            }
        }
    }

    dataset = []
    
    # Generate exactly 600 unique samples
    for category_name, content_data in categories.items():
        topics = content_data["topics"]
        templates = content_data["templates"]
        
        for topic in topics:
            for tone, template in templates.items():
                
                # Create the natural language instruction
                instruction = f"Write a {tone} {category_name} about {topic}."
                if category_name == "Q&A" or category_name == "summarization":
                    instruction = f"Provide a {tone} {category_name} regarding: {topic}."
                
                # Fill the predefined high-quality template
                generated_content = template.format(topic=topic)
                
                # Create structured output
                output_json = {
                    "task": category_name,
                    "content": generated_content,
                    "tone": tone,
                    "format": "json"
                }
                
                sample = {
                    "instruction": instruction,
                    "input": "",
                    "output": output_json
                }
                
                dataset.append(sample)

    # Shuffle to ensure diversity is spread evenly
    random.seed(42)
    random.shuffle(dataset)
    
    # Write full dataset
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    full_path = os.path.join(data_dir, "dataset.json")
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)
        
    # Split 80/20
    split_idx = int(len(dataset) * 0.8)
    train_data = dataset[:split_idx]
    test_data = dataset[split_idx:]
    
    with open(os.path.join(data_dir, "train.json"), "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=4)
    with open(os.path.join(data_dir, "test.json"), "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=4)
        
    print(f"Dataset Generation Complete!")
    print(f"Total Samples: {len(dataset)}")
    print(f"Train Size: {len(train_data)}")
    print(f"Test Size: {len(test_data)}")
    
    # Dataset Analysis (Diversity Check)
    print("\n[ Dataset Analysis ]")
    cat_counts = {}
    tone_counts = {}
    length_counts = []
    
    for item in dataset:
        cat = item['output']['task']
        tone = item['output']['tone']
        content_len = len(item['output']['content'].split())
        
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        tone_counts[tone] = tone_counts.get(tone, 0) + 1
        length_counts.append(content_len)
        
    print("-" * 30)
    print("Category Balance:")
    for c, count in cat_counts.items():
        print(f"  {c}: {count}")
    print("\nTone Balance:")
    for t, count in tone_counts.items():
        print(f"  {t}: {count}")
    print("\nContent Length Diversity:")
    print(f"  Average Words per Response: {sum(length_counts) / len(length_counts):.1f}")
    print(f"  Min Words: {min(length_counts)}")
    print(f"  Max Words: {max(length_counts)}")
    print("-" * 30)
    print("Files saved to 'data/' folder.")

if __name__ == "__main__":
    generate_dataset()
