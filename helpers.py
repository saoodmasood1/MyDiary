def analyze_mood(text):
    text = text.lower()

    # Expanded Neural Vocabulary for 12 Moods
    mood_map = {
        "Joyful": ["happy", "excited", "great", "glad", "awesome", "cheerful", "delighted", "overjoyed", "jubilant", "wonderful", "fantastic", "ecstatic", "beaming", "radiant"],
        "Anxious": ["worried", "nervous", "stressed", "panic", "scared", "uneasy", "apprehensive", "restless", "jittery", "tense", "overwhelmed", "fret", "dread", "shaking"],
        "Angry": ["mad", "furious", "annoyed", "frustrated", "hate", "angry", "irritable", "enraged", "resentful", "livid", "bitter", "pissed", "outraged", "spiteful"],
        "Sad": ["depressed", "lonely", "unhappy", "crying", "miserable", "sad", "gloomy", "heartbroken", "sorrow", "melancholy", "devastated", "tearful", "low", "unfocused"],
        "Peaceful": ["calm", "relaxed", "serene", "chill", "peace", "tranquil", "composed", "placid", "untroubled", "still", "quiet", "mellow", "harmonious", "contented"],
        "Tired": ["exhausted", "sleepy", "drained", "weak", "tired", "fatigued", "lethargic", "weary", "burnt", "sleep-deprived", "drowsy", "low-energy", "slug", "worn"],
        "Lonely": ["isolated", "ignored", "empty", "alone", "lonely", "abandoned", "forgotten", "unloved", "withdrawn", "distant", "secluded", "lonesome"],
        "Confident": ["strong", "ready", "capable", "proud", "bold", "empowered", "determined", "assured", "fearless", "unstoppable", "worthy", "certain", "heroic", "mighty"],
        "Confused": ["lost", "unsure", "puzzled", "conflicted", "confused", "disoriented", "bewildered", "perplexed", "doubtful", "unclear", "muddled", "stuck"],
        "Grateful": ["thankful", "blessed", "appreciate", "lucky", "grateful", "indebted", "praise", "valued", "humbled", "admire", "cherish"],
        "Hopeful": ["optimistic", "believe", "hope", "forward", "encouraged", "positive", "expectant", "promising", "reassured", "trusting", "ambitious"],
        "Inspired": ["creative", "motivated", "idea", "spark", "vision", "inspired", "artistic", "inventive", "fascinated", "driven", "awakened", "stimulated", "genius"]
    }

    # Advanced Intensity Modifiers
    intensifiers = {
        "very": 1.5, "extremely": 2.0, "really": 1.3, "totally": 1.4,
        "absolutely": 2.0, "completely": 1.8, "slightly": 0.5, "barely": 0.4
    }

    scores = {mood: 0 for mood in mood_map}
    words = text.replace(".", "").replace("!", "").replace(",", "").split()

    found_any = False
    for i, word in enumerate(words):
        for mood, keywords in mood_map.items():
            if word in keywords:
                found_any = True
                weight = 1.0
                # Look-back logic for intensifiers
                if i > 0 and words[i-1] in intensifiers:
                    weight = intensifiers[words[i-1]]
                scores[mood] += weight

    if not found_any:
        return {"primary_mood": "Neutral", "confidence": 50.0}

    primary = max(scores, key=scores.get)
    total_val = sum(scores.values())
    confidence = round((scores[primary] / total_val * 100), 1)

    return {"primary_mood": primary, "confidence": min(confidence, 100.0)}
