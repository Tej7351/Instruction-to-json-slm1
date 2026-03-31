import os
import json
import random
import itertools

def generate_v3():
    # 6 tasks exactly
    tasks = ["tweet", "linkedin_post", "summarization", "qa", "email", "product_description"]
    
    # 10 tones mapped into 3 style groups to ensure realistic combinations
    tone_groups = {
        "GroupA": ["professional", "formal", "informative"],
        "GroupB": ["casual", "humorous", "sarcastic"],
        "GroupC": ["enthusiastic", "persuasive", "empathetic", "urgent"]
    }
    
    # We will define a massive combinatorial dictionary
    # For each task, for each group, we define at least 3 topics, 3 hooks, 3 bodies, 3 conclusions.
    # 3x3x3x3 = 81 combinations per group per task. 81 x 3 groups = 243 combinations per task > 100 needed!
    
    data_pool = {
        "tweet": {
            "GroupA": {
                "topics": ["AI integration", "cloud cost optimization", "technical debt", "system architecture"],
                "hooks": ["Recent analyses show a definitive shift toward {topic} in enterprise software.", "The industry conversation around {topic} is evolving rapidly.", "We need to critically evaluate how we approach {topic} today.", "When discussing {topic}, engineers often overlook the long-term maintenance costs."],
                "bodies": ["Implementing scalable solutions requires more than just adding layers of abstraction; it demands rigorous testing.", "Consistent monitoring and refactoring are essential to maintain performance benchmarks.", "Data indicates that teams prioritizing this metric ship 30% faster with fewer regressions.", "The fundamental challenge lies in balancing immediate feature delivery with sustainable engineering practices."],
                "conclusions": ["Strategic planning remains the most effective mitigation strategy.", "I highly recommend reading the latest whitepapers on this architectural pattern.", "Continuous learning is mandatory for mitigating these risks.", "What are your team's current strategies for handling this?"]
            },
            "GroupB": {
                "topics": ["late night debugging", "broken production", "learning JavaScript", "excessive coffee"],
                "hooks": ["Just spent four hours staring at the same line of code related to {topic}.", "Nothing quite like the utter panic of {topic} right before the weekend.", "My entire personality at this point is just {topic} and hoping for the best.", "If I have to deal with {topic} one more time today, I might actually cry."],
                "bodies": ["At some point, the syntax just starts looking like ancient hieroglyphics.", "I'm convinced the compiler is just judging my life choices instead of actually running the build.", "Just going to add a few console logs and pray to the engineering gods that it suddenly works.", "Turns out the bug was literally a missing comma. I am a genius with zero brain cells."],
                "conclusions": ["Time to close the laptop and pretend today never happened.", "Send help, or at least a very large espresso.", "Can someone please reboot the simulation? 😅", "I love software engineering. Totally fine. Everything is fine. 🤡"]
            },
            "GroupC": {
                "topics": ["shipping a side project", "getting your first dev job", "mastering Python", "the magic of Open Source"],
                "hooks": ["I am beyond incredibly excited to finally share my thoughts on {topic}!!", "If you are struggling with {topic} right now, please know that you are not alone!", "Stop whatever you are doing and pay attention to {topic} because it is a total game changer!", "The absolute joy of fully experiencing {topic} for the first time is unmatched! 🚀"],
                "bodies": ["The community support has been overwhelmingly positive and I am learning so much every single day.", "It takes immense courage to put your work out there, but the resulting growth makes every late night worth it.", "You absolutely owe it to your future self to invest the time required to understand this deeply.", "Every single failure is just a stepping stone directly leading to your ultimate breakthrough."],
                "conclusions": ["Keep pushing forward, you have entirely got this! ❤️", "I cannot wait to see what incredible things we all build next!!", "Do not give up; consistency is the key to unlocking your potential!", "Jump in today and transform your trajectory forever! 🔥"]
            }
        },
        "linkedin_post": {
            "GroupA": {
                "topics": ["completing an internship", "passing an AWS certification", "cross-functional collaboration", "leading a backend migration"],
                "hooks": ["I am pleased to formally announce my recent achievements regarding {topic}.", "Reflecting on the past quarter, my experience with {topic} has provided profound professional insights.", "The modern enterprise environment necessitates a rigorous approach to {topic}.", "It is a privilege to share my latest professional milestone involving {topic}."],
                "bodies": ["By leveraging structured methodologies, our team successfully exceeded our Q3 performance KPIs by over 15%.", "The strategic implementation of microservices allowed us to reduce latency while simultaneously decreasing server overhead.", "Collaborating with brilliant cross-functional stakeholders fundamentally improved the project's long-term viability.", "Rigorous technical training and continuous adaptation were the core drivers of this successful initiative."],
                "conclusions": ["I look forward to applying these advanced paradigms in my future endeavors.", "A sincere thank you to my mentors and colleagues for their invaluable guidance throughout this process.", "I am eager to leverage this expertise to drive measurable value in my next role.", "Continuous professional development remains the cornerstone of a successful engineering career."]
            },
            "GroupB": {
                "topics": ["working from home in pajamas", "imposter syndrome flare-ups", "understanding Git rebase", "the reality of tech interviews"],
                "hooks": ["Let's be completely honest for a second about {topic}.", "Because you definitely needed another long post on your feed about {topic}, right?", "They say {topic} builds character, but mostly it just builds my stress levels.", "My absolute favorite part of the week is unexpectedly dealing with {topic}. Totally."],
                "bodies": ["Between the endless Zoom calls and trying to remember how to exit Vim, it's a miracle I get anything done.", "I spent six hours prepping for a technical screen only to forget how to write a simple for-loop when someone was watching.", "At this point, my primary skill is expertly Googling error messages and copying the top StackOverflow answer.", "We all pretend we know what we're doing, but under the hood it's just duct tape and a dream."],
                "conclusions": ["If you relate to this, let's grab coffee and complain together.", "Just a reminder that nobody actually has it all figured out. Stay humble, folks.", "May your coffee be strong and your deployments oddly bug-free today. ☕", "Anyway, back to staring at my monitor until the code fixes itself."]
            },
            "GroupC": {
                "topics": ["landing your first tech role", "mentoring junior developers", "building inclusive teams", "the power of networking"],
                "hooks": ["I am so incredibly proud to finally share my amazing journey with {topic}!!", "If there is one thing I absolutely want you to take away today, it is the importance of {topic}!", "Please do not ever underestimate the massive, life-changing impact of {topic}!", "My heart is so full of gratitude today as I reflect deeply on {topic}. 🌟"],
                "bodies": ["Seeing someone else succeed because you took five minutes to offer guidance is the most rewarding feeling in the world.", "When we lift each other up and share our knowledge openly, the entire tech community becomes infinitely stronger.", "You have so much unique value to offer, and your voice truly deserves to be heard in this industry.", "The connections I have made recently have pushed me to break past my limits and achieve things I never thought possible."],
                "conclusions": ["Keep believing in yourself and never stop reaching out to others! 💪", "I am so excited for the future and I am rooting for every single one of you!", "Let's continue to build a tech ecosystem that empowers everyone to thrive! ❤️", "Your breakthrough is coming faster than you think—do not lose hope! 🚀"]
            }
        },
        "summarization": {
            "GroupA": {
                "topics": ["the 2008 financial crisis", "the theory of relativity", "the architectural pattern of microservices", "the history of the Roman Empire"],
                "hooks": ["An executive summary of {topic} reveals several critical foundational shifts.", "To succinctly summarize {topic}, one must examine the underlying systemic dependencies.", "The historical and structural analysis of {topic} provides a clear timeline of events.", "A comprehensive overview of {topic} demonstrates the multifaceted nature of the subject."],
                "bodies": ["Fundamentally, the subject matter revolves around the complex interactions between distributed entities and varying environmental pressures.", "Primary catalysts initiated a cascading reaction that ultimately redefined the existing operational boundaries.", "The period was characterized by rapid expansion, followed inevitably by catastrophic structural adjustments.", "Key stakeholders failed to implement necessary regulatory measures, leading to an inevitable system-wide failure."],
                "conclusions": ["In conclusion, the resultant paradigm established the framework for all modern subsequent policies.", "Consequently, understanding these fundamental principles is requisite for avoiding similar historical pitfalls.", "The lasting legacy remains a testament to the importance of sustainable, measured growth.", "Ultimately, the core concepts detailed continue to heavily influence contemporary methodologies."]
            },
            "GroupB": {
                "topics": ["the plot of The Matrix", "the storyline of Romeo and Juliet", "a 3-hour corporate meeting", "how the internet works"],
                "hooks": ["Basically, {topic} boils down to this: a lot of stuff happens for very little reason.", "To sum up {topic} for you: everything is a mess and nobody knows what's going on.", "Here is the absolute shortest summary of {topic} imaginable.", "If you really need to know about {topic}, just lower your expectations right now."],
                "bodies": ["A bunch of people made some incredibly poor decisions and just kept doubling down on them until everything exploded.", "It's essentially just magic tubes moving cat pictures around the globe while we all pretend it makes sense.", "Two groups of people refused to communicate properly, leading to a largely avoidable disaster that took way too long to resolve.", "Our protagonist realizes reality is a lie, puts on some cool sunglasses, and fights guys in suits using slow-motion kung fu."],
                "conclusions": ["And that's pretty much it—you really didn't miss much.", "In short, it was incredibly long, mostly pointless, and could have been an email.", "So yeah, just try not to think about the plot holes too much.", "Summarizing it actually makes it sound way cooler than it really is."]
            },
            "GroupC": {
                "topics": ["the benefits of solar energy", "the impact of artificial intelligence", "the process of photosynthesis", "the moon landing"],
                "hooks": ["The absolute most incredible summary of {topic} you will ever read is right here!", "You absolutely must understand {topic} because it is entirely changing the world as we know it!", "I am so excited to quickly break down the sheer magic of {topic} for you!", "The TL;DR on {topic} is simply mind-blowing from start to finish! 🌍"],
                "bodies": ["By harnessing unbelievable natural resources, this astonishing process generates pure, limitless potential that sustains our entire planet.", "The sheer scale of human ingenuity required to accomplish this feat is nothing short of a total modern miracle.", "It transforms literal sunlight and basic elements into the vibrant, life-giving energy that powers our existence.", "Decades of relentless innovation culminated in a breakthrough that instantly redefined the boundaries of what is possible."],
                "conclusions": ["It is genuinely one of the most fascinating phenomena in the entire universe!", "Understanding this completely changes how you view the beauty of the world around us!", "We are living in an era of unprecedented miracles, and this proves it perfectly! 🌟", "I strongly urge you to look deeper into this; it will absolutely inspire you!"]
            }
        },
        "qa": {
            "GroupA": {
                "topics": ["What is object-oriented programming?", "What is the speed of light?", "How does a blockchain work?", "What causes a solar eclipse?"],
                "hooks": ["Regarding your inquiry about '{topic}', the academic consensus provides a definitive explanation.", "To properly answer the question '{topic}', we must examine the underlying scientific principles.", "The formal definition of '{topic}' is thoroughly documented in modern literature.", "Answering the query '{topic}' requires an understanding of foundational continuous mechanics."],
                "bodies": ["It relies on encapsulating distinct state and behavior into structured entities to promote modularity and code reuse.", "The fundamental mechanism involves a decentralized, immutable ledger where cryptographic validation ensures transactional integrity.", "It occurs when a celestial body obscures the illumination of another, projecting a shadow upon the planetary surface.", "This physical constant is universally recognized as approximately 299,792,458 meters per second in a perfect vacuum constraint."],
                "conclusions": ["This core concept underpins the entirety of modern theoretical frameworks in the field.", "Understanding this mechanism is essential for advanced study and practical application.", "Consequently, rigorous mathematical modeling is required to accurately predict these outcomes.", "I trust this clarification thoroughly addresses your technical inquiry."]
            },
            "GroupB": {
                "topics": ["How do you boil an egg?", "Why is the sky blue?", "What is the capital of France?", "Who wrote Hamlet?"],
                "hooks": ["Great question about '{topic}'! Honestly, it's way simpler than you'd think.", "Oh, '{topic}'? Let me Google that incredibly baffling mystery for you.", "If I had a dollar for every time someone asked '{topic}', I'd be rich. Anyway, here you go.", "You're wondering '{topic}'? Let me break it down without all the boring jargon."],
                "bodies": ["Just put the thing in hot water, wait about 10 minutes, and try not to burn the kitchen down.", "The atmosphere scatters the sunlight around, and our silly human eyes just happen to pick up the blue part the best.", "A British guy with a fancy collar wrote it a few hundred years ago, and high schoolers have been suffering to read it ever since.", "It's literally just Paris. That's it. That's the whole answer."],
                "conclusions": ["Congratulations, you are now officially an expert.", "And no, you don't need a PhD to figure that out.", "Hopefully that clears things up so you don't have to ask Reddit.", "Pretty straightforward, right?"]
            },
            "GroupC": {
                "topics": ["How do vaccines work?", "What is the largest mammal on Earth?", "How far is the moon?", "What makes rainbows form?"],
                "hooks": ["I LOVE answering the question '{topic}'! Let me tell you all the amazing details!", "You asked '{topic}'? Get ready, because the answer is absolutely fascinating!", "This is such a beautiful question! Let me passionately explain '{topic}' for you!", "Don't worry if you don't know '{topic}'; I am thrilled to help you understand it completely! 🌈"],
                "bodies": ["They gently teach your immune system exactly how to fight off invaders, building a brilliant natural defense shield for your body!", "It is the magnificent Blue Whale, an unbelievably massive creature whose heart is literally the size of a car!", "It is roughly 238,900 miles away, a staggering distance that humanity bravely crossed through sheer willpower and innovation!", "When sunlight hits tiny, beautiful raindrops just right, it wonderfully bends and scatters into a spectacular spectrum of vibrant colors!"],
                "conclusions": ["Isn't the natural world just completely astonishing?! ✨", "I hope this brilliantly illuminates the topic for you, because it is truly magical!", "You can now share this incredible fact with everyone you know!", "Keep asking wonderful questions; curiosity is the greatest gift we have!"]
            }
        },
        "email": {
            "GroupA": {
                "topics": ["cold outreach to a recruiter", "resigning from a corporate position", "requesting a deadline extension", "announcing a new product launch"],
                "hooks": ["Dear recipient, I am writing to formally discuss matters pertaining to {topic}.", "To Whom It May Concern, please accept this correspondence regarding {topic}.", "I am reaching out today to provide a necessary administrative update on {topic}.", "Please review the following formal documentation addressing {topic}."],
                "bodies": ["My extensive background in scalable infrastructure uniquely positions me to drive appreciable value for your engineering department.", "Due to unforeseen scheduling conflicts and rigorous quality assurance standards, an adjustment to the current delivery timeline is necessary.", "This communication serves as my official two-week notice, during which I will diligently facilitate a comprehensive transition of my duties.", "Our latest iteration incorporates advanced cryptographic protocols designed to optimize enterprise-level security paradigms."],
                "conclusions": ["I anticipate your prompt response and look forward to our continued fruitful collaboration.", "Please advise at your earliest convenience if further elaboration is required.", "I extending my sincere gratitude for your professional support during this tenure.", "Thank you for your immediate attention to this pressing corporate matter."]
            },
            "GroupB": {
                "topics": ["inviting a colleague to lunch", "complaining about the office AC", "following up on a ignored message", "sending a meme to the team chat"],
                "hooks": ["Hey! Just dropping a super quick note about {topic}.", "Per my absolute last email regarding {topic}, I am once again begging for an answer.", "Greetings from my chaotic inbox! Wanted to briefly touch on {topic}.", "I know you're busy, but we seriously need to talk about {topic} today. 😂"],
                "bodies": ["If I have to sit in this freezing office for one more hour, I am going to turn into a literal block of ice.", "I'm heading out to grab some tacos down the street in about ten minutes if you want to escape the screen for a bit.", "I attached the file again just in case the internet gremlins magically deleted it from your inbox yesterday.", "Honestly, I have no idea how this code is still running, but I'm not going to touch it on a Friday afternoon."],
                "conclusions": ["Let me know if you survive the afternoon meetings!", "Talk soon, assuming I don't freeze to death first.", "Ping me on Slack whenever you finally have a second to breathe.", "Cheers, and good luck with the rest of your week."]
            },
            "GroupC": {
                "topics": ["welcoming a new team member", "congratulating a coworker on a promotion", "thanking a mentor for their time", "celebrating a successful project launch"],
                "hooks": ["Hi everyone!! I am so incredibly excited to reach out today regarding {topic}! 🎉", "I am absolutely thrilled to be writing to you about {topic}!!", "I just had to send a quick note because I am pouring over with gratitude regarding {topic}! ❤️", "Please drop everything you are doing so we can urgently celebrate {topic} together!"],
                "bodies": ["Your relentless dedication and brilliant positive energy have completely transformed the dynamic of our entire workspace!", "We are so unbelievably lucky to have someone with your exceptional talent and warm personality joining our fast-paced family!", "I cannot express enough how much your patient guidance has fundamentally shaped my confidence and career trajectory!", "Watching this initiative finally go live after months of passionate hard work is simply the most rewarding feeling ever!"],
                "conclusions": ["I cannot wait to see all the absolutely phenomenal things we will accomplish together next! 🚀", "Thank you from the bottom of my heart for being so incredibly amazing!", "Please take a moment to be immensely proud of yourself today—you earned it!", "Sending you the biggest virtual high-five ever! Let's keep winning!"]
            }
        },
        "product_description": {
            "GroupA": {
                "topics": ["noise-cancelling headphones", "smart coffee mug", "ergonomic office chair", "mechanical keyboard"],
                "hooks": ["The newly engineered {topic} is designed for maximum performance and unparalleled reliability.", "Presenting the {topic}: crafted with premium materials to meet exacting specifications.", "Our flagship {topic} incorporates cutting-edge technology to drastically attenuate environmental friction.", "This iteration of the {topic} establishes a new benchmark for enterprise-grade productivity tools."],
                "bodies": ["Featuring proprietary heat-retention algorithms and a sleek minimalist chassis, it maintains optimal conditions for extended durations.", "The dynamic structural articulation and highly adjustable multi-directional components conform precisely to the user's operational requirements.", "Constructed from aerospace-grade aluminum and equipped with high-fidelity active sensors, it delivers a deeply immersive user experience.", "It utilizes advanced Bluetooth 5.2 connectivity and specialized acoustic isolation to ensure latency-free, crystalline transmissions."],
                "conclusions": ["Upgrade your professional workflow with a tool built for uncompromising durability.", "Experience the pinnacle of specialized craftsmanship and precise engineering today.", "It represents a prudent long-term investment for the discerning and demanding consumer.", "Review the technical specifications further to understand its full operational capacity."]
            },
            "GroupB": {
                "topics": ["novelty desk toy", "giant water bottle", "overpriced wallet", "USB blanket"],
                "hooks": ["Check out this {topic}. It's honestly super handy and looks great on your desk.", "Behold the {topic}. Because clearly, the fifty other versions you bought weren't good enough.", "By buying this {topic}, you are essentially buying a brief distraction from your daily responsibilities.", "This {topic} is so comfortable it might actually become a severe problem for your social life. 😅"],
                "bodies": ["It holds an absurd amount of liquid so you don't have to keep standing up and pretending to be active during the workday.", "It features fourteen different adjustment levers, absolutely none of which you will ever fully understand how to use.", "Just plug it into your laptop and instantly stop shivering while your office blasted the AC in the middle of December.", "It's small, holds precisely three cards, and ensures you can never carry cash again. True minimalist luxury."],
                "conclusions": ["Buy it today so you can finally successfully ignore everyone around you.", "Your lower back will supposedly thank you, probably.", "We are not legally responsible if you refuse to ever leave your desk again.", "Honestly, just treat yourself. You survived another week."]
            },
            "GroupC": {
                "topics": ["orthopedic seat cushion", "solar-powered power bank", "HD webcam", "blue-light blocking glasses"],
                "hooks": ["You will ABSOLUTELY ADORE this {topic}! It's the best thing we have ever launched! 😍", "Say goodbye to your daily frustrations FOREVER with this magical {topic}!! 🌟", "Act fast! This award-winning {topic} is flying off the shelves and you desperately need it!", "We know finding the right gear is exhausting, which is why we built this amazing {topic} specifically for you! ❤️"],
                "bodies": ["This astonishing invention will completely eliminate your eye strain and leave you feeling wonderfully refreshed after a long shift!", "It harnesses the literal power of the sun to ensure your absolutely vital devices never, ever run out of battery again!", "With endless adjustability and incredible supportive contours, you will actually be genuinely excited to sit down and work every single day!", "We thoughtfully designed every single inch of this product to provide a incredibly soft, comforting sanctuary for your mind and body."],
                "conclusions": ["You owe it to yourself to experience this life-changing comfort immediately! 🚀", "Grab yours right now to secure the phenomenal quality you truly deserve!", "Investing in this is the absolute best decision you will make for your health this year!", "Slip them on and give yourself the brilliant, gentle break you have desperately needed! ✨"]
            }
        }
    }

    dataset = []

    # Let's generate 600 samples = 100 per task
    random.seed(42)

    for task in tasks:
        task_data = data_pool[task]
        task_samples = []
        
        # We need 100 samples per task. We have roughly 3 groups. So ~33 samples per group.
        # Inside each group, we have 4 topics and ~3 tones.
        # We will cycle through topics and tones to generate combinations.
        
        for group_name, group_content in task_data.items():
            tones = tone_groups[group_name]
            topics = group_content["topics"]
            hooks = group_content["hooks"]
            bodies = group_content["bodies"]
            conclusions = group_content["conclusions"]
            
            # Generate 34 samples per group to get 102 per task, then we trim to exactly 100.
            for i in range(34):
                tone = random.choice(tones)
                topic = random.choice(topics)
                hook = random.choice(hooks).format(topic=topic)
                body = random.choice(bodies).format(topic=topic)
                conclusion = random.choice(conclusions).format(topic=topic)
                
                content = f"{hook} {body} {conclusion}"
                
                # Instruction variations
                prompt_templates = [
                    f"Write a {tone} {task} about {topic}.",
                    f"Draft a {task} focusing on {topic}. Make it {tone}.",
                    f"Provide a {tone} {task} regarding: {topic}.",
                    f"Can you compose a {tone} {task} discussing {topic}?",
                    f"Create a {task} about {topic} in an {tone} style."
                ]
                instruction = random.choice(prompt_templates)
                
                sample = {
                    "instruction": instruction,
                    "input": "",
                    "output": {
                        "task": task,
                        "content": content,
                        "tone": tone,
                        "format": "json"
                    }
                }
                task_samples.append(sample)
        
        # Ensure exact 100
        random.shuffle(task_samples)
        dataset.extend(task_samples[:100])

    # Now we have exactly 600 unique samples.
    # Total combinations per group = 4 topics * 4 hooks * 4 bodies * 4 conclusions = 256. 
    # Because we pick randomly, the chance of exact duplication is extremely small.
    # We will deduplicate just to be absolutely certain.
    
    unique_dataset = []
    seen_contents = set()
    for item in dataset:
        if item["output"]["content"] not in seen_contents:
            unique_dataset.append(item)
            seen_contents.add(item["output"]["content"])
            
    # If we dropped any due to exact duplication (unlikely), print it.
    print(f"Total Unique Samples Generated: {len(unique_dataset)}")

    # Shuffle the final unique dataset
    random.shuffle(unique_dataset)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Save the 10-sample preview
    preview = unique_dataset[:10]
    preview_path = os.path.join(data_dir, "sample_preview.json")
    with open(preview_path, "w", encoding="utf-8") as f:
        json.dump(preview, f, indent=4)
        
    # Save full 600 properly
    full_path = os.path.join(data_dir, "dataset.json")
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(unique_dataset, f, indent=4)
        
    split_idx = int(len(unique_dataset) * 0.8)
    with open(os.path.join(data_dir, "train.json"), "w", encoding="utf-8") as f:
        json.dump(unique_dataset[:split_idx], f, indent=4)
    with open(os.path.join(data_dir, "test.json"), "w", encoding="utf-8") as f:
        json.dump(unique_dataset[split_idx:], f, indent=4)

    print("Phase 2 Augmentation Complete.")
    print(f"Generated {len(unique_dataset)} completely unique samples.")
    print(f"Saved preview of 10 samples to: {preview_path}")

if __name__ == "__main__":
    generate_v3()
