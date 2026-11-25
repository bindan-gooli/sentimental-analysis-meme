import os
import sqlite3

DB_PATH = "/Users/bindanm/IndicSent-M/memes.db"

# 240 Curated, High-Quality, Linguistically Balanced Memes (48 per Language x 5 Languages)
# Exactly 80 Positive, 80 Neutral, 80 Negative (16 of each class per language)

UNIQUE_MEMES = [
    # =========================================================================
    # 1. TELUGU MEMES (16 Positive, 16 Neutral, 16 Negative)
    # =========================================================================
    # --- Telugu Positive (16) ---
    {"lang": "Telugu", "tag": "Tollywood Punch", "title": "First Try Compile Success", "caption": "వామ్మో! ఈ కోడ్ ఫస్ట్ అటెంప్ట్‌లోనే రన్ అయింది! 😂🔥", "emoji": "🤯", "sentiment": "positive", "slug": "ch"},
    {"lang": "Telugu", "tag": "Pushpa Vibe", "title": "Thaggedhe Le Deployment", "caption": "టెస్టింగ్ చేయకుండానే ప్రొడక్షన్ లో డిప్లాయ్ చేశాం.. తగ్గేదే లే! 🪓🔥", "emoji": "🪓", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Balayya Power", "title": "Single Click Bugfix", "caption": "సింగిల్ క్లిక్ తో 50 బగ్స్ క్లియర్ చేసి వీకెండ్ బిర్యానీ తింటున్న మూడ్ 🍗😎", "emoji": "🍗", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "RRR Celebration", "title": "Natu Natu Signoff", "caption": "క్లయింట్ సైలెంట్ గా సైన్ ఆఫ్ ఇచ్చేశాడు.. ఇక నాటు నాటు డాన్సే! 🕺🏆", "emoji": "🕺", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Weekend Vibe", "title": "Friday Logout Bliss", "caption": "శుక్రవారం సాయంత్రం 5 గంటలకు స్లాక్ లో ఆఫ్లైన్ పెట్టే ఆనందం వేరురా బాబు 🎉🍻", "emoji": "🎉", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Ali Comedy", "title": "Google Copy Paste Win", "caption": "ఇంటర్య్వూలో 5 ఇయర్స్ సీనియర్ డెవలపర్ అని చెప్పి.. గూగుల్ లో లూప్ ఎలా రాయాలో వెతుకుతున్న నేను 💻", "emoji": "💻", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Brahmi Joy", "title": "Appraisal Letter Received", "caption": "అనుకున్నదానికంటే ఎక్కువ హైక్ వచ్చింది.. ఇక పార్టీ టైమ్ రా బాబు! 🥳💰", "emoji": "🥳", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Mahesh Babu Swag", "title": "Clean Code Architecture", "caption": "నా కోడ్ చూసి సీనియర్ ఆర్కిటెక్ట్ కూడా ఫిదా అయ్యాడు.. అది నా బ్రాండ్! ✨💼", "emoji": "✨", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Chiranjeevi Energy", "title": "Feature Demo Roaring Success", "caption": "డెమో లో క్లయింట్ క్లాప్స్ కొట్టాడు.. సూపర్ హిట్ రా మామా! 👏🌟", "emoji": "👏", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Trivikram Dialouge", "title": "Elegant One Liner Fix", "caption": "మాటల్లో ప్రాస, కోడ్ లో లాజిక్.. రెండూ మనకు వెన్నతో పెట్టిన విద్య! 🎯💡", "emoji": "🎯", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Allu Arjun Style", "title": "Zero Bug Delivery", "caption": "స్ప్రింట్ పూర్తయింది, జీరో బగ్స్.. తగ్గేదే లే అసలు! 🚀🏆", "emoji": "🚀", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Hyd Biryani", "title": "Paradise Biryani Treat", "caption": "ప్రాజెక్ట్ డెలివరీ అయిపోయింది.. బావార్చి లో డబుల్ మసాలా బిర్యానీ పార్టీ! 🍲🤤", "emoji": "🍲", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "NTR Energy", "title": "Lightning Fast Query", "caption": "ఒక్క ఇండెక్స్ తో క్వెరీ స్పీడ్ 100 రెట్లు పెరిగింది.. రచ్చ రంబోలా! ⚡🔥", "emoji": "⚡", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Pawan Kalyan Craze", "title": "Gabbar Singh Review", "caption": "నా రివ్యూ వస్తే కామెంట్స్ ఉండవు.. కేవలం అప్రూవల్సే! 🦁🔥", "emoji": "🦁", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Venkatesh Comedy", "title": "Smooth Release No Tension", "caption": "ఈసారి ఎలాంటి టెన్షన్ లేకుండా ప్రొడక్షన్ రిలీజ్ అయిపోయింది భయ్యా! 🌈😄", "emoji": "🌈", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Relatable Tech", "title": "Bonus Credited Message", "caption": "అకౌంట్ లో బోనస్ క్రెడిట్ అయిందని మెసేజ్ వచ్చింది.. దిమ్మతిరిగి బొమ్మ కనిపించింది! 💸🥳", "emoji": "💸", "sentiment": "positive", "slug": "leo"},

    # --- Telugu Neutral (16) ---
    {"lang": "Telugu", "tag": "Hitec City IT", "title": "Rao Ramesh Philosophy", "caption": "లైఫ్ లో ఏదో సాధిద్దాం అనుకున్నాం.. కానీ రోజూ మీటింగ్స్ తోనే సరిపోతోంది 🥲", "emoji": "🧘", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "BTech Struggles", "title": "One Night Standup Study", "caption": "ఎగ్జామ్ ముందు రోజు రాత్రి: ఈ ఒక్క నైట్ చదివితే యూనివర్సిటీ టాపర్ అయిపోతాను! 📚", "emoji": "📚", "sentiment": "neutral", "slug": "fry"},
    {"lang": "Telugu", "tag": "Traffic Trauma", "title": "Gachibowli Flyover Traffic", "caption": "గచ్చిబౌలి ఫ్లైఓవర్ ట్రాఫిక్ లో కూర్చుని జీవితం మీద వేదాంతం ఆలోచించే క్షణాలు 🚗🛵", "emoji": "🚗", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Code Mystery", "title": "Working Code Don't Touch", "caption": "ఈ లైన్ ఎందుకు రాశానో నాకే తెలియదు, కానీ తీసేస్తే యాప్ మొత్తం క్రాష్ అవుతోంది! 🚫", "emoji": "🚫", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Family Drama", "title": "Relative Asking Salary", "caption": "చుట్టాలు వచ్చి: బాబు జీతం ఎంత అంటే.. ఇన్ కమ్ టాక్స్ ఆఫీసర్ లా చూస్తున్న వాళ్లు 🤐", "emoji": "🤐", "sentiment": "neutral", "slug": "sarcasticbear"},
    {"lang": "Telugu", "tag": "Corporate Reality", "title": "Daily Standup Update", "caption": "నిన్న ఏం చేశావు అంటే ఆలోచించడానికి ఐదు నిమిషాలు టైమ్ కావాలి మేనేజర్ గారూ ⏳📋", "emoji": "⏳", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Tea Break", "title": "Madhapur Chai Adda", "caption": "కోడ్ లో బగ్ రాలేదు కానీ చాయ్ తాగడానికి ఒక చిన్న కారణం దొరికింది ☕🫖", "emoji": "☕", "sentiment": "neutral", "slug": "kermit"},
    {"lang": "Telugu", "tag": "WFH Habit", "title": "Camera Off Sleeping", "caption": "ఆల్ హ్యాండ్స్ మీటింగ్ లో కెమెరా ఆఫ్ చేసి సైలెంట్ గా కాఫీ తాగుతున్న క్షణాలు ☕🛋️", "emoji": "☕", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Tech Update", "title": "New Framework Released", "caption": "నేను పాత ఫ్రేమ్‌వర్క్ నేర్చుకునేలోపు మార్కెట్ లోకి ఇంకో కొత్తది వచ్చేసింది 🔄💻", "emoji": "🔄", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Commute Story", "title": "Metro Route Routine", "caption": "రాయదుర్గం మెట్రో లో నిలబడి సీట్ కోసం ఎదురుచూసే దినచర్య 🚇🎧", "emoji": "🚇", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Lunch Decision", "title": "Mess Food vs Swiggy", "caption": "మధ్యాహ్నం ఏం తినాలి అని ఆలోచించడానికే ఒక గంట మీటింగ్ పడుతుంది 🍱🤔", "emoji": "🍱", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Weekend Plan", "title": "Saturday Sleep Goal", "caption": "ఈ శనివారం చాలా చదవాలి అనుకున్నాను కానీ మధ్యాహ్నం 12 వరకు నిద్రపోయాను 😴🛌", "emoji": "😴", "sentiment": "neutral", "slug": "cheems"},
    {"lang": "Telugu", "tag": "Documentation", "title": "Empty Readme File", "caption": "ఈ ప్రాజెక్ట్ కి డాక్యుమెంటేషన్ రాయడం అంటే హిమాలయాల్లో తపస్సు చేయడం లాంటిది 📄🏔️", "emoji": "📄", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Weather Talk", "title": "Hyderabad Rain Traffic", "caption": "చిన్న చినుకు పడగానే హైటెక్ సిటీ రోడ్లు చెరువుల్లా మారిపోయే చిత్రం 🌧️🚶‍♂️", "emoji": "🌧️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Sprint Planning", "title": "Story Point Estimation", "caption": "ఈ టాస్క్ కి 3 పాయింట్లా లేక 5 పాయింట్లా అని అందరూ సీరియస్ గా చర్చలు 🎲📊", "emoji": "🎲", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Gym Resolution", "title": "Monthly Subscription Reality", "caption": "జిమ్ ఫీజు కట్టేశాం.. కానీ వెళ్లింది మాత్రం మొదటి రోజే 🏋️‍♂️🤷‍♂️", "emoji": "🏋️‍♂️", "sentiment": "neutral", "slug": "cheems"},

    # --- Telugu Negative (16) ---
    {"lang": "Telugu", "tag": "Salary Sarcasm", "title": "1st vs 30th Reality", "caption": "జీతం పడ్డ మొదటి రోజు బాహుబలి.. నెల చివరి రోజు భిక్షాటన 💸😭", "emoji": "💸", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Corporate Chaos", "title": "Friday 6 PM Release", "caption": "ఫ్రైడే ఈవెనింగ్ 6 గంటలకు ప్రొడక్షన్ రిలీజ్ ప్లాన్ చేసిన మేనేజర్ ని చూస్తూ నేను 🚨💀", "emoji": "🚨", "sentiment": "negative", "slug": "sarcasticbear"},
    {"lang": "Telugu", "tag": "Client vs Dev", "title": "Sunil Confusion", "caption": "క్లయింట్ చెప్పిన రిక్వైర్మెంట్ vs నేను రాసిన కోడ్.. రెండింటికీ అసలు సంబంధమే లేదు! 🤷‍♂️", "emoji": "🤷‍♂️", "sentiment": "negative", "slug": "drake"},
    {"lang": "Telugu", "tag": "WFH Dilemma", "title": "Camera On Panic", "caption": "మేనేజర్: అందరూ కెమెరా ఆన్ చేయండి! మంచం మీద లుంగీతో పడుకున్న నేను 😱🛏️", "emoji": "😱", "sentiment": "negative", "slug": "ch"},
    {"lang": "Telugu", "tag": "Brahmi Tears", "title": "Merge Conflict Disaster", "caption": "500 ఫైల్స్ లో కాన్ఫ్లిక్ట్ వచ్చింది.. నా చేతులు వణికిపోతున్నాయి భయ్యా! 😭💻", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Prod Outage", "title": "Server Crash At Midnight", "caption": "రాత్రి 2 గంటలకు ఆన్-కాల్ పేజర్ మోగింది.. సర్వర్ మొత్తం డౌన్ అయిపోయింది 🚨💀", "emoji": "🚨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Appraisal Pain", "title": "1 Percent Hike Agony", "caption": "ఇంత కష్టపడితే ఇచ్చిన హైక్ 1 శాతం.. గుండె పగిలిపోయింది దేవుడా 💔💸", "emoji": "💔", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Interview Failure", "title": "Rejected In Round 4", "caption": "4 రౌండ్స్ అయ్యాక బడ్జెట్ లేదని రిజెక్ట్ చేశారు.. ఇంతకంటే ద్రోహం ఉందా! 😤🚪", "emoji": "😤", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Monday Gloom", "title": "Sunday Night Anxiety", "caption": "ఆదివారం రాత్రి 10 గంటలవగానే సోమవారం ఆఫీస్ గుర్తొచ్చి గుండెల్లో దడ మొదలైంది ⏰😰", "emoji": "😰", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Database Horror", "title": "Drop Table Without Where", "caption": "టెస్ట్ డీబీ అనుకుని ప్రొడక్షన్ డీబీ ని డ్రాప్ చేసేశాను.. కెరీర్ సమాప్తం! 💥😱", "emoji": "💥", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Overtime Burden", "title": "Midnight 3 AM Working", "caption": "అందరూ ప్రశాంతంగా నిద్రపోతుంటే నేను ఇక్కడ బగ్స్ కోసం ఏడుస్తున్నాను 🌙😭", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Internet Loss", "title": "WiFi Cut During Presentation", "caption": "క్లయింట్ కి ప్రజెంటేషన్ ఇస్తుండగా నెట్ పోయింది.. కొంప మునిగిపోయింది! 🔌🛑", "emoji": "🛑", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Loan Stress", "title": "EMI Deduction Message", "caption": "జీతం వచ్చిన వెంటనే EMI కట్ అయిపోయింది.. చేతిలో చిల్లిగవ్వ లేదు 💸📉", "emoji": "📉", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Laptop Dead", "title": "Blue Screen Of Death", "caption": "సేవ్ చేయని ప్రాజెక్ట్ ఉండగా ల్యాప్‌టాప్ బ్లూ స్క్రీన్ ఇచ్చేసింది.. కన్నీళ్లే మిగిలాయి 💻💀", "emoji": "💻", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Toxic Boss", "title": "Micro Management Nightmare", "caption": "ప్రతి అరగంటకి వచ్చి స్టేటస్ అడిగే మేనేజర్ ని తట్టుకోలేకపోతున్నాను భయ్యా 🤬😤", "emoji": "🤬", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Cancelled Leave", "title": "Leave Rejected For Holiday", "caption": "సంక్రాంతి సెలవులకి ప్లాన్ చేసుకుంటే లీవ్ రిజెక్ట్ చేశారు.. ఘోరమైన అన్యాయం 🚷😭", "emoji": "😭", "sentiment": "negative", "slug": "bad"},

    # =========================================================================
    # 2. BENGALI MEMES (16 Positive, 16 Neutral, 16 Negative)
    # =========================================================================
    # --- Bengali Positive (16) ---
    {"lang": "Bengali", "tag": "MemoSen Classic", "title": "Disaster Girl Prod Test", "caption": "দারুণ খেলা হচ্ছে ভাই! প্রোডাকশনে টেস্ট করে দেখি কী হয় 🚀💥", "emoji": "😼", "sentiment": "positive", "slug": "disastergirl"},
    {"lang": "Bengali", "tag": "Food Emotion", "title": "Biryani vs Hostel Khichdi", "caption": "মায়ের হাতের ইলিশ মাছ vs মেসের ঠান্ডা ডাল-ভাত: চরম চোখের জল 🍲💔", "emoji": "🍲", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Ghost Code", "title": "Bhoot In My Repository", "caption": "কোড একবারেই রান হয়ে গেল? নিশ্চিত কোথাও বড় একটা ভূত লুকিয়ে আছে! 👻🚫", "emoji": "👻", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Bengali", "tag": "Football Rivalry", "title": "East Bengal vs Mohun Bagan", "caption": "ডার্বি ম্যাচের দিন অফিসে কাজের কথা বললে মার খাবেন ভাই ⚽🔥", "emoji": "⚽", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Pujo Joy", "title": "Durga Pujo Bonus Credited", "caption": "পুজোর বোনাস অ্যাকাউন্টে ঢুকতেই কলকাতার রাস্তায় ঢাকের আওয়াজ! 🥁✨", "emoji": "🥁", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Feluda Brain", "title": "Mogojastro Bug Solved", "caption": "মগজাস্ত্র ব্যবহার করে ৫ মিনিটের মধ্যে বাগ সমাধান করে ফেললাম! 🔍💡", "emoji": "🔍", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Coffee House", "title": "Adda With Old Friends", "caption": "কলেজ স্ট্রিট কফি হাউসে বসে গরম কফি আর বন্ধুদের তুমুল আড্ডা! ☕🎉", "emoji": "☕", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Client Praise", "title": "Client Loved The Feature", "caption": "ক্লায়েন্ট রিভিউ মিটিংয়ে বলল: অসাধারণ কাজ হয়েছে! মনটা জুড়িয়ে গেল 🌟👏", "emoji": "🌟", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Weekend Mood", "title": "Friday Evening Phuchka", "caption": "শুক্রবার বিকেলে অফিস ছুটি আর পার্ক স্ট্রিটে দাঁড়িয়ে ফুচকা খাওয়া! 🤤🎊", "emoji": "🤤", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Code Poetry", "title": "Clean Script Celebration", "caption": "আমার কোড যেন রবীন্দ্রনাথের কবিতা, প্রতিটি লাইনে নিখুঁত ছন্দ! 📜✨", "emoji": "📜", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Sweets Love", "title": "Rosogolla After Sprint", "caption": "স্প্রিন্ট রিলিজ সফল হতেই টিমের জন্য কে সি দাশের রসগোল্লা! 🍯😋", "emoji": "🍯", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Darjeeling Trip", "title": "Approved Annual Leave", "caption": "ম্যানেজার দার্জিলিং ট্যুরের ছুটি মঞ্জুর করে দিয়েছে.. জয় মা তারা! 🏔️🚂", "emoji": "🏔️", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Hike Joy", "title": "Expected Promotion Achieved", "caption": "অবশেষে কাঙ্ক্ষিত প্রমোশন লেটার হাতে পেলাম.. আজ আনন্দের সীমা নেই! 🏆🥂", "emoji": "🏆", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Winter Comfort", "title": "Nolen Gur Season", "caption": "শীতের সকালে নলেন গুড়ের সন্দেশ আর কোডিং.. জীবনটা স্বর্গীয়! ❄️🍯", "emoji": "❄️", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "Sourav Ganguly", "title": "Dada Style Comeback", "caption": "লর্ডসের ব্যালকনিতে সৌরভ গাঙ্গুলীর মতো জামা উড়িয়ে কামব্যাক করলাম! 🏏🔥", "emoji": "🏏", "sentiment": "positive", "slug": "leo"},
    {"lang": "Bengali", "tag": "App Release", "title": "Zero Crash On Launch", "caption": "অ্যাপ স্টোরে লাইভ হলো এবং কোনও ক্র্যাশ রিপোর্ট নেই.. জয় গুরু! 📱🎉", "emoji": "📱", "sentiment": "positive", "slug": "leo"},

    # --- Bengali Neutral (16) ---
    {"lang": "Bengali", "tag": "Kolkata Adda", "title": "Coffee House Intellectuals", "caption": "চা এর দোকানে বসে পুরো বিশ্বের অর্থনীতি আর রাজনীতি সমাধান করে ফেলেছি ☕📰", "emoji": "☕", "sentiment": "neutral", "slug": "kermit"},
    {"lang": "Bengali", "tag": "Feluda Deduction", "title": "Topshe Mystery", "caption": "তোপসে, এই বাগটার পেছনে নির্ঘাত ম্যানেজারের কোনো গোপন ষড়যন্ত্র আছে! 🔍🧐", "emoji": "🔍", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Bengali", "tag": "Sleep Priority", "title": "Client Deadline Ignored", "caption": "ক্লায়েন্ট বলে দিল: কাল সকাল ৯টায় সব চাই! আমি: ঠিক আছে, ঘুম থেকে উঠে ভাবব 😴", "emoji": "😴", "sentiment": "neutral", "slug": "cheems"},
    {"lang": "Bengali", "tag": "Bengali Sarcasm", "title": "Byomkesh Truth", "caption": "সত্যের সন্ধানে বের হয়ে দেখি পুরো কোডবেসটাই চ্যাটজিপিটি দিয়ে লেখা 🕵️‍♂️💀", "emoji": "🕵️‍♂️", "sentiment": "neutral", "slug": "fry"},
    {"lang": "Bengali", "tag": "Rainy Day", "title": "Khichuri Weather Kolkata", "caption": "বৃষ্টির দিনে অফিসে বসে খিচুড়ি আর তেলেভাজার কথা ভাবার সময় 🌧️🍲", "emoji": "🌧️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Metro Commute", "title": "Esplanade Metro Line", "caption": "এসপ্ল্যানেড মেট্রো স্টেশনে দাঁড়িয়ে দার্শনিক চিন্তা করার দৈনিক অভ্যাস 🚇💭", "emoji": "🚇", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Daily Routine", "title": "Salt Lake Sector 5 Bus", "caption": "সেক্টর ফাইভের বাসে ঝুলতে ঝুলতে জীবনের মোক্ষলাভের চেষ্টা 🚌🧘", "emoji": "🚌", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Book Fair", "title": "Boimela Stroll", "caption": "বইমেলায় গিয়ে বই কেনার চেয়ে লিটল ম্যাগাজিনের স্টলে চা খাওয়া বেশি জরুরি 📚☕", "emoji": "📚", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "College Life", "title": "Presidency Canteen Gossip", "caption": "ক্যান্টিনে বসে ঘণ্টার পর ঘণ্টা তর্ক করেও কোনও সিদ্ধান্ত বের হলো না 🗣️⏳", "emoji": "🗣️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Tech Debate", "title": "Mac vs Linux Argument", "caption": "উইন্ডোজ বনাম লিনাক্স নিয়ে ক্যাবিনে এক ঘণ্টা ধরে বুদ্ধিজীবী বিতর্ক 💻🐧", "emoji": "💻", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Sunday Lazy", "title": "Bhaat Ghoom Tradition", "caption": "রবিবার দুপুরে মাংস-ভাত খাওয়ার পর একটা দীর্ঘ ভাতঘুমের প্রয়োজনীয়তা 🍛😴", "emoji": "🍛", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Standup Update", "title": "Nothing New In Scrum", "caption": "কাল যা বলেছিলাম আজও তাই বলব.. শুধু তারিখটা পাল্টে দিয়েছি 📋🔄", "emoji": "📋", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Market Visit", "title": "Bajar Dor Bargain", "caption": "মাছের বাজারে গিয়ে ইলিশের দাম শুনে নীরব দর্শকের ভূমিকা পালন করলাম 🐟👀", "emoji": "🐟", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "New Year Goal", "title": "Nabobarsho Promises", "caption": "পয়লা বৈশাখে বলেছিলাম রোজ সকালে হাঁটব.. এখনও বিছানায় বসে চা খাচ্ছি 🌅🛏️", "emoji": "🌅", "sentiment": "neutral", "slug": "cheems"},
    {"lang": "Bengali", "tag": "Music Taste", "title": "Rabindrasangeet On Loop", "caption": "কোড লিখতে বসে ব্যাকগ্রাউন্ডে রবিঠাকুরের গান চালিয়ে দেওয়া এক অদ্ভুত শান্তি 🎵🎧", "emoji": "🎵", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Bengali", "tag": "Office AC", "title": "Winter In June Inside Office", "caption": "বাইরে ৪২ ডিগ্রি গরম কিন্তু অফিসের এসির ঠান্ডায় কাশ্মীর মনে হচ্ছে ❄️🏢", "emoji": "❄️", "sentiment": "neutral", "slug": "fine"},

    # --- Bengali Negative (16) ---
    {"lang": "Bengali", "tag": "Corporate Tragedy", "title": "Monday Blues Kolkata", "caption": "সোমবারে অফিসে যাওয়ার চেয়ে সুন্দরবনে বাঘের সামনে যাওয়া অনেক ভালো ছিল 🐅", "emoji": "🐅", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Salt Lake IT", "title": "Sector 5 Auto Struggle", "caption": "সল্টলেক সেক্টর ৫ এর অটো লাইনে দাঁড়িয়ে মোক্ষ লাভ করার অনুভূতি 🚖🤦‍♂️", "emoji": "🚖", "sentiment": "negative", "slug": "fine"},
    {"lang": "Bengali", "tag": "Durga Puja Mood", "title": "Pujo Shopping Budget Crash", "caption": "পুজোর শপিং করতে গিয়ে নিজের ব্যাঙ্ক ব্যালেন্স দেখে হার্ট অ্যাটাক 💸😱", "emoji": "💸", "sentiment": "negative", "slug": "sarcasticbear"},
    {"lang": "Bengali", "tag": "College Life", "title": "Semester Exam Night", "caption": "সারা বছর পড়া নেই, পরীক্ষার আগের রাতে সিলেবাস দেখে মনে হচ্ছে নতুন গ্রহের ভাষা 📚😭", "emoji": "😭", "sentiment": "negative", "slug": "fry"},
    {"lang": "Bengali", "tag": "Prod Outage", "title": "Database Dropped By Intern", "caption": "ইন্টার্ন প্রডাকশন ডাটাবেস ড্রপ করে বাড়ি চলে গেছে.. হায় ভগবান! 😱💥", "emoji": "😱", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Appraisal Grief", "title": "Peanuts Hike In Appraisal", "caption": "সারা বছর গাধার মতো খেটে হাইকের নামে হাতে বাদাম ধরিয়ে দিল! 🥜😭", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Train Delay", "title": "Sealdah Local Stuck In Signal", "caption": "শিয়ালদহ লোকাল সিগন্যালে দাঁড়িয়ে ১ ঘণ্টা.. জীবনের প্রতি তীব্র বিরক্তি 🚂🛑", "emoji": "🛑", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Hot Summer", "title": "Load Shedding In Summer Night", "caption": "কালবৈশাখী এলো না কিন্তু লোডশেডিং এসে রাতের ঘুম কেড়ে নিল 🕯️🥵", "emoji": "🥵", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Merge Conflict", "title": "Entire Branch Corrupted", "caption": "গিট ব্রাঞ্চে এমন কনফ্লিক্ট হয়েছে যে পুরো প্রজেক্টটাই ডিলিট করতে ইচ্ছে করছে 💻💀", "emoji": "💻", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Client Rage", "title": "Angry Escalation Email", "caption": "সকাল ১০টায় ক্লায়েন্টের রেড-ফ্ল্যাগ এসকেলেশন ইমেল দেখে রক্তচাপ বেড়ে গেল 🚨📧", "emoji": "🚨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Weekend Ruined", "title": "Sunday Support Call", "caption": "রবিবার সকালে ম্যানেজার ফোন করে বলল: একটু লগইন করতে হবে ভাই! 📞💀", "emoji": "📞", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Broken Laptop", "title": "Spilled Tea On Keyboard", "caption": "কাজের মাঝে কিবোর্ডের ওপর গরম চা ঢেলে ফেললাম.. সব শেষ! ☕💻", "emoji": "☕", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Interview Reject", "title": "Ghosted After 5 Rounds", "caption": "পাঁচ রাউন্ড ইন্টারভিউ নেওয়ার পর কোম্পানি আর কোনও রিপ্লাই দিল না 👻🚪", "emoji": "👻", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Waterlogging", "title": "Kolkata Waterlogging Nightmare", "caption": "অফিস থেকে বাড়ি ফেরার পথে কোমর সমান জলে দাঁড়িয়ে কান্না পাচ্ছে 🌧️🚶‍♂️", "emoji": "🌧️", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Failed Deploy", "title": "Friday Night 500 Error", "caption": "শুক্রবার রাতে ৫টি সার্ভারে ইন্টারনাল সার্ভার এরর.. মাথায় হাত! 🤦‍♂️🚨", "emoji": "🤦‍♂️", "sentiment": "negative", "slug": "bad"},
    {"lang": "Bengali", "tag": "Salary Vanished", "title": "Rent And EMI Devastation", "caption": "বাড়িভাড়া আর ইএমআই দিতেই মাসের ৫ তারিখে ওয়ালেট খালি হয়ে গেল 💸📉", "emoji": "💸", "sentiment": "negative", "slug": "bad"},

    # =========================================================================
    # 3. HINDI & HINGLISH MEMES (16 Positive, 16 Neutral, 16 Negative)
    # =========================================================================
    # --- Hindi Positive (16) ---
    {"lang": "Hindi", "tag": "Mirzapur Attitude", "title": "Munna Bhaiya Royalty", "caption": "जब कोड पहली बार में बिना किसी एरर के कंपाइल हो जाए: कभी कभी लगता है अपुन ही भगवान है! 👑🔥", "emoji": "👑", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Gangs of Wasseypur", "title": "Faizal Badla", "caption": "बाप का, दादा का, भाई का.. सबका बदला लेगा तेरा ये सेमीकोलन 🔫🤠", "emoji": "🔫", "sentiment": "positive", "slug": "bad"},
    {"lang": "Hindi", "tag": "WFH Reality", "title": "Formal Top Pyjama Bottom", "caption": "कुर्ता ऊपर, पायजामा नीचे: जूम कॉल पर वर्क फ्रॉम होम की असली कहानी 👔🩳", "emoji": "👔", "sentiment": "positive", "slug": "cheems"},
    {"lang": "Hindi", "tag": "Shark Tank Ashneer", "title": "Profitable Sprint Launch", "caption": "भाई तूने तो आग लगा दी! पूरा फीचर बिना बग के रिलीज हो गया 🚀🔥", "emoji": "🚀", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Hera Pheri", "title": "Salary Credited SMS Joy", "caption": "पैसा ही पैसा होगा! जब महीने की पहली तारीख को सैलरी अकाउंट में आ जाए 💰🕺", "emoji": "💰", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Munna Bhai MBBS", "title": "Jaadu Ki Jhappi Bugfix", "caption": "सीनियर ने एक लाइन में बग ठीक कर दिया.. जादू की झप्पी का अहसास! 🤗✨", "emoji": "🤗", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Sholay Classic", "title": "Jai Veeru Partnership", "caption": "ये दोस्ती हम नहीं तोड़ेंगे: डेवलपर और क्यूए जब मिलकर प्रोडक्शन बचा लें 🤝🎉", "emoji": "🤝", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Chak De India", "title": "Sprint 70 Minutes Speech", "caption": "ये सत्तर मिनट तुमसे कोई नहीं छीन सकता.. शानदार कोड डिलीवर हो गया! 🏆🌟", "emoji": "🏆", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Golmaal Fun", "title": "Friday Logout Excitement", "caption": "शुक्रवार शाम को लैपटॉप बंद करके पार्टी मोड ऑन करने का सुकून! 🍻🎊", "emoji": "🍻", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Bollywood Energy", "title": "Shah Rukh Khan Signature Pose", "caption": "जब क्लाइंट बोले 'अप्रूव्ड विद नो चेंजेस': अपनी तो जैसे तैसे कट जाएगी! 😎✨", "emoji": "😎", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Chai Love", "title": "Tapri Chai Post Deployment", "caption": "सफल डिप्लॉयमेंट के बाद टपरी पर अदरक वाली चाय और समोसा.. जन्नत! ☕🤤", "emoji": "☕", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Lagaan Spirit", "title": "Cricket Match Victory", "caption": "मैनेजर ने टीम को दिया पूरा दिन ऑफ.. मैच जीत गए भाई! 🏏🎉", "emoji": "🏏", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Pushpa Hindi", "title": "Main Jhukega Nahi Release", "caption": "बग कितना भी गहरा हो, अपुन झुकेगा नहीं साला! 🪓🔥", "emoji": "🪓", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Panchayat Sachiv", "title": "Beer Party Phulera", "caption": "सचिव जी ने टंकी पर बैठकर बीयर पी ली.. वीकेंड का स्वागत! 🍺🌾", "emoji": "🍺", "sentiment": "positive", "slug": "leo"},
    {"lang": "Hindi", "tag": "Rancho 3 Idiots", "title": "All Is Well Deployment", "caption": "दिल को बोलो ऑल इज वेल, कोड अपने आप टेस्ट पास कर लेगा! 💖💡", "emoji": "💖", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Hindi", "tag": "Diwali Bonus", "title": "Cash Bonus Sweet Box", "caption": "दिवाली पर सोनपापड़ी नहीं बल्कि रियल कैश बोनस मिला.. खुशी का ठिकाना नहीं! 🎁🥳", "emoji": "🎁", "sentiment": "positive", "slug": "leo"},

    # --- Hindi Neutral (16) ---
    {"lang": "Hindi", "tag": "Shark Tank Ashneer", "title": "Doglapan Exposed", "caption": "ये सब दोगलापन है! जब मैनेजमेंट बोलता है वर्क-लाइफ बैलेंस बहुत ज़रूरी है 🤡", "emoji": "🤡", "sentiment": "neutral", "slug": "sarcasticbear"},
    {"lang": "Hindi", "tag": "Hera Pheri Akshay", "title": "21 Din Mein Paisa Double", "caption": "21 दिन में पूरा प्रॉडक्ट तैयार कर देंगे: सेल्स टीम क्लाइंट से वादा करते हुए 🤥📦", "emoji": "🤥", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Hindi", "tag": "TMKOC Jethalal", "title": "Sundar Problem", "caption": "चाय पीते ही क्लाइंट का पैनिक कॉल आ गया.. अब जिंदगी में बस बबिता जी की शांति चाहिए ☕🤦‍♂️", "emoji": "☕", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "3 Idiots", "title": "Raju Ki Maa", "caption": "पनीर तो बेटा कुछ दिनों में सुनार की दुकान पर मिलेगा: मंहगाई और अप्रैज़ल का दर्द 🧀💍", "emoji": "🧀", "sentiment": "neutral", "slug": "sarcasticbear"},
    {"lang": "Hindi", "tag": "Monday Alarm", "title": "Gym & Alarm Reality", "caption": "सोमवार की सुबह: आज से रोज 6 बजे उठूंगा! मंगलवार सुबह: अलार्म सीधा डिलीट 😴🛌", "emoji": "😴", "sentiment": "neutral", "slug": "fry"},
    {"lang": "Hindi", "tag": "Corporate Talk", "title": "Synergy And Bandwidth", "caption": "मीटिंग में 'सिनर्जी' और 'बैंडविड्थ' बोलकर आधा घंटा आराम से निकाल दिया 🗣️📊", "emoji": "🗣️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Panchayat Pradhan", "title": "Pradhan Ji Discussion", "caption": "प्रधान जी पंचायत में बैठकर सोच रहे हैं कि ये ब्लॉकचेन किस चिड़िया का नाम है 🌾🤔", "emoji": "🌾", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Bangalore Traffic", "title": "Silk Board Jam Philosophy", "caption": "सिल्क बोर्ड जाम में बैठे-बैठे मैंने जीवन का सारा दर्शन समझ लिया 🚗🧘", "emoji": "🚗", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Diet Plan", "title": "Salad vs Chole Bhature", "caption": "डाइट शुरू की थी लेकिन लंच में छोले भटूरे देखकर मन पिघल गया 🥗🥪", "emoji": "🥗", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Remote Work", "title": "Nodding On Zoom Call", "caption": "जूम कॉल पर सिर्फ सिर हिलाते रहो ताकि लगे कि बहुत ध्यान से सुन रहे हो 💻🙃", "emoji": "💻", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Cricket Score", "title": "Checking Score In Meeting", "caption": "मैनेजर जब स्क्रीन शेयर कर रहा हो, तब टैब स्विच करके क्रिकेट स्कोर देखना 🏏👀", "emoji": "🏏", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Hindi", "tag": "Scrum Master", "title": "Standup Blockers Check", "caption": "कोई ब्लॉकर नहीं है लेकिन फिर भी काम कल ही होगा 📋⏳", "emoji": "📋", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "LinkedIn Post", "title": "Agree Agree Influencer", "caption": "लिंक्डइन पर ज्ञान बांटने वाले इन्फ्लुएंसर्स को देखकर मौन धारण कर लिया 📱🤐", "emoji": "📱", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Online Shopping", "title": "Cart Full No Checkout", "caption": "अमेज़न कार्ट में 50 सामान जोड़ लिए पर पेमेंट करने की हिम्मत नहीं हुई 🛒💭", "emoji": "🛒", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Weekend Routine", "title": "Binge Watch Netflix", "caption": "पूरा वीकेंड कंबल में बैठकर वेब सीरीज देखने का साधारण कार्यक्रम 📺🍿", "emoji": "📺", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Hindi", "tag": "Casual Friday", "title": "Pizza In Office Cafeteria", "caption": "ऑफिस में मुफ्त का पिज्जा मिला है तो स्टैंडअप थोड़ा देर से भी चलेगा 🍕😋", "emoji": "🍕", "sentiment": "neutral", "slug": "fine"},

    # --- Hindi Negative (16) ---
    {"lang": "Hindi", "tag": "Hera Pheri", "title": "Baburao Deep Prayer", "caption": "उठा ले रे देवा उठा ले.. मेरे को नहीं इस बग को उठा ले! 😭🙏", "emoji": "🙏", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Panchayat Satire", "title": "Binod Live Observation", "caption": "देख रहे हो बिनोद.. कैसे फ्राइडे शाम 6 बजे नया फीचर डिप्लॉय हो रहा है 💀👀", "emoji": "👀", "sentiment": "negative", "slug": "drake"},
    {"lang": "Hindi", "tag": "Corporate Hike", "title": "Salary Hike Meeting", "caption": "ये कोई तरीका है भीख मांगने का? सैलरी हाइक डिस्कशन में एचआर से मैं 💸", "emoji": "💸", "sentiment": "negative", "slug": "fry"},
    {"lang": "Hindi", "tag": "Developer Agony", "title": "Missing Semicolon 4 Hours", "caption": "बग ढूंढने के लिए पूरा कोड रीराइट कर दिया, फिर पता चला सेमीकोलन मिसिंग था 🤦‍♂️💀", "emoji": "🤦‍♂️", "sentiment": "negative", "slug": "fine"},
    {"lang": "Hindi", "tag": "Code-Mixed Hinglish", "title": "Bro Pushed Straight to Main", "caption": "Bro really thought he could fix production without taking a database backup 💀", "emoji": "💀", "sentiment": "negative", "slug": "cheems"},
    {"lang": "Hindi", "tag": "Production Outage", "title": "Critical Server Down Alert", "caption": "रात 3 बजे सर्वर क्रैश हो गया.. पूरी रात जागकर बग ढूंढने की सजा 🚨😭", "emoji": "🚨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Hike Disappointment", "title": "Peanuts Rating Letter", "caption": "साल भर 14 घंटे काम किया और रेटिंग मिली 'मीट्स एक्सपेक्टेशन'.. दिल टूट गया 💔📉", "emoji": "💔", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Interview Agony", "title": "Live Coding Panic Attack", "caption": "इंटरव्यूअर ने बोला स्क्रीन शेयर करो और मेरा दिमाग बिल्कुल खाली हो गया 🥶😱", "emoji": "🥶", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Client Rage", "title": "Angry Weekend Call", "caption": "शनिवार की सुबह क्लाइंट का गुस्सा भरा कॉल आ गया.. वीकेंड तबाह! 🤬📱", "emoji": "🤬", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Broken Build", "title": "CI CD Pipeline Red", "caption": "पूरी पाइपलाइन लाल हो गई.. 20 टेस्ट फेल और प्रोडक्शन ब्लॉक! 🛑💥", "emoji": "🛑", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Toxic Boss", "title": "Late Night Slack Message", "caption": "रात 11 बजे मैनेजर का मैसेज आया: 'क्विक कॉल?'.. पसीना छूट गया 😨💬", "emoji": "😨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Unpaid Overtime", "title": "16 Hours Daily Work", "caption": "बिना किसी ओवर-टाइम पे के लगातार तीसरे हफ्ते 16 घंटे काम चल रहा है 😫💼", "emoji": "😫", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Data Loss", "title": "Accidental Git Reset Hard", "caption": "गलती से 'git reset --hard' चला दिया और 3 दिन की मेहनत पानी में बह गई 😭💻", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Rent Burden", "title": "Bangalore Flat Rent Hike", "caption": "मकान मालिक ने 40% किराया बढ़ा दिया.. अब सड़क पर तंबू लगाना पड़ेगा 💸🏚️", "emoji": "💸", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Monday Horror", "title": "Monday Morning 9 AM Meeting", "caption": "सोमवार सुबह 9 बजे पहला ही कॉल रिव्यू का.. जिंदगी से भरोसा उठ गया 💀⏰", "emoji": "💀", "sentiment": "negative", "slug": "bad"},
    {"lang": "Hindi", "tag": "Rejection Mail", "title": "Standard Auto Reject", "caption": "'वी विश यू लक इन योर फ्यूचर एंडेवर्स'.. यह ईमेल पढ़कर आंखों में आंसू आ गए ✉️😢", "emoji": "✉️", "sentiment": "negative", "slug": "bad"},

    # =========================================================================
    # 4. TAMIL MEMES (16 Positive, 16 Neutral, 16 Negative)
    # =========================================================================
    # --- Tamil Positive (16) ---
    {"lang": "Tamil", "tag": "Code Magic", "title": "Mystery Working Script", "caption": "கோட் வேலை செய்யுது ஆனா எப்படி செய்யுதுன்னு எனக்கே தெரியல! அஸ்ஸலாமு அலைக்கும் 🤷‍♂️✨", "emoji": "🤷‍♂️", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Tamil", "tag": "Santhanam Counter", "title": "Overtime Work Rejection", "caption": "மேனேजर: இன்னைக்கு கொஞ்சம் லேட்டா போக முடியுமா? நான்: வாய்ப்பில்லை ராஜா! 🙅‍♂️🚀", "emoji": "🙅‍♂️", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Rajinikanth Style", "title": "Kabali Comeback", "caption": "கபாலி டா! பக் எல்லாம் முடிச்சுட்டு புரொடக்ஷன்ல சிங்கம் மாதிரி நிக்கிறோம் 😎🔥", "emoji": "🦁", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Vijay Thalapathy", "title": "Master Sprint Complete", "caption": "ஸ்பிரிண்ட் வெற்றிகரமாக முடிந்தது.. வாத்தி கம்மிங் கொண்டாட்டம் தான்! 🎵🕺", "emoji": "🎵", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Ajith Thala", "title": "Billa Cool Head", "caption": "எவ்வளவு பிரஷர் வந்தாலும் கூலா கோட் பண்ணி பாஸ் பண்ணியாச்சு! 🕶️⚡", "emoji": "🕶️", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Vadivelu Comedy", "title": "Winner Celebration", "caption": "கைப்புள்ள ஜெயிச்சுட்டான்டா! கிளைன்ட் முழுசா அப்ரூவல் கொடுத்தாச்சு 🏆🥳", "emoji": "🏆", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Chennai Filter Coffee", "title": "Degree Coffee Happiness", "caption": "டிகிரி காபிய குடிச்சிட்டு கோட் அடிச்சா பக் தானா ஓடிப்போய்டும்! ☕✨", "emoji": "☕", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Weekend Mood", "title": "Marina Beach Breeze", "caption": "வெள்ளிக்கிழமை சாயங்காலம் மெரினா பீச்ல சுண்டல் சாப்பிடும் ஆனந்தம்! 🏖️🎉", "emoji": "🏖️", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Hike Surprise", "title": "Double Digit Appraisal", "caption": "எதிர்பார்க்காத அளவுக்கு அப்ரைசல் வந்திருக்கு.. இன்னைக்கு பிரியாணி விருந்து! 🍗💰", "emoji": "🍗", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Clean Architecture", "title": "Zero Warning Compile", "caption": "ஜீரோ வார்னிங், ஜீரோ எரர்.. கம்ப்யூட்டரே கைதட்டுது! 👏💡", "emoji": "👏", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Dhanush Swag", "title": "VIP Raghuvaran Win", "caption": "வேலையில்லா பட்டதாரி இல்லடா.. இப்போ நான் சீனியர் டெக் லீட்! 👔🌟", "emoji": "👔", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Kamal Haasan", "title": "Ulaga Nayagan Logic", "caption": "கமல் சார் படம் மாதிரி என் கோட்ல அவ்வளவு நுணுக்கம் இருக்கு! 🎭🎬", "emoji": "🎭", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Leave Approved", "title": "Pongal Leave Sanctioned", "caption": "பொங்கல் லீவ் அப்ரூவ் ஆயிடுச்சு.. ஊருக்கு போறோம் ஜாலியா! 🌾🚂", "emoji": "🌾", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Client Signoff", "title": "Happy Demo Meeting", "caption": "டெமோ முடிஞ்சதும் கிளைன்ட் பாராட்டு மழை பொழிஞ்சுட்டான்! 🌟🤝", "emoji": "🌟", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Bug Slayer", "title": "One Line Quick Fix", "caption": "மூணு நாள் தேடின பக்கை ஒரே ஒரு ஸ்பేஸ் விட்டு சரி பண்ணிட்டேன்! 🎯💡", "emoji": "🎯", "sentiment": "positive", "slug": "leo"},
    {"lang": "Tamil", "tag": "Bonus Day", "title": "Diwali Bonus Credited", "caption": "தீபாவளி போனஸ் அக்கவுண்ட்ல விழுந்தாச்சு.. பட்டாசு கிளப்புங்க! 🎆💸", "emoji": "🎆", "sentiment": "positive", "slug": "leo"},

    # --- Tamil Neutral (16) ---
    {"lang": "Tamil", "tag": "Vadivelu Comedy", "title": "Meeting Confusion Vadivelu", "caption": "எதுக்கு இந்த மீட்டிங் வெச்சீங்கன்னு யாருக்காவது தெரியுமா? 🤔😂", "emoji": "🤷‍♂️", "sentiment": "neutral", "slug": "fry"},
    {"lang": "Tamil", "tag": "Chennai IT Corridor", "title": "OMR Toll Gate Traffic", "caption": "OMR டிராபிக்ல மாட்டிக்கிட்டு வாழ்க்கையோட அர்த்தத்த தேடுற தருணம் 🛵🚗", "emoji": "🛵", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Interview Comedy", "title": "Spoken English Struggle", "caption": "இண்டர்வியூல இங்கிலீஷ் பேசும்போது நான் vs மனசுக்குள்ள நான் 🤐😂", "emoji": "🤐", "sentiment": "neutral", "slug": "drake"},
    {"lang": "Tamil", "tag": "Tea Kadai", "title": "Tea Kadai Bench Discussion", "caption": "டீ கடையில உட்கார்ந்து உலக அரசியலையும் ஐடி கம்பெனியையும் அலசுற கூட்டம் ☕📰", "emoji": "☕", "sentiment": "neutral", "slug": "kermit"},
    {"lang": "Tamil", "tag": "Daily Scrum", "title": "Standup Regular Dialogue", "caption": "நேத்து என்ன பண்ணீங்கன்னு கேட்டா யோசிக்க ரெண்டு நிமிஷம் வேணும் பாஸ் 📋⏳", "emoji": "📋", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Lunch Dilemma", "title": "Meals vs Variety Rice", "caption": "மதிய சாப்பாட்டுக்கு என்ன வாங்குறதுன்னு யோசிக்கவே ஒரு மணி நேரம் ஆகுது 🍱🤔", "emoji": "🍱", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "WFH Habit", "title": "Sleeping During Call", "caption": "ஆல்-ஹேண்ட்ஸ் மீட்டிங்ல மைக் ஆஃப் பண்ணிட்டு குறட்டை விடுற வாழ்க்கை 😴🛋️", "emoji": "😴", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Local Train", "title": "Beach to Tambaram Routine", "caption": "பீச் - தாம்பரம் ட்ரெயின்ல விண்டோ சீட் தேடுற எளிய மனிதனின் போராட்டம் 🚆🎧", "emoji": "🚆", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "New Framework", "title": "Too Many JS Libraries", "caption": "பழையதை படிக்கிறதுக்குள்ள புதுசா பத்து லைப்ரரி வந்துடுது 💻🔄", "emoji": "💻", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Weather Drama", "title": "Chennai Sunny Afternoon", "caption": "சென்னையில மூணே சீசன் தான்: வெயில், அக்னி வெயில், அதையும் தாண்டிய வெயில் ☀️🔥", "emoji": "☀️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Gym Dream", "title": "Gym Membership Postponed", "caption": "திங்கட்கிழமை ஜிம் போலாம்னு நினைச்சேன்.. ஆனா எந்த திங்கட்கிழமைன்னு சொல்லல 🏋️‍♂️🤷‍♂️", "emoji": "🏋️‍♂️", "sentiment": "neutral", "slug": "cheems"},
    {"lang": "Tamil", "tag": "Online Cart", "title": "Swiggy Cart Waiting", "caption": "கார்ட்ல போட்டு வெச்சிருக்கேன் ஆனா கூப்பன் கோடு வேலை செய்யல 🛒💭", "emoji": "🛒", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Code History", "title": "Who Wrote This Function", "caption": "இந்த கோட யார் எழுதினான்னு கிட் பிளேம் பாத்தா.. நானே தான் எழுதி இருக்கேன்! 🤦‍♂️🔍", "emoji": "🤦‍♂️", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Tamil", "tag": "Weekend Routine", "title": "Saturday Afternoon Sleep", "caption": "சனிக்கிழமை மதியம் நல்லா தூங்கி எழுந்தா மணி ஆறு ஆயிடுது 🛌😴", "emoji": "🛌", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Client Call", "title": "Camera Off Nodding", "caption": "கேமரா ஆஃப்ல இருக்கும்போது நாம என்ன பண்றோம்னு யாருக்கு தெரியும் 💻🙃", "emoji": "💻", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Tamil", "tag": "Documentation", "title": "Empty Documentation Tab", "caption": "டாக்குமெண்டேஷன் படிக்கலாம்னு தொறந்தா நாலு வரி தான் இருக்கு 📄👀", "emoji": "📄", "sentiment": "neutral", "slug": "fine"},

    # --- Tamil Negative (16) ---
    {"lang": "Tamil", "tag": "Kollywood Sarcasm", "title": "Friday Prod Nightmare", "caption": "வெள்ளிக்கிழமை சாயங்காலம் புரொடக்ஷன்ல கோட் புஷ் பண்ணின என் நிலைமை 💀🚨", "emoji": "💀", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Vadivelu Panic", "title": "Aahaa Oru Mudivoda Thaan", "caption": "ஆஹா! ஒரு முடிவோடு தான் வந்துருக்காங்க.. கிளைன்ட் கிட்ட இருந்து தப்பிக்க முடியாது 🏃‍♂️💨", "emoji": "🏃‍♂️", "sentiment": "negative", "slug": "sarcasticbear"},
    {"lang": "Tamil", "tag": "Salary Vanished", "title": "Account Balance Zero", "caption": "சம்பளம் வந்த அடுத்த நிமிஷமே அக்கவுண்ட் ஜீரோ ஆயிடுச்சு.. கண்ணீர் மல்க বিদায় 💸😭", "emoji": "💸", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Vadivelu Agony", "title": "Vandhutanunga Da Call", "caption": "வந்துட்டானுங்கடா வந்துட்டானுங்க.. வீக்கெண்ட்ல வேலைய வச்சிக்கிட்டு வந்துட்டானுங்க 😭🚨", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Crash Horror", "title": "Production Server 502", "caption": "லைவ் சர்வர்ல 502 பேட் கேட்வே.. மேனேஜர் கண்ணுல அனல் பறக்குது! 🔥😱", "emoji": "🔥", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Appraisal Pain", "title": "Single Digit Percentage", "caption": "இவ்வளவு உழைச்சதுக்கு வெறும் 2% ஹைகா.. மனசு சுக்குநூறா உடைஞ்சு போச்சு 💔📉", "emoji": "💔", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Interview Failure", "title": "Leetcode Hard Nightmare", "caption": "ஈஸியான கம்பெனின்னு நெனச்சு போனா லீட்கோட் ஹார்ட் கேட்டு கதற விட்டுட்டாங்க 😭💻", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Monday Fear", "title": "Sunday Night Panic Attack", "caption": "ஞாயிறு இரவு 9 மணிக்கு மேனேஜர் மெயில்.. தூக்கம் போச்சு! 📧😰", "emoji": "😰", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Merge Conflict", "title": "Git Conflict Mess", "caption": "மெர்ஜ் பண்ணும்போது 40 ஃபைல் கான்பிளிக்ட்.. தலையில துண்ட போட்டுக்க வேண்டியது தான் 🤦‍♂️💀", "emoji": "🤦‍♂️", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Overtime Hell", "title": "2 AM Release Drama", "caption": "நடுராத்திரி ரெண்டு மணிக்கு ஆபிஸ்ல உக்காந்து அழுதுட்டு இருக்கேன் 🌙😭", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Database Mistake", "title": "Truncate Table Run On Prod", "caption": "டெஸ்ட்னு நினைச்சு புரொடக்ஷன் டேபிளை காலி பண்ணிட்டேன்.. அவ்ளோதான் வேலை காலி! 💥🛑", "emoji": "💥", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Power Cut", "title": "EB Cut In Middle Of Code", "caption": "சார்ஜர் இல்லாம பேட்டரி 2% இருக்கும்போது கரண்ட் போயிடுச்சு.. பெருந்துயரம்! 🔌😱", "emoji": "🔌", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Toxic Boss", "title": "Micromanaging Lead", "caption": "நிமிஷத்துக்கு நிமிஷம் அப்டேட் கேக்குற மேனேஜர் கிட்ட இருந்து காப்பாத்துங்கடா 🤬😤", "emoji": "🤬", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Rent Hike", "title": "Chennai House Rent Horror", "caption": "அட்வான்ஸ் பத்து மாசம், வாடகை பாதி சம்பளம்.. ரோட்டுல தான் படுக்கணும் 💸🏚️", "emoji": "💸", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Cancelled Trip", "title": "Goa Trip Cancelled Due To Work", "caption": "கோவா டிக்கெட் போட்டு வெச்சிருந்தேன்.. கடைசி நிமிஷத்துல ரிலீஸ்னு சொல்லி தடுத்துட்டாங்க 🏖️💔", "emoji": "💔", "sentiment": "negative", "slug": "bad"},
    {"lang": "Tamil", "tag": "Laptop Dead", "title": "Spilled Coffee On MacBook", "caption": "லேப்டாப் மேல காபிய கொட்டிட்டேன்.. போர்டு போச்சு, ஃபைலும் போச்சு! ☕💻", "emoji": "💻", "sentiment": "negative", "slug": "bad"},

    # =========================================================================
    # 5. GLOBAL & HINGLISH MEMES (16 Positive, 16 Neutral, 16 Negative)
    # =========================================================================
    # --- Global Positive (16) ---
    {"lang": "Global", "tag": "Absolute Cinema", "title": "Leo DiCaprio Cheers", "caption": "When client says: 'Approved with zero revisions, payment released today' 😎🥂", "emoji": "🥂", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Big Brain", "title": "Roll Safe Galaxy Brain", "caption": "You can't have bugs in production if you never release anything to production 🧠💡", "emoji": "🧠", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Global", "tag": "Pure Bliss", "title": "Fixing Code by Deletion", "caption": "When you fix a 3-day production bug by deleting 200 lines of unused spaghetti code 🧹✨", "emoji": "✨", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "It Works On My Machine", "title": "Shipping Your Machine", "caption": "Developer: 'It works on my machine!' DevOps: 'Then we will ship your machine to the customer!' 💻📦", "emoji": "💻", "sentiment": "positive", "slug": "cheems"},
    {"lang": "Global", "tag": "Coffee Energy", "title": "Coffee Running My Organs", "caption": "My blood is 10% water and 90% double espresso right now ☕⚡", "emoji": "☕", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "StackOverflow Hero", "title": "Copy Pasted Script Worked", "caption": "The random 12-year-old answer on StackOverflow solved the entire company outage! 🏆🙌", "emoji": "🏆", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Friday Freedom", "title": "5 PM Friday Shutdown", "caption": "Closing all 87 browser tabs at 5 PM on Friday is pure spiritual therapy 🎉🏖️", "emoji": "🎉", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Senior Architect", "title": "Clean Refactor Merge", "caption": "Reduced query latency from 14 seconds to 80 milliseconds.. feel like a wizard! 🧙‍♂️⚡", "emoji": "🧙‍♂️", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Demo Success", "title": "Flawless Live Presentation", "caption": "Live demo worked on the first try in front of the VP of Engineering! 🌟👏", "emoji": "🌟", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Bonus Announcement", "title": "Quarterly Bonus Released", "caption": "Company exceeded revenue targets and quarterly profit bonus just hit the bank! 💰🥳", "emoji": "💰", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "CI Pipeline", "title": "All Green Checkmarks", "caption": "Looking at 45 green checkmarks on GitHub Actions like a work of modern art 🟢✅", "emoji": "🟢", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Dark Mode Bliss", "title": "Perfect Dark Theme", "caption": "Turning on OLED dark mode in IDE feels like giving my eyeballs a warm blanket 🌙🖤", "emoji": "🌙", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Promotion Confirmed", "title": "Staff Engineer Letter", "caption": "Promotion finalized and compensation band raised to top tier! 🚀🥂", "emoji": "🚀", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "No Meetings Day", "title": "Deep Focus Friday", "caption": "Zero meetings scheduled for the entire day.. pure uninterrupted coding paradise 🎧💻", "emoji": "🎧", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Test Automation", "title": "100 Percent Unit Test Pass", "caption": "All 800 automated test cases passed without a single flake! 🎯🔥", "emoji": "🎯", "sentiment": "positive", "slug": "leo"},
    {"lang": "Global", "tag": "Coffee Treat", "title": "Team Coffee Treat", "caption": "Manager bought everyone iced caramel macchiatos after sprint delivery! ☕🧁", "emoji": "☕", "sentiment": "positive", "slug": "leo"},

    # --- Global Neutral (16) ---
    {"lang": "Global", "tag": "Developer History", "title": "Doge Assembly vs CSS", "caption": "Developers in 1970 writing OS in assembly vs Me crying because CSS centering broke 🐶🐕", "emoji": "🐕", "sentiment": "neutral", "slug": "cheems"},
    {"lang": "Global", "tag": "Automation Trap", "title": "6 Hours Automating", "caption": "Spending 6 hours writing a Python script to automate a task that takes 20 seconds manually 🤖🕒", "emoji": "🤖", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Global", "tag": "StackOverflow Down", "title": "Global Tech Standstill", "caption": "If StackOverflow ever goes down for 24 hours, the world economy stops moving 🌍📉", "emoji": "🌍", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Browser Tabs", "title": "80 Tabs Open", "caption": "Having 80 browser tabs open just so I don't forget something I will never read 🌐📑", "emoji": "🌐", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Agile Standup", "title": "Yesterday Today Blockers", "caption": "Yesterday I investigated, today I will continue investigating, no blockers 📋⏳", "emoji": "📋", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Keyboard Sound", "title": "Mechanical Keyboard Click", "caption": "Click clack of mechanical switches making it sound like I am hacking the Pentagon ⌨️🎧", "emoji": "⌨️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Git Commit Log", "title": "Fix Typo Commit", "caption": "Commit history showing 'fixed bug', 'really fixed bug', 'final fix', 'final final fix' 📝🔍", "emoji": "📝", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "AI Assistants", "title": "Asking AI For Syntax", "caption": "Senior developer with 10 years experience asking AI how to write a regex 🤖💡", "emoji": "🤖", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Global", "tag": "Lunch Break", "title": "Standing in Lunch Line", "caption": "Standing in cafeteria queue debating whether to get burrito or salad 🌯🥗", "emoji": "🌯", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Software Version", "title": "Restart For Update", "caption": "Clicking 'Remind me tomorrow' on OS system update for the 47th consecutive day 💻⏰", "emoji": "💻", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Documentation Reality", "title": "TODO Add Comments", "caption": "Code comment says: // TODO: Clean this up later (Written 7 years ago) 📜⏳", "emoji": "📜", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Hardware Fan", "title": "Laptop Fan Airplane Mode", "caption": "Opening Docker and Android Studio causes laptop fan to sound like Boeing 747 takeoff 🛫💨", "emoji": "🛫", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Desk Setup", "title": "Three Monitor Workspace", "caption": "Three 4K monitors: one for code, one for Slack, one for YouTube cat videos 🖥️🐱", "emoji": "🖥️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Naming Variables", "title": "Two Hard Things In CS", "caption": "There are only two hard things in Computer Science: cache invalidation and naming things 🧠🏷️", "emoji": "🧠", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Sprint Velocity", "title": "Story Point Fibonacci", "caption": "Arguing whether converting button color is 2 story points or 3 Fibonacci points 🎲📊", "emoji": "🎲", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Global", "tag": "Water Bottle", "title": "Hydration Reminder App", "caption": "Installed 3 hydration tracking apps just to remember to drink one glass of water 💧📱", "emoji": "💧", "sentiment": "neutral", "slug": "fine"},

    # --- Global Negative (16) ---
    {"lang": "Global", "tag": "Universal Sarcasm", "title": "Disappointed Fan Sarcasm", "caption": "Waah! Kya service hai! 10 ghante line mein khada rakh ke bola server down hai 😭💀", "emoji": "🤦‍♂️", "sentiment": "negative", "slug": "sarcasticbear"},
    {"lang": "Global", "tag": "Blame Game", "title": "Spider-Man Multi-Team Blame", "caption": "Frontend dev, Backend dev, and DevOps pointing at each other during an outage 👈👉", "emoji": "🕷️", "sentiment": "negative", "slug": "spiderman"},
    {"lang": "Global", "tag": "Senior Dev Panic", "title": "Junior Git Force Push", "caption": "Senior dev watching intern type 'git push --force origin main' with cold sweat 😱🚨", "emoji": "😱", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Dark Mode Only", "title": "Light Mode Blindness", "caption": "Opening an app that doesn't have dark mode at 2 AM feels like staring into the sun ☀️😵", "emoji": "☀️", "sentiment": "negative", "slug": "ch"},
    {"lang": "Global", "tag": "Production Down", "title": "500 Internal Error Nightmare", "caption": "Black Friday checkout page throwing 500 error.. millions disappearing every second 🚨📉", "emoji": "🚨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Infinite Loop", "title": "Browser Out Of Memory Crash", "caption": "Accidental infinite while loop froze entire browser and crashed un-saved work 💻💥", "emoji": "💥", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Layoff Anxiety", "title": "Mandatory Calendar Invite", "caption": "Received an unexpected invite titled 'Department Restructure Update' with HR copied 😰🚪", "emoji": "😰", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Corrupt Hard Drive", "title": "Lost Local Repository", "caption": "SSD corrupted and unsynced project work vanished into the void 😭💾", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Weekend On-Call", "title": "PagerDuty Pager Sirens", "caption": "PagerDuty alarm screaming at 3 AM on Sunday morning during thunderstorm 🚨📱", "emoji": "🚨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Zero Day Vulnerability", "title": "Log4j Style Emergency", "caption": "Critical zero-day security CVE dropped right before leaving for vacation 🛑🔓", "emoji": "🛑", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Micromanagement", "title": "Activity Tracker Software", "caption": "Company installing mouse-movement tracker to monitor bathroom breaks 🖱️😡", "emoji": "😡", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Burnout Exhaustion", "title": "Sixth Consecutive 70hr Week", "caption": "Staring blankly at monitor feeling completely drained and burned out 💀🕯️", "emoji": "💀", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Spilled Coffee", "title": "MacBook Keyboard Ruined", "caption": "Spilled hot coffee straight into the cooling vents of my brand new work laptop ☕💻", "emoji": "💻", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Cloud Bill Shock", "title": "Surprise 10000 Dollar Bill", "caption": "Forgot to terminate GPU instance over weekend and got a $12,000 AWS bill 💸😱", "emoji": "💸", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Denied Raise", "title": "Zero Percent Merit Increase", "caption": "Told there is no budget for cost of living raises while CEO buys third yacht 💔📉", "emoji": "💔", "sentiment": "negative", "slug": "bad"},
    {"lang": "Global", "tag": "Scope Creep", "title": "Client Doubled Requirements", "caption": "Client added 40 new features two days before hard contractual deadline ⏳😫", "emoji": "😫", "sentiment": "negative", "slug": "bad"}
]

PALETTES = [
    ("#4f46e5", "#06b6d4"), ("#e11d48", "#f97316"), ("#0f766e", "#06b6d4"),
    ("#7c3aed", "#ec4899"), ("#334155", "#1e293b"), ("#b45309", "#78350f"),
    ("#065f46", "#10b981"), ("#1e1b4b", "#4338ca"), ("#991b1b", "#ef4444")
]

def seed():
    print(f"[*] Seeding clean, perfectly balanced {len(UNIQUE_MEMES)} memes into {DB_PATH}...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE memes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meme_id TEXT UNIQUE,
        title TEXT,
        language TEXT,
        tag TEXT,
        caption TEXT,
        image_url TEXT,
        fallback_bg_start TEXT,
        fallback_bg_end TEXT,
        emoji TEXT,
        sentiment TEXT,
        keywords TEXT
    )
    """)

    cursor.execute("CREATE INDEX idx_memes_lang ON memes(language);")
    cursor.execute("CREATE INDEX idx_memes_sentiment ON memes(sentiment);")

    records = []
    for idx, item in enumerate(UNIQUE_MEMES):
        pal = PALETTES[idx % len(PALETTES)]
        meme_id = f"{item['lang'].lower()}-{idx+1}"
        image_url = f"https://api.memegen.link/images/{item['slug']}/{item['title'].replace(' ', '_')}/{item['lang']}.png"
        keywords = f"{item['lang'].lower()} {item['title'].lower()} {item['tag'].lower()} {item['sentiment']}"

        records.append((
            meme_id, item['title'], item['lang'], item['tag'], item['caption'], image_url,
            pal[0], pal[1], item['emoji'], item['sentiment'], keywords
        ))

    cursor.executemany("""
    INSERT INTO memes (
        meme_id, title, language, tag, caption, image_url,
        fallback_bg_start, fallback_bg_end, emoji, sentiment, keywords
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    conn.commit()

    cursor.execute("SELECT COUNT(*), COUNT(DISTINCT caption) FROM memes")
    total, distinct = cursor.fetchone()

    cursor.execute("SELECT sentiment, COUNT(*) FROM memes GROUP BY sentiment")
    counts = cursor.fetchall()
    print(f"[SUCCESS] Seeded {total} unique memes ({distinct} distinct) into {DB_PATH}!")
    print(f"[*] Class breakdown: {counts}")
    conn.close()

if __name__ == "__main__":
    seed()
