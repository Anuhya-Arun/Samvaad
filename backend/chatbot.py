
import random
import re
import unicodedata


# --------------------------------------------------
# TEXT PROCESSING
# --------------------------------------------------

def normalize(text):
    text = unicodedata.normalize("NFC", text.lower())
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def phrase_matches(text, phrase):
    """Match a complete phrase instead of part of another word."""
    phrase = normalize(phrase)

    if not phrase:
        return False

    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return bool(re.search(pattern, text))


def contains_any(text, phrases):
    return any(phrase_matches(text, phrase) for phrase in phrases)


# --------------------------------------------------
# PREDEFINED CONVERSATION TOPICS
# Every topic contains Sanskrit, English and 3
# suggested follow-up questions.
# --------------------------------------------------

TOPICS = {
    "greetings": {
        "keywords": [
            "hello", "hi", "hey", "greeting", "greetings",
            "namaste", "नमस्ते", "नमस्कार", "सुप्रभात",
            "good morning", "common Sanskrit greetings",
            "what are common Sanskrit greetings",
            "show me common Sanskrit greetings"
        ],
        "sanskrit": "नमस्ते! भवतः दिनं शुभं भवतु।",
        "english": (
            "Hello! May your day be happy and auspicious. "
            "नमस्ते is a common Sanskrit greeting."
        ),
        "questions": [
            "How do I say good morning?",
            "How do I ask how someone is?",
            "Translate: thank you"
        ]
    },

    "introduction": {
        "keywords": [
            "introduce myself", "introduction", "my name",
            "मम नाम", "परिचय", "your name", "who are you",
            "how do i introduce myself in sanskrit",
            "how do i say my name is"
        ],
        "sanskrit": "मम नाम संवादः अस्ति। भवतः नाम किम्?",
        "english": (
            "My name is Samvaad. What is your name? "
            "To introduce yourself, say: मम नाम ___ अस्ति।"
        ),
        "questions": [
            "How do I say my name is ...?",
            "How do I ask someone's name?",
            "Teach me Sanskrit pronouns"
        ]
    },

    "wellbeing": {
        "keywords": [
            "how are you", "are you fine", "कथम् अस्ति",
            "कथं अस्ति", "कुशल", "कथमसि",
            "how do i ask how someone is"
        ],
        "sanskrit": "अहं कुशली अस्मि। भवान् कथम् अस्ति?",
        "english": (
            "I am fine. How are you? "
            "अहं कुशली अस्मि means 'I am well.'"
        ),
        "questions": [
            "How do I say I am fine?",
            "How do I say thank you?",
            "Show me more greetings"
        ]
    },

    "thanks": {
        "keywords": [
            "thank you", "thanks", "धन्यवाद", "कृतज्ञ",
            "how do i say thank you"
        ],
        "sanskrit": "धन्यवादः!",
        "english": (
            "Thank you! धन्यवादः is a commonly used expression "
            "of gratitude in Sanskrit learning contexts."
        ),
        "questions": [
            "How do I say you're welcome?",
            "Teach me a polite phrase",
            "What does नमस्ते mean?"
        ]
    },

    "goodbye": {
        "keywords": [
            "goodbye", "bye", "see you", "पुनर्मिलामः",
            "पुनर्दर्शनाय"
        ],
        "sanskrit": "पुनर्मिलामः! भवतः दिनं शुभं भवतु।",
        "english": "Goodbye! See you again. Have a wonderful day.",
        "questions": [
            "How do I say good morning?",
            "Teach me a polite phrase",
            "Learn a new Sanskrit word"
        ]
    },

    "numbers": {
        "keywords": [
            "number", "numbers", "count", "counting",
            "संख्या", "गणना", "teach me numbers"
        ],
        "sanskrit": "एकम्, द्वे, त्रीणि, चत्वारि, पञ्च।",
        "english": (
            "Here are numbers one to five: "
            "एकम् (one), द्वे (two), त्रीणि (three), "
            "चत्वारि (four), and पञ्च (five). "
            "Sanskrit number forms can change with grammatical gender."
        ),
        "questions": [
            "Teach me Sanskrit colours",
            "Learn a new Sanskrit word",
            "How do I introduce myself?"
        ]
    },

    "family": {
        "keywords": [
            "family", "mother", "father", "brother", "sister",
            "माता", "पिता", "भ्राता", "भगिनी", "परिवार",
            "everyday words", "more everyday words"
        ],
        "sanskrit": (
            "माता, पिता, भ्राता, भगिनी च परिवारस्य सदस्याः सन्ति।"
        ),
        "english": (
            "माता means mother, पिता means father, "
            "भ्राता means brother, and भगिनी means sister."
        ),
        "questions": [
            "Teach me more everyday words",
            "Learn Sanskrit pronouns",
            "Translate: my name is"
        ]
    },

    "nature": {
        "keywords": [
            "nature", "sun", "moon", "water", "tree", "flower",
            "river", "earth", "sky", "सूर्य", "चन्द्र", "जल",
            "वृक्ष", "पुष्प", "नदी", "पृथ्वी", "आकाश",
            "nature words", "more nature words"
        ],
        "sanskrit": (
            "सूर्यः, चन्द्रः, नदी, वृक्षः, पुष्पम् च "
            "प्रकृतेः भागाः सन्ति।"
        ),
        "english": (
            "Some nature words are सूर्यः (sun), चन्द्रः (moon), "
            "नदी (river), वृक्षः (tree), पुष्पम् (flower), "
            "and जलम् (water)."
        ),
        "questions": [
            "Teach me Sanskrit colours",
            "Learn more nature words",
            "Teach me numbers"
        ]
    },

    "education": {
        "keywords": [
            "school", "book", "teacher", "student", "study",
            "learn", "knowledge", "विद्यालय", "पुस्तक",
            "गुरु", "विद्यार्थी", "विद्या", "पठ",
            "what can you teach me"
        ],
        "sanskrit": "विद्या ज्ञानं ददाति।",
        "english": (
            "विद्या ज्ञानं ददाति means 'Knowledge gives understanding.' "
            "पुस्तकम् means book, विद्यालयः means school, "
            "and गुरुः means teacher."
        ),
        "questions": [
            "Teach me common verbs",
            "Learn Sanskrit pronouns",
            "Learn a new Sanskrit word"
        ]
    },

    "colours": {
        "keywords": [
            "colour", "colors", "colours", "red", "blue",
            "green", "white", "black", "पीत", "रक्त", "नील",
            "हरित", "श्वेत", "कृष्ण", "teach me Sanskrit colours"
        ],
        "sanskrit": (
            "रक्तवर्णः, नीलवर्णः, हरितवर्णः, पीतवर्णः च।"
        ),
        "english": (
            "Some colour words are रक्त (red), नील (blue), "
            "हरित (green), पीत (yellow), श्वेत (white), "
            "and कृष्ण (black). Their endings may change "
            "according to grammatical gender and context."
        ),
        "questions": [
            "Teach me numbers",
            "Learn more nature words",
            "Learn a new Sanskrit word"
        ]
    },

    "pronouns": {
        "keywords": [
            "pronoun", "pronouns", "i", "you", "we",
            "अहम्", "त्वम्", "वयम्", "यूयम्",
            "learn Sanskrit pronouns"
        ],
        "sanskrit": "अहम्, त्वम्, वयम्, यूयम्।",
        "english": (
            "अहम् means I, त्वम् means you (singular), "
            "वयम् means we, and यूयम् means you (plural). "
            "Pronoun usage depends on the context."
        ),
        "questions": [
            "How do I introduce myself?",
            "Teach me common verbs",
            "Learn a new Sanskrit word"
        ]
    },

    "verbs": {
        "keywords": [
            "verb", "verbs", "read", "write", "go", "come",
            "eat", "speak", "पठामि", "लिखामि", "गच्छामि",
            "आगच्छ", "वद", "खाद", "teach me common verbs"
        ],
        "sanskrit": "अहं पठामि। अहं लिखामि। अहं गच्छामि।",
        "english": (
            "अहं पठामि means 'I read or study.' "
            "अहं लिखामि means 'I write.' "
            "अहं गच्छामि means 'I go.'"
        ),
        "questions": [
            "Learn Sanskrit pronouns",
            "Explain a simple Sanskrit sentence",
            "Learn a new Sanskrit word"
        ]
    },

    "grammar": {
        "keywords": [
            "grammar", "sentence", "noun", "case", "व्याकरण",
            "वाक्य", "explain", "अहं पठामि",
            "explain a simple Sanskrit sentence"
        ],
        "sanskrit": (
            "अहं पठामि। अत्र 'अहम्' कर्ता अस्ति, "
            "'पठामि' क्रियापदम् अस्ति।"
        ),
        "english": (
            "अहं पठामि means 'I read or study.' "
            "अहम् means 'I' and functions as the subject; "
            "पठामि means 'read or study' and is the verb."
        ),
        "questions": [
            "Teach me common verbs",
            "Learn Sanskrit pronouns",
            "Show me more greetings"
        ]
    },

    "pronunciation": {
        "keywords": [
            "pronounce", "pronunciation", "how to pronounce",
            "उच्चारण"
        ],
        "sanskrit": (
            "संस्कृतशब्दानाम् उच्चारणे स्वराणां "
            "व्यञ्जनानां च स्पष्टता महत्त्वपूर्णा अस्ति।"
        ),
        "english": (
            "Clear vowels and consonants are important in Sanskrit "
            "pronunciation. I can provide basic written guidance, "
            "but this chatbot does not generate audio."
        ),
        "questions": [
            "How do I pronounce नमस्ते?",
            "Learn a new Sanskrit word",
            "Show me common greetings"
        ]
    }
}


# --------------------------------------------------
# EXPANDED SANSKRIT VOCABULARY
# Format: Sanskrit word -> English meaning, topic
# --------------------------------------------------

VOCABULARY = {
    # Greetings and expressions
    "नमस्ते": ("Hello / Greetings", "greetings"),
    "नमस्कारः": ("Greetings / Salutations", "greetings"),
    "धन्यवादः": ("Thank you", "thanks"),
    "स्वागतम्": ("Welcome", "thanks"),
    "सुप्रभातम्": ("Good morning", "greetings"),
    "शुभरात्रिः": ("Good night", "goodbye"),
    "पुनर्मिलामः": ("See you again", "goodbye"),
    "कृपया": ("Please", "greetings"),
    "क्षम्यताम्": ("Please forgive / Excuse me", "greetings"),

    # Family and people
    "माता": ("Mother", "family"),
    "पिता": ("Father", "family"),
    "भ्राता": ("Brother", "family"),
    "भगिनी": ("Sister", "family"),
    "मित्रम्": ("Friend", "family"),
    "बालकः": ("Boy", "family"),
    "बालिका": ("Girl", "family"),
    "परिवारः": ("Family", "family"),
    "नरः": ("Man", "family"),
    "नारी": ("Woman", "family"),

    # Everyday objects and places
    "जलम्": ("Water", "nature"),
    "पुस्तकम्": ("Book", "education"),
    "गृहम्": ("House / Home", "family"),
    "विद्यालयः": ("School", "education"),
    "लेखनी": ("Pen", "education"),
    "द्वारम्": ("Door", "family"),
    "आसनम्": ("Seat", "family"),
    "वस्त्रम्": ("Clothing / Garment", "family"),
    "मार्गः": ("Road / Path", "nature"),
    "नगरम्": ("City", "nature"),

    # Education
    "विद्या": ("Knowledge / Learning", "education"),
    "गुरुः": ("Teacher", "education"),
    "विद्यार्थी": ("Student", "education"),
    "पाठशाला": ("School", "education"),
    "ज्ञानम्": ("Knowledge", "education"),
    "प्रश्नः": ("Question", "education"),
    "उत्तरम्": ("Answer", "education"),
    "भाषा": ("Language", "education"),
    "संस्कृतम्": ("Sanskrit", "education"),
    "शब्दः": ("Word", "education"),

    # Nature
    "फलम्": ("Fruit", "nature"),
    "पुष्पम्": ("Flower", "nature"),
    "वृक्षः": ("Tree", "nature"),
    "नदी": ("River", "nature"),
    "पर्वतः": ("Mountain", "nature"),
    "सूर्यः": ("Sun", "nature"),
    "चन्द्रः": ("Moon", "nature"),
    "पृथ्वी": ("Earth", "nature"),
    "आकाशः": ("Sky", "nature"),
    "वायुः": ("Air / Wind", "nature"),
    "अग्निः": ("Fire", "nature"),
    "समुद्रः": ("Ocean / Sea", "nature"),
    "वर्षा": ("Rain", "nature"),
    "मेघः": ("Cloud", "nature"),
    "पशुः": ("Animal", "nature"),
    "पक्षी": ("Bird", "nature"),

    # Food
    "अन्नम्": ("Food / Grain", "family"),
    "दुग्धम्": ("Milk", "family"),
    "फलानि": ("Fruits", "family"),
    "ओदनः": ("Cooked rice", "family"),
    "भोजनम्": ("Meal / Food", "family"),

    # Colours
    "रक्तः": ("Red (masculine form)", "colours"),
    "नीलः": ("Blue (masculine form)", "colours"),
    "हरितः": ("Green (masculine form)", "colours"),
    "पीतः": ("Yellow (masculine form)", "colours"),
    "श्वेतः": ("White (masculine form)", "colours"),
    "कृष्णः": ("Black (masculine form)", "colours"),

    # Numbers
    "एकम्": ("One", "numbers"),
    "द्वे": ("Two", "numbers"),
    "त्रीणि": ("Three", "numbers"),
    "चत्वारि": ("Four", "numbers"),
    "पञ्च": ("Five", "numbers"),
    "षट्": ("Six", "numbers"),
    "सप्त": ("Seven", "numbers"),
    "अष्ट": ("Eight", "numbers"),
    "नव": ("Nine", "numbers"),
    "दश": ("Ten", "numbers"),

    # Pronouns
    "अहम्": ("I", "pronouns"),
    "त्वम्": ("You (singular)", "pronouns"),
    "वयम्": ("We", "pronouns"),
    "यूयम्": ("You (plural)", "pronouns"),
    "सः": ("He / That (masculine)", "pronouns"),
    "सा": ("She / That (feminine)", "pronouns"),
    "तत्": ("It / That (neuter)", "pronouns"),

    # Common verbs
    "पठामि": ("I read / study", "verbs"),
    "लिखामि": ("I write", "verbs"),
    "गच्छामि": ("I go", "verbs"),
    "आगच्छामि": ("I come", "verbs"),
    "वदामि": ("I speak", "verbs"),
    "खादामि": ("I eat", "verbs"),
    "पिबामि": ("I drink", "verbs"),
    "पश्यामि": ("I see", "verbs"),
    "जानामि": ("I know", "verbs"),
    "क्रीडामि": ("I play", "verbs"),

    # Adjectives and abstract words
    "सुन्दरम्": ("Beautiful", "nature"),
    "लघु": ("Small / Short", "education"),
    "बृहत्": ("Big / Large", "education"),
    "नवीनम्": ("New", "education"),
    "पुरातनम्": ("Old / Ancient", "education"),
    "सुखम्": ("Happiness / Comfort", "wellbeing"),
    "दुःखम्": ("Sadness / Sorrow", "wellbeing"),
    "प्रेम": ("Love", "wellbeing"),
    "शान्तिः": ("Peace", "wellbeing"),
    "समयः": ("Time", "wellbeing"),

    # Question words
    "किम्": ("What?", "grammar"),
    "कः": ("Who? (masculine)", "grammar"),
    "का": ("Who? (feminine)", "grammar"),
    "कुत्र": ("Where?", "grammar"),
    "कदा": ("When?", "grammar"),
    "कथम्": ("How?", "grammar"),
    "कस्मात्": ("Why? / From what cause?", "grammar"),
}


# --------------------------------------------------
# PREDEFINED PHRASE TRANSLATIONS
# --------------------------------------------------

TRANSLATIONS = {
    "hello": (
        "नमस्ते।",
        "Hello."
    ),
    "hi": (
        "नमस्ते।",
        "Hello."
    ),
    "good morning": (
        "सुप्रभातम्।",
        "Good morning."
    ),
    "good afternoon": (
        "शुभमध्याह्नम्।",
        "Good afternoon. This is a simple learning phrase."
    ),
    "good night": (
        "शुभरात्रिः।",
        "Good night."
    ),
    "thank you": (
        "धन्यवादः।",
        "Thank you."
    ),
    "you are welcome": (
        "स्वागतम्।",
        "You are welcome."
    ),
    "please": (
        "कृपया।",
        "Please."
    ),
    "excuse me": (
        "क्षम्यताम्।",
        "Excuse me / Please forgive me."
    ),
    "goodbye": (
        "पुनर्मिलामः।",
        "Goodbye; see you again."
    ),
    "how are you": (
        "भवान् कथम् अस्ति? भवती कथम् अस्ति?",
        "How are you? भवान् is a respectful masculine form; "
        "भवती is a respectful feminine form."
    ),
    "i am fine": (
        "अहं कुशली अस्मि।",
        "I am fine."
    ),
    "my name is": (
        "मम नाम ___ अस्ति।",
        "My name is ___. Replace the blank with your name."
    ),
    "what is your name": (
        "भवतः नाम किम्? भवत्याः नाम किम्?",
        "What is your name? The Sanskrit form varies with the "
        "person being addressed."
    ),
    "i am a student": (
        "अहं विद्यार्थी अस्मि।",
        "I am a student. This example uses the masculine form विद्यार्थी."
    ),
    "i am happy": (
        "अहं प्रसन्नः अस्मि।",
        "I am happy. This example uses the masculine form प्रसन्नः."
    ),
    "water": (
        "जलम्।",
        "Water."
    ),
    "friend": (
        "मित्रम्।",
        "Friend."
    ),
    "book": (
        "पुस्तकम्।",
        "Book."
    ),
    "mother": (
        "माता।",
        "Mother."
    ),
    "father": (
        "पिता।",
        "Father."
    ),
    "peace": (
        "शान्तिः।",
        "Peace."
    ),
    "sun": (
        "सूर्यः।",
        "Sun."
    ),
    "moon": (
        "चन्द्रः।",
        "Moon."
    ),
    "i read": (
        "अहं पठामि।",
        "I read / study."
    ),
    "i write": (
        "अहं लिखामि।",
        "I write."
    ),
    "i go": (
        "अहं गच्छामि।",
        "I go."
    ),
    "i eat": (
        "अहं खादामि।",
        "I eat."
    ),
    "i drink": (
        "अहं पिबामि।",
        "I drink."
    ),
    "i speak": (
        "अहं वदामि।",
        "I speak."
    ),
}


# --------------------------------------------------
# RESPONSE BUILDERS
# --------------------------------------------------

def make_answer(sanskrit, english, questions=None):
    """Return a consistent bilingual answer and three suggestions."""
    default_questions = [
        "Show me common Sanskrit greetings",
        "Learn a new Sanskrit word",
        "Explain a simple Sanskrit sentence"
    ]

    selected_questions = list(questions or default_questions)[:3]

    while len(selected_questions) < 3:
        selected_questions.append(
            default_questions[len(selected_questions)]
        )

    return {
        "sanskrit": sanskrit,
        "english": english,
        "questions": selected_questions
    }


def topic_answer(topic_name):
    topic = TOPICS[topic_name]

    return make_answer(
        topic["sanskrit"],
        topic["english"],
        topic["questions"]
    )


def vocabulary_answer(word, meaning, topic_name):
    return make_answer(
        f"{word} — {meaning}",
        f"The Sanskrit word {word} means {meaning}.",
        TOPICS.get(topic_name, {}).get("questions")
    )


# --------------------------------------------------
# MAIN RULE-BASED CHATBOT
# --------------------------------------------------

def get_response(message):
    original = message.strip()
    text = normalize(original)

    if not text:
        return make_answer(
            "कृपया प्रश्नं लिखतु।",
            "Please type a question or select one of the suggested prompts."
        )

    # 1. Handle explicit translation requests first.
    translate_match = re.search(
        r"^(?:translate|sanskrit for|how do i say)\s*[:\-]?\s*(.+)$",
        text
    )

    if translate_match:
        phrase = translate_match.group(1).strip()

        for english_phrase in sorted(
            TRANSLATIONS,
            key=len,
            reverse=True
        ):
            if phrase_matches(phrase, english_phrase):
                sanskrit, english = TRANSLATIONS[english_phrase]

                return make_answer(
                    sanskrit,
                    english,
                    [
                        "How do I pronounce this?",
                        "Translate: thank you",
                        "Learn a new Sanskrit word"
                    ]
                )

        return make_answer(
            "क्षम्यताम्, एतस्य वाक्यस्य अनुवादः "
            "मम वर्तमानशब्दकोशे नास्ति।",
            "Sorry, that phrase is not in my predefined translation list yet. "
            "Try 'thank you', 'good morning', 'water', or 'I am fine'."
        )

    # 2. Answer meaning questions.
    meaning_match = re.search(
        r"^(?:what does|meaning of|define)\s+(.+?)(?:\s+mean)?$",
        text
    )

    if meaning_match:
        requested_word = meaning_match.group(1).strip()

        for word, (meaning, topic_name) in VOCABULARY.items():
            if requested_word == normalize(word):
                return make_answer(
                    f"{word} इत्यस्य अर्थः — {meaning}",
                    f"{word} means {meaning}.",
                    TOPICS[topic_name]["questions"]
                )

        if requested_word in TRANSLATIONS:
            sanskrit, english = TRANSLATIONS[requested_word]

            return make_answer(
                sanskrit,
                english,
                [
                    "How do I pronounce this?",
                    "Learn a new Sanskrit word",
                    "Show me common Sanskrit greetings"
                ]
            )

        return make_answer(
            "क्षम्यताम्, एषः शब्दः मम शब्दकोशे नास्ति।",
            "Sorry, that word is not in my current vocabulary. "
            "Try मित्रम्, जलम्, पुस्तकम्, सूर्यः, or विद्या."
        )

    # 3. Direct exact vocabulary lookup.
    for word, (meaning, topic_name) in VOCABULARY.items():
        if text == normalize(word):
            return vocabulary_answer(word, meaning, topic_name)

    # 4. Teach a random word when requested.
    if contains_any(text, [
        "teach me a new sanskrit word",
        "learn a new sanskrit word",
        "new sanskrit word",
        "word of the day",
        "आजतन शब्द"
    ]):
        word, (meaning, topic_name) = random.choice(
            list(VOCABULARY.items())
        )

        return make_answer(
            f"अद्यतनः शब्दः — {word}",
            f"Today's Sanskrit word is {word}, meaning '{meaning}'.",
            TOPICS[topic_name]["questions"]
        )

    # 5. Handle common question patterns.
    if contains_any(text, [
        "what can you do",
        "what can you teach me",
        "help",
        "साहाय्य",
        "सहायता"
    ]):
        return make_answer(
            "अहं संस्कृतशब्दान्, अभिवादनानि, सरलवाक्यानि च शिक्षयामि।",
            "I can help you explore Sanskrit vocabulary, greetings, "
            "simple translations, numbers, colours, and basic grammar. "
            "Choose one of the suggested questions to begin.",
            [
                "Show me common Sanskrit greetings",
                "Teach me a new Sanskrit word",
                "Explain a simple Sanskrit sentence"
            ]
        )

    # 6. Match predefined topics using whole-phrase matching.
    # Longer keywords are checked first to prefer more specific matches.
    for topic_name, topic in TOPICS.items():
        keywords = sorted(
            topic["keywords"],
            key=len,
            reverse=True
        )

        if contains_any(text, keywords):
            return topic_answer(topic_name)

    # 7. Bilingual fallback for unrecognized input.
    return make_answer(
        "क्षम्यताम्, अहं प्रश्नम् पूर्णतया न अवगच्छामि। "
        "कृपया अधः दत्तेषु प्रश्नेषु एकं चिनोतु।",
        "Sorry, I could not match that message to my predefined topics. "
        "You can choose a suggested question or try a common Sanskrit "
        "word, greeting, or phrase.",
        [
            "Show me common Sanskrit greetings",
            "Teach me a new Sanskrit word",
            "Explain a simple Sanskrit sentence"
        ]
    )


# --------------------------------------------------
# INITIAL SUGGESTIONS FOR THE WELCOME SCREEN
# --------------------------------------------------

def get_suggestions():
    return [
        "How do I introduce myself in Sanskrit?",
        "What are common Sanskrit greetings?",
        "Teach me a new Sanskrit word."
    ]
